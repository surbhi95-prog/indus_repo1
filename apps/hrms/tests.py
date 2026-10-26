from datetime import date, datetime, time, timedelta
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

from django.test import SimpleTestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.hrms.models.employee_shift import EmployeeShift
from apps.hrms.models.roster import RosterAssignment
from apps.hrms.services.attendance_service import AttendanceService
from apps.hrms.pagination import get_pagination, page_queryset, pagination_metadata
from apps.hrms.serializers.shift_update_serializer import ShiftUpdateSerializer
from apps.hrms.shift_types import normalize_shift_type


class PaginationHelperTests(SimpleTestCase):
    def request(self, params=None):
        return SimpleNamespace(query_params=params or {})

    def test_defaults_and_explicit_page(self):
        self.assertEqual(get_pagination(self.request()), (1, 10))
        self.assertEqual(
            get_pagination(self.request({"page": "2", "limit": "3"})),
            (2, 3),
        )

    def test_rejects_invalid_page_and_limit_values(self):
        for params in (
            {"page": "abc"},
            {"page": "0"},
            {"page": "-1"},
            {"limit": "abc"},
            {"limit": "0"},
            {"limit": "-1"},
            {"limit": "101"},
        ):
            with self.subTest(params=params), self.assertRaises(ValidationError):
                get_pagination(self.request(params))

    def test_slice_and_metadata_include_empty_and_out_of_range_pages(self):
        records = list(range(7))
        self.assertEqual(page_queryset(records, 2, 3), [3, 4, 5])
        self.assertEqual(page_queryset(records, 4, 3), [])
        self.assertEqual(
            pagination_metadata(7, 2, 3),
            {
                "count": 7,
                "page": 2,
                "limit": 3,
                "total_pages": 3,
                "next_page": 3,
                "previous_page": 1,
            },
        )
        self.assertEqual(pagination_metadata(0, 1, 10)["total_pages"], 0)


class ShiftUpdateSerializerTests(SimpleTestCase):
    def setUp(self):
        self.shift = SimpleNamespace(
            name="Day", shift_type="general", start_time=time(9), end_time=time(17),
            grace_minutes=15, is_active=True,
        )

    def test_general_shift_type_and_legacy_basic_input_normalize_to_general(self):
        self.assertEqual(normalize_shift_type("General"), "general")
        self.assertEqual(normalize_shift_type("BASIC"), "general")
        self.assertEqual(normalize_shift_type("Contract"), "contract")

        serializer = ShiftUpdateSerializer(
            instance=self.shift,
            data={
                "shift_name": "Day",
                "shift_type": "Basic",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "shift_grace_time": 15,
                "is_active": True,
            },
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["shift_type"], "general")

    def test_patch_shift_name_only_validates_provided_field(self):
        serializer = ShiftUpdateSerializer(instance=self.shift, data={"shift_name": "  Day A "}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data, {"name": "Day A"})

    def test_patch_grace_time_retains_effective_omitted_fields(self):
        serializer = ShiftUpdateSerializer(instance=self.shift, data={"shift_grace_time": 5}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data, {"grace_minutes": 5})

    def test_rejects_invalid_name_type_and_negative_grace(self):
        for payload in ({"shift_name": "  "}, {"shift_type": "seasonal"}, {"shift_grace_time": -1}):
            with self.subTest(payload=payload):
                serializer = ShiftUpdateSerializer(instance=self.shift, data=payload, partial=True)
                self.assertFalse(serializer.is_valid())


