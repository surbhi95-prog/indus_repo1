from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from apps.hrms.models.attendance import Attendance
from apps.hrms.models.attendance_log import AttendanceLog
from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.hrms.services.attendance_service import AttendanceService


class AttendanceShiftField(serializers.Field):

    def __init__(self, shift_attribute, **kwargs):
        self.shift_attribute = shift_attribute
        super().__init__(**kwargs)

    def get_attribute(self, instance):
        # Resolve shift fields from the attendance's employee/date rather than
        # looking for non-existent shift_* attributes on the Attendance model.
        return instance

    def to_internal_value(self, data):
        if not isinstance(data, str) or not data.strip():
            raise serializers.ValidationError("This field must be a non-empty string.")
        if self.shift_attribute == "shift_type":
            return normalize_shift_type(data)
        return data.strip()

    def to_representation(self, obj):
        assignment = AttendanceService.get_employee_shift(
            obj.employee,
            obj.attendance_date,
            company_id=obj.company_id,
            plant_id=obj.plant_id,
        )
        shift = assignment.shift if assignment else None
        if not shift or (
            shift.company_id != obj.company_id
            or shift.plant_id != obj.plant_id
            or not shift.is_active
            or shift.is_deleted
        ):
            return None
        if self.shift_attribute == "shift_time":
            return (
                f"{shift.start_time.strftime('%H:%M')}-"
                f"{shift.end_time.strftime('%H:%M')}"
            )
        return getattr(shift, self.shift_attribute)


class AttendanceLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceLog

        fields = [
            "id",
            "employee",
            "attendance",
            "punch_type",
            "punch_time",
            "source",
            "latitude",
            "longitude",
            "device_id",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class AttendanceSerializer(serializers.ModelSerializer):

    company_id = serializers.PrimaryKeyRelatedField(
        source="company",
        queryset=Company.objects.all(),
        write_only=True,
        required=False,
    )

    plant_id = serializers.PrimaryKeyRelatedField(
        source="plant",
        queryset=Plant.objects.all(),
        write_only=True,
        required=False,
    )

    employee_code = serializers.CharField(
        source="employee.employee_code",
        read_only=True
    )

    punching_code = serializers.SerializerMethodField()

    employee_name = serializers.SerializerMethodField()

    shift_name = AttendanceShiftField("name", required=False)
    shift_id = AttendanceShiftField("id", required=False, read_only=True)
    shift_time = AttendanceShiftField("shift_time", required=False)
    shift_type = AttendanceShiftField("shift_type", required=False)

    logs = AttendanceLogSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Attendance

        fields = [
            "id",
            "company",
            "plant",
            "company_id",
            "plant_id",
            "employee",
            "employee_code",
            "punching_code",
            "employee_name",
            "shift_id",
            "shift_name",
            "shift_time",
            "shift_type",
            "attendance_date",
            "day_type",
            "status",
            "in_time",
            "out_time",
            "total_work_minutes",
            "break_minutes",
            "late_minutes",
            "is_late",
            "late_count",
            "early_leave_minutes",
            "overtime_minutes",
            "source",
            "remarks",
            "logs",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "company": {"required": False},
            "plant": {"required": False},
        }

        read_only_fields = [
            "id",
            "total_work_minutes",
            "break_minutes",
            "late_minutes",
            "is_late",
            "late_count",
            "early_leave_minutes",
            "overtime_minutes",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):

        return (
            f"{obj.employee.first_name} "
            f"{obj.employee.last_name}"
        ).strip()

    def get_punching_code(self, obj):
        statutory = getattr(obj.employee, "statutory", None)
        return statutory.punching_code if statutory else None

    def validate(self, attrs):
        request_data = self.initial_data
        submitted_company = request_data.get("company_id") or request_data.get("company")
        submitted_plant = request_data.get("plant_id") or request_data.get("plant")

        if (
            request_data.get("company_id")
            and request_data.get("company")
            and str(request_data["company_id"]) != str(request_data["company"])
        ):
            raise serializers.ValidationError({
                "company_id": "company and company_id must identify the same company."
            })
        if (
            request_data.get("plant_id")
            and request_data.get("plant")
            and str(request_data["plant_id"]) != str(request_data["plant"])
        ):
            raise serializers.ValidationError({
                "plant_id": "plant and plant_id must identify the same plant."
            })

        if submitted_plant and not submitted_company:
            raise serializers.ValidationError({
                "company_id": "company_id is required when plant_id is provided."
            })

        if submitted_company and submitted_plant:
            company = attrs.get("company") or getattr(self.instance, "company", None)
            plant = attrs.get("plant") or getattr(self.instance, "plant", None)
            if company and plant and plant.company_id != company.id:
                raise serializers.ValidationError({
                    "plant_id": "The selected plant does not belong to the selected company."
                })

        employee = attrs.get("employee") or getattr(self.instance, "employee", None)
        attendance_date = attrs.get("attendance_date") or getattr(
            self.instance, "attendance_date", None
        )
        company = attrs.get("company") or getattr(self.instance, "company", None)
        plant = attrs.get("plant") or getattr(self.instance, "plant", None)
        in_time = attrs.get("in_time", getattr(self.instance, "in_time", None))
        out_time = attrs.get("out_time", getattr(self.instance, "out_time", None))

        if attendance_date and in_time:
            in_date = timezone.localtime(in_time).date() if timezone.is_aware(in_time) else in_time.date()
            if in_date != attendance_date:
                raise serializers.ValidationError({
                    "in_time": "The calendar date of in_time must match attendance_date."
                })

        if attendance_date and out_time:
            out_date = timezone.localtime(out_time).date() if timezone.is_aware(out_time) else out_time.date()
            allowed_out_dates = {attendance_date}
            assignment = AttendanceService.get_employee_shift(
                employee,
                attendance_date,
                company_id=company.id if company else None,
                plant_id=plant.id if plant else None,
            ) if employee else None
            shift = assignment.shift if assignment else None
            if shift and (shift.is_overnight or shift.end_time <= shift.start_time):
                allowed_out_dates.add(attendance_date + timedelta(days=1))
            if out_date not in allowed_out_dates:
                raise serializers.ValidationError({
                    "out_time": "The calendar date of out_time must match attendance_date, except for the next-day out_time of an overnight shift."
                })

        if self.instance is None and not company:
            raise serializers.ValidationError({
                "company_id": "Company is required."
            })
        if self.instance is None and not plant:
            raise serializers.ValidationError({
                "plant_id": "Plant is required."
            })

        if employee and company and employee.company_id != company.id:
            raise serializers.ValidationError({
                "employee": "Employee does not belong to the selected company."
            })
        if employee and plant and employee.plant_id != plant.id:
            raise serializers.ValidationError({
                "employee": "Employee does not belong to the selected plant."
            })

        shift_values = {
            key: request_data.get(key)
            for key in ("shift_name", "shift_type", "shift_time")
        }
        if shift_values["shift_type"] is not None:
            shift_values["shift_type"] = normalize_shift_type(
                shift_values["shift_type"]
            )
        supplied_shift_values = [value is not None for value in shift_values.values()]
        if any(supplied_shift_values):
            if not all(
                isinstance(value, str) and value.strip()
                for value in shift_values.values()
            ):
                raise serializers.ValidationError({
                    "shift": "shift_name, shift_type, and shift_time must be provided together."
                })
            if not company or not plant:
                raise serializers.ValidationError({
                    "shift": "company_id and plant_id are required with shift fields."
                })
            if shift_values["shift_type"] not in dict(
                Shift.SHIFT_TYPE_CHOICES
            ):
                raise serializers.ValidationError({"shift_type": "Invalid shift_type."})

            try:
                start_text, end_text = [
                    part.strip() for part in shift_values["shift_time"].split("-")
                ]
                start_time = datetime.strptime(start_text, "%H:%M").time()
                end_time = datetime.strptime(end_text, "%H:%M").time()
            except (ValueError, TypeError):
                raise serializers.ValidationError({
                    "shift_time": "Use 24-hour HH:MM-HH:MM format."
                })

            assignment = AttendanceService.get_employee_shift(
                employee,
                attendance_date,
                company_id=company.id,
                plant_id=plant.id,
            )
            shift = assignment.shift if assignment else None
            if not shift or (
                shift.company_id != company.id
                or shift.plant_id != plant.id
                or not shift.is_active
                or shift.is_deleted
            ):
                raise serializers.ValidationError({
                    "shift": "Employee has no active shift assignment for this date and company/plant."
                })

            if shift.name.strip().casefold() != shift_values["shift_name"].strip().casefold():
                raise serializers.ValidationError({"shift_name": "Does not match the employee's assigned shift."})
            if shift.shift_type != shift_values["shift_type"]:
                raise serializers.ValidationError({"shift_type": "Does not match the employee's assigned shift."})
            if shift.start_time != start_time or shift.end_time != end_time:
                raise serializers.ValidationError({"shift_time": "Does not match the employee's assigned shift."})

        return attrs

    @staticmethod
    def _discard_shift_request_fields(validated_data):
        for field in ("shift_name", "shift_type", "shift_time"):
            validated_data.pop(field, None)

    @transaction.atomic
    def create(self, validated_data):
        self._discard_shift_request_fields(validated_data)
        if validated_data.get("status") == "weekly_off":
            validated_data["day_type"] = "week_off"
        attendance = super().create(validated_data)
        AttendanceService.recalculate_monthly_late_counts(
            attendance.employee, attendance.attendance_date
        )
        attendance.refresh_from_db()
        return attendance

    @transaction.atomic
    def update(self, instance, validated_data):
        old_employee = instance.employee
        old_date = instance.attendance_date
        self._discard_shift_request_fields(validated_data)
        if validated_data.get("status", instance.status) == "weekly_off":
            validated_data["day_type"] = "week_off"
        attendance = super().update(instance, validated_data)
        AttendanceService.recalculate_monthly_late_counts(old_employee, old_date)
        AttendanceService.recalculate_monthly_late_counts(
            attendance.employee, attendance.attendance_date
        )
        attendance.refresh_from_db()
        return attendance