class AttendanceOvertimeCalculationTests(SimpleTestCase):
    plant_timezone = ZoneInfo("Asia/Kolkata")
    attendance_date = date(2026, 10, 15)

    def make_datetime(self, day, hour, minute=0):
        return timezone.make_aware(
            datetime.combine(day, time(hour, minute)),
            self.plant_timezone,
        )

    def make_attendance(self, in_time, out_time):
        return SimpleNamespace(
            employee=SimpleNamespace(company_id="company", plant_id="plant"),
            company_id="company",
            plant_id="plant",
            plant=SimpleNamespace(timezone="Asia/Kolkata"),
            attendance_date=self.attendance_date,
            in_time=in_time,
            out_time=out_time,
            status="absent",
        )

    def make_shift(self, start_time, end_time, is_overnight=False):
        return SimpleNamespace(
            company_id="company",
            plant_id="plant",
            is_active=True,
            is_deleted=False,
            start_time=start_time,
            end_time=end_time,
            grace_minutes=15,
            overtime_after_minutes=480,
            minimum_work_minutes=480,
            is_overnight=is_overnight,
        )

    def calculate_with_shift(self, attendance, shift):
        with patch.object(
            AttendanceService,
            "get_employee_shift",
            return_value=SimpleNamespace(shift=shift),
        ):
            return AttendanceService.calculate_attendance(attendance)

    def test_normal_shift_overtime_is_time_after_scheduled_end(self):
        shift = self.make_shift(time(9), time(18))
        in_time = self.make_datetime(self.attendance_date, 9)

        before_end = self.make_attendance(
            in_time, self.make_datetime(self.attendance_date, 17, 59)
        )
        self.calculate_with_shift(before_end, shift)
        self.assertEqual(before_end.overtime_minutes, 0)

        at_end = self.make_attendance(
            in_time, self.make_datetime(self.attendance_date, 18)
        )
        self.calculate_with_shift(at_end, shift)
        self.assertEqual(at_end.overtime_minutes, 0)

        after_end = self.make_attendance(
            in_time, self.make_datetime(self.attendance_date, 18, 30)
        )
        self.calculate_with_shift(after_end, shift)
        self.assertEqual(after_end.overtime_minutes, 30)

    def test_overnight_shift_uses_next_day_scheduled_end(self):
        shift = self.make_shift(time(21), time(6), is_overnight=True)
        in_time = self.make_datetime(self.attendance_date, 21)
        next_day = self.attendance_date + timedelta(days=1)

        before_end = self.make_attendance(
            in_time, self.make_datetime(next_day, 5, 59)
        )
        self.calculate_with_shift(before_end, shift)
        self.assertEqual(before_end.overtime_minutes, 0)

        at_end = self.make_attendance(
            in_time, self.make_datetime(next_day, 6)
        )
        self.calculate_with_shift(at_end, shift)
        self.assertEqual(at_end.overtime_minutes, 0)

        after_end = self.make_attendance(
            in_time, self.make_datetime(next_day, 6, 45)
        )
        self.calculate_with_shift(after_end, shift)
        self.assertEqual(after_end.overtime_minutes, 45)

    def test_end_time_before_start_time_rolls_scheduled_end_to_next_day(self):
        shift = self.make_shift(time(21), time(6), is_overnight=False)
        attendance = self.make_attendance(
            self.make_datetime(self.attendance_date, 21),
            self.make_datetime(self.attendance_date + timedelta(days=1), 6, 30),
        )

        self.calculate_with_shift(attendance, shift)

        self.assertEqual(attendance.overtime_minutes, 30)

    def test_missing_out_time_and_missing_shift_have_no_overtime(self):
        shift = self.make_shift(time(9), time(18))
        missing_out = self.make_attendance(
            self.make_datetime(self.attendance_date, 9), None
        )
        self.calculate_with_shift(missing_out, shift)
        self.assertEqual(missing_out.overtime_minutes, 0)

        no_shift = self.make_attendance(
            self.make_datetime(self.attendance_date, 9),
            self.make_datetime(self.attendance_date, 20),
        )
        with patch.object(AttendanceService, "get_employee_shift", return_value=None):
            AttendanceService.calculate_attendance(no_shift)
        self.assertEqual(no_shift.overtime_minutes, 0)

    def test_late_grace_and_half_day_threshold_are_unchanged(self):
        shift = self.make_shift(time(9), time(18))
        late_short_day = self.make_attendance(
            self.make_datetime(self.attendance_date, 9, 20),
            self.make_datetime(self.attendance_date, 12, 20),
        )
        self.calculate_with_shift(late_short_day, shift)

        self.assertTrue(late_short_day.is_late)
        self.assertEqual(late_short_day.late_minutes, 5)
        self.assertEqual(late_short_day.status, "half_day")


class AttendanceShiftResolutionTests(SimpleTestCase):
    def setUp(self):
        self.employee = SimpleNamespace(company_id="company", plant_id="plant")
        self.attendance_date = date(2026, 10, 15)

    def queryset(self, result):
        query = MagicMock()
        query.filter.return_value = query
        query.select_related.return_value = query
        query.order_by.return_value = query
        query.first.return_value = result
        return query

    def test_roster_shift_has_priority_over_direct_mapping(self):
        roster_assignment = SimpleNamespace(shift=SimpleNamespace(name="Roster shift"))
        roster_query = self.queryset(roster_assignment)
        direct_query = self.queryset(SimpleNamespace(shift=SimpleNamespace(name="Direct shift")))

        with (
            patch.object(RosterAssignment, "objects") as roster_manager,
            patch.object(EmployeeShift, "objects") as direct_manager,
        ):
            roster_manager.filter.return_value = roster_query
            direct_manager.filter.return_value = direct_query

            result = AttendanceService.get_employee_shift(
                self.employee, self.attendance_date
            )

        self.assertIs(result, roster_assignment)
        direct_manager.filter.assert_not_called()

    def test_direct_shift_is_fallback_when_no_valid_roster_shift(self):
        roster_query = self.queryset(None)
        direct_assignment = SimpleNamespace(shift=SimpleNamespace(name="Direct shift"))
        direct_query = self.queryset(direct_assignment)

        with (
            patch.object(RosterAssignment, "objects") as roster_manager,
            patch.object(EmployeeShift, "objects") as direct_manager,
        ):
            roster_manager.filter.return_value = roster_query
            direct_manager.filter.return_value = direct_query

            result = AttendanceService.get_employee_shift(
                self.employee, self.attendance_date
            )

        self.assertIs(result, direct_assignment)
        self.assertEqual(
            roster_manager.filter.call_args.kwargs["shift__isnull"], False
        )
        self.assertEqual(
            direct_manager.filter.call_args.kwargs["effective_from__lte"],
            self.attendance_date,
        )
