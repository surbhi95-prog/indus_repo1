# from datetime import datetime, date, timedelta

# from django.db.models import Q, Count
# from django.utils import timezone

# from rest_framework import status, viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response

# from apps.hrms.models.attendance import Attendance
# from apps.hrms.models.employee import Employee
# from apps.hrms.models.attendance_log import AttendanceLog

# from apps.hrms.serializers.attendance import (
#     AttendanceSerializer,
#     AttendanceLogSerializer,
# )

# from apps.hrms.services.attendance_service import (
#     AttendanceService,
# )


# class AttendanceViewSet(viewsets.ModelViewSet):

#     queryset = (
#         Attendance.objects
#         .select_related(
#             "employee",
#             "company",
#             "plant",
#         )
#         .prefetch_related("logs")
#         .order_by("-attendance_date")
#     )

#     serializer_class = AttendanceSerializer

#     def get_queryset(self):

#         queryset = super().get_queryset()

#         # =====================================================
#         # EXISTING FILTERS
#         # =====================================================

#         employee = self.request.query_params.get(
#             "employee"
#         )

#         employee_code = self.request.query_params.get(
#             "employee_code"
#         )

#         company = self.request.query_params.get(
#             "company"
#         )

#         plant = self.request.query_params.get(
#             "plant"
#         )

#         attendance_date = self.request.query_params.get(
#             "date"
#         )

#         start_date = self.request.query_params.get(
#             "start_date"
#         )

#         end_date = self.request.query_params.get(
#             "end_date"
#         )

#         status_filter = self.request.query_params.get(
#             "status"
#         )

#         source = self.request.query_params.get(
#             "source"
#         )

#         # =====================================================
#         # NEW FILTERS
#         # =====================================================

#         department = self.request.query_params.get(
#             "department"
#         )

#         week = self.request.query_params.get(
#             "week"
#         )

#         month = self.request.query_params.get(
#             "month"
#         )

#         year = self.request.query_params.get(
#             "year"
#         )

#         # =====================================================
#         # EMPLOYEE FILTER
#         # =====================================================

#         if employee:
#             queryset = queryset.filter(
#                 employee_id=employee
#             )

#         # =====================================================
#         # EMPLOYEE CODE FILTER
#         # =====================================================

#         if employee_code:
#             queryset = queryset.filter(
#                 employee__employee_code=employee_code
#             )

#         # =====================================================
#         # COMPANY FILTER
#         # =====================================================

#         if company:
#             queryset = queryset.filter(
#                 company_id=company
#             )

#         # =====================================================
#         # PLANT FILTER
#         # =====================================================

#         if plant:
#             queryset = queryset.filter(
#                 plant_id=plant
#             )

#         # =====================================================
#         # DEPARTMENT FILTER
#         # =====================================================

#         if department:
#             queryset = queryset.filter(
#                 employee__department_id=department
#             )

#         # =====================================================
#         # EXACT DATE FILTER
#         # Example:
#         # ?date=2026-09-17
#         # =====================================================

#         if attendance_date:
#             queryset = queryset.filter(
#                 attendance_date=attendance_date
#             )

#         # =====================================================
#         # WEEK FILTER
#         # Example:
#         # ?week=2026-W38
#         #
#         # ISO week:
#         # Monday -> Sunday
#         # =====================================================

#         if week:

#             try:

#                 week_year, week_number = week.split("-W")

#                 week_year = int(week_year)
#                 week_number = int(week_number)

#                 first_day_of_week = date.fromisocalendar(
#                     week_year,
#                     week_number,
#                     1
#                 )

#                 last_day_of_week = first_day_of_week + timedelta(
#                     days=6
#                 )

#                 queryset = queryset.filter(
#                     attendance_date__range=[
#                         first_day_of_week,
#                         last_day_of_week
#                     ]
#                 )

#             except (ValueError, TypeError):

#                 queryset = queryset.none()

#         # =====================================================
#         # MONTH FILTER
#         #
#         # Example:
#         # ?month=9&year=2026
#         #
#         # Returns:
#         # 2026-09-01 -> 2026-09-30
#         # =====================================================

#         if month:

#             try:

#                 month_number = int(month)

#                 if year:
#                     year_number = int(year)
#                 else:
#                     year_number = date.today().year

#                 if month_number < 1 or month_number > 12:
#                     return queryset.none()

#                 first_day_of_month = date(
#                     year_number,
#                     month_number,
#                     1
#                 )

#                 if month_number == 12:

#                     first_day_of_next_month = date(
#                         year_number + 1,
#                         1,
#                         1
#                     )

#                 else:

#                     first_day_of_next_month = date(
#                         year_number,
#                         month_number + 1,
#                         1
#                     )

#                 last_day_of_month = (
#                     first_day_of_next_month -
#                     timedelta(days=1)
#                 )

#                 queryset = queryset.filter(
#                     attendance_date__range=[
#                         first_day_of_month,
#                         last_day_of_month
#                     ]
#                 )

#             except (ValueError, TypeError):

#                 queryset = queryset.none()

#         # =====================================================
#         # YEAR FILTER
#         #
#         # Example:
#         # ?year=2026
#         #
#         # Returns:
#         # 2026-01-01 -> 2026-12-31
#         # =====================================================

#         if year and not month:

#             try:

#                 year_number = int(year)

#                 first_day_of_year = date(
#                     year_number,
#                     1,
#                     1
#                 )

#                 last_day_of_year = date(
#                     year_number,
#                     12,
#                     31
#                 )

#                 queryset = queryset.filter(
#                     attendance_date__range=[
#                         first_day_of_year,
#                         last_day_of_year
#                     ]
#                 )

#             except (ValueError, TypeError):

#                 queryset = queryset.none()

#         # =====================================================
#         # CUSTOM DATE RANGE
#         #
#         # Example:
#         # ?start_date=2026-09-01&end_date=2026-09-15
#         # =====================================================

#         if start_date:
#             queryset = queryset.filter(
#                 attendance_date__gte=start_date
#             )

#         if end_date:
#             queryset = queryset.filter(
#                 attendance_date__lte=end_date
#             )

#         # =====================================================
#         # STATUS FILTER
#         # =====================================================

#         if status_filter:
#             queryset = queryset.filter(
#                 status=status_filter
#             )

#         # =====================================================
#         # SOURCE FILTER
#         # =====================================================

#         if source:
#             queryset = queryset.filter(
#                 source=source
#             )

#         return queryset
#         # =========================================================
#     # ATTENDANCE LIST WITH SUMMARY COUNTS
#     # =========================================================

#         def list(self, request, *args, **kwargs):

#             queryset = self.get_queryset()

#             data = AttendanceSerializer(
#             queryset,
#             many=True
#         ).data

#             summary = {
#             "total": queryset.count(),

#             "present": queryset.filter(
#                 status="present"
#             ).count(),

#             "absent": queryset.filter(
#                 status="absent"
#             ).count(),

#             "half_day": queryset.filter(
#                 status="half_day"
#             ).count(),

#             "leave": queryset.filter(
#                 status="leave"
#             ).count(),

#             "holiday": queryset.filter(
#                 status="holiday"
#             ).count(),

#             "weekly_off": queryset.filter(
#                 status="weekly_off"
#             ).count(),

#             "work_from_home": queryset.filter(
#                 status="work_from_home"
#             ).count(),

#             "total_overtime_minutes": sum(
#                 queryset.values_list(
#                     "overtime_minutes",
#                     flat=True
#                 )
#             ),

#             "employee_summary": [],
#         }
#         # =====================================================
#         # EMPLOYEE-WISE ATTENDANCE SUMMARY
#         # =====================================================

#         employee_summary = (
#             queryset
#             .values(
#                 "employee_id",
#                 "employee__employee_code",
#                 "employee__first_name",
#                 "employee__last_name",
#             )
#             .annotate(
#                 total=Count("id"),

#                 present=Count(
#                     "id",
#                     filter=Q(status="present")
#                 ),

#                 absent=Count(
#                     "id",
#                     filter=Q(status="absent")
#                 ),

#                 half_day=Count(
#                     "id",
#                     filter=Q(status="half_day")
#                 ),

#                 leave=Count(
#                     "id",
#                     filter=Q(status="leave")
#                 ),

#                 holiday=Count(
#                     "id",
#                     filter=Q(status="holiday")
#                 ),

#                 weekly_off=Count(
#                     "id",
#                     filter=Q(status="weekly_off")
#                 ),

#                 work_from_home=Count(
#                     "id",
#                     filter=Q(status="work_from_home")
#                 ),
#             )
#             .order_by(
#                 "employee__employee_code"
#             )
#         )

#         # =====================================================
#         # FORMAT EMPLOYEE SUMMARY
#         # =====================================================

#         for employee in employee_summary:

#             first_name = (
#                 employee["employee__first_name"]
#                 or ""
#             )

#             last_name = (
#                 employee["employee__last_name"]
#                 or ""
#             )

#             employee_name = (
#                 f"{first_name} {last_name}"
#             ).strip()

#             summary["employee_summary"].append(
#                 {
#                     "employee_id": str(
#                         employee["employee_id"]
#                     ),

#                     "employee_code": (
#                         employee[
#                             "employee__employee_code"
#                         ]
#                     ),

#                     "employee_name": employee_name,

#                     "total": employee["total"],

#                     "present": employee["present"],

#                     "absent": employee["absent"],

#                     "half_day": employee["half_day"],

#                     "leave": employee["leave"],

#                     "holiday": employee["holiday"],

#                     "weekly_off": employee["weekly_off"],

#                     "work_from_home": (
#                         employee["work_from_home"]
#                     ),
#                 }
#             )

#         return Response(
#             {
#                 "success": True,
#                 "summary": summary,
#                 "count": queryset.count(),
#                 "data": data,
#             }
#         )
#         return Response(
#             {
#                 "success": True,
#                 "summary": summary,
#                 "count": queryset.count(),
#                 "data": data,
#             }
#         )
#     # =========================================================
#     # CHECK-IN API
#     # =========================================================

#     @action(
#         detail=False,
#         methods=["post"],
#         url_path="check-in"
#     )
#     def in_time(self, request):

#         employee_id = request.data.get(
#             "employee"
#         )

#         if not employee_id:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "Employee is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:

#             employee = Employee.objects.get(
#                 id=employee_id,
#                 status="active"
#             )

#         except Employee.DoesNotExist:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "Active employee not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         now = datetime.now().astimezone()

#         attendance = AttendanceService.add_punch(
#             employee=employee,
#             punch_time=now,
#             punch_type="in_time",
#             source="manual"
#         )

#         return Response(
#             {
#                 "success": True,
#                 "message": "Check-in recorded successfully.",
#                 "data": AttendanceSerializer(
#                     attendance
#                 ).data
#             },
#             status=status.HTTP_201_CREATED
#         )

#     # =========================================================
#     # CHECK-OUT API
#     # =========================================================

#     @action(
#         detail=False,
#         methods=["post"],
#         url_path="check-out"
#     )
#     def out_time(self, request):

#         employee_id = request.data.get(
#             "employee"
#         )

#         if not employee_id:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "Employee is required."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:

#             employee = Employee.objects.get(
#                 id=employee_id,
#                 status="active"
#             )

#         except Employee.DoesNotExist:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "Active employee not found."
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         now = datetime.now().astimezone()

#         attendance = AttendanceService.add_punch(
#             employee=employee,
#             punch_time=now,
#             punch_type="out_time",
#             source="manual"
#         )

#         return Response(
#             {
#                 "success": True,
#                 "message": "Check-out recorded successfully.",
#                 "data": AttendanceSerializer(
#                     attendance
#                 ).data
#             }
#         )

#     # =========================================================
#     # EXISTING SUMMARY API
#     # =========================================================

#     @action(
#         detail=False,
#         methods=["get"],
#         url_path="summary"
#     )
#     def summary(self, request):

#         queryset = self.get_queryset()

#         data = {
#             "total": queryset.count(),

#             "present": queryset.filter(
#                 status="present"
#             ).count(),

#             "absent": queryset.filter(
#                 status="absent"
#             ).count(),

#             "half_day": queryset.filter(
#                 status="half_day"
#             ).count(),

#             "leave": queryset.filter(
#                 status="leave"
#             ).count(),

#             "holiday": queryset.filter(
#                 status="holiday"
#             ).count(),

#             "weekly_off": queryset.filter(
#                 status="weekly_off"
#             ).count(),

#             "work_from_home": queryset.filter(
#                 status="work_from_home"
#             ).count(),

#             "total_overtime_minutes": sum(
#                 queryset.values_list(
#                     "overtime_minutes",
#                     flat=True
#                 )
#             ),
#         }

#         return Response(
#             {
#                 "success": True,
#                 "data": data
#             }
#         )

#     # =========================================================
#     # NEW DAILY ATTENDANCE SUMMARY API
#     #
#     # GET:
#     # /api/hrms/attendance/today-summary/
#     #
#     # Returns today's:
#     # Total
#     # Present
#     # Absent
#     # Half Day
#     # Leave
#     # Overtime
#     # =========================================================

#     @action(
#         detail=False,
#         methods=["get"],
#         url_path="today-summary"
#     )
#     def today_summary(self, request):

#         # Get current date according to
#         # Django application timezone
#         today = timezone.localdate()

#         # Get only today's attendance records
#         queryset = Attendance.objects.filter(
#             attendance_date=today
#         )

#         # -----------------------------------------------------
#         # TOTAL
#         # -----------------------------------------------------

#         total = queryset.count()

#         # -----------------------------------------------------
#         # PRESENT
#         # -----------------------------------------------------

#         present = queryset.filter(
#             status="present"
#         ).count()

#         # -----------------------------------------------------
#         # ABSENT
#         # -----------------------------------------------------

#         absent = queryset.filter(
#             status="absent"
#         ).count()

#         # -----------------------------------------------------
#         # HALF DAY
#         #
#         # Half day is counted from the status already
#         # calculated and saved by AttendanceService/import.
#         # -----------------------------------------------------

#         half_day = queryset.filter(
#             status="half_day"
#         ).count()

#         # -----------------------------------------------------
#         # LEAVE
#         # -----------------------------------------------------

#         leave = queryset.filter(
#             status="leave"
#         ).count()

#         # -----------------------------------------------------
#         # OVERTIME
#         #
#         # Count employees/attendance records having
#         # overtime greater than 0 minutes.
#         # -----------------------------------------------------

#         overtime = queryset.filter(
#             overtime_minutes__gt=0
#         ).count()

#         # -----------------------------------------------------
#         # RESPONSE
#         # -----------------------------------------------------

#         return Response(
#             {
#                 "success": True,
#                 "date": today,
#                 "data": {
#                     "total": total,
#                     "present": present,
#                     "absent": absent,
#                     "half_day": half_day,
#                     "leave": leave,
#                     "overtime": overtime,
#                 }
#             },
#             status=status.HTTP_200_OK
#         )


# class AttendanceLogViewSet(viewsets.ReadOnlyModelViewSet):

#     queryset = (
#         AttendanceLog.objects
#         .select_related(
#             "employee",
#             "attendance"
#         )
#         .order_by("-punch_time")
#     )

#     serializer_class = AttendanceLogSerializer

#     def get_queryset(self):

#         queryset = super().get_queryset()

#         employee = self.request.query_params.get(
#             "employee"
#         )

#         source = self.request.query_params.get(
#             "source"
#         )

#         punch_type = self.request.query_params.get(
#             "punch_type"
#         )

#         if employee:
#             queryset = queryset.filter(
#                 employee_id=employee
#             )

#         if source:
#             queryset = queryset.filter(
#                 source=source
#             )

#         if punch_type:
#             queryset = queryset.filter(
#                 punch_type=punch_type
#             )

#         return queryset
from datetime import datetime, date, timedelta
from uuid import UUID

from django.db import transaction
from django.db.models import Q, Count, OuterRef, Subquery
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.hrms.models.attendance import Attendance
from apps.hrms.models.employee import Employee
from apps.hrms.models.attendance_log import AttendanceLog
from apps.hrms.models.employee_shift import EmployeeShift
from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type
from apps.masters.models.plant import Plant

from apps.hrms.serializers.attendance import (
    AttendanceSerializer,
    AttendanceLogSerializer,
)

from apps.hrms.services.attendance_service import (
    AttendanceService,
)


class AttendanceViewSet(viewsets.ModelViewSet):

    queryset = (
        Attendance.objects
        .select_related(
            "employee",
            "employee__statutory",
            "company",
            "plant",
        )
        .prefetch_related("logs")
        .order_by("-created_at", "-attendance_date")
    )

    serializer_class = AttendanceSerializer

    @transaction.atomic
    def perform_destroy(self, instance):
        employee = instance.employee
        attendance_date = instance.attendance_date
        instance.delete()
        AttendanceService.recalculate_monthly_late_counts(
            employee,
            attendance_date,
        )

    def get_queryset(self):

        queryset = super().get_queryset()

        # =====================================================
        # EXISTING FILTERS
        # =====================================================

        employee = self.request.query_params.get(
            "employee"
        )

        employee_code = self.request.query_params.get(
            "employee_code"
        )

        company = (
            self.request.query_params.get("company")
            or self.request.query_params.get("company_id")
        )

        plant = (
            self.request.query_params.get("plant")
            or self.request.query_params.get("plant_id")
        )

        if plant and not company:
            raise ValidationError({
                "company": "company is required when filtering by plant."
            })

        if company and plant:
            try:
                company_id = UUID(company)
                plant_id = UUID(plant)
            except (ValueError, TypeError, AttributeError):
                raise ValidationError({
                    "company": "Provide valid company and plant IDs."
                })

            if not Plant.objects.filter(
                id=plant_id,
                company_id=company_id,
            ).exists():
                raise ValidationError({
                    "plant": "This plant does not belong to the selected company."
                })

        attendance_date = self.request.query_params.get(
            "date"
        )

        start_date = self.request.query_params.get(
            "start_date"
        )

        end_date = self.request.query_params.get(
            "end_date"
        )

        status_filter = self.request.query_params.get(
            "status"
        )

        source = self.request.query_params.get(
            "source"
        )

        shift_type = self.request.query_params.get("shift_type")
        if shift_type is not None:
            shift_type = normalize_shift_type(shift_type)
        shift_id = self.request.query_params.get("shift_id")
        shift_name = self.request.query_params.get("shift_name")
        shift_time = self.request.query_params.get("shift_time")

        legacy_shift_filters = (shift_name, shift_time)
        if any(value is not None for value in legacy_shift_filters):
            if not all(
                value and value.strip()
                for value in (shift_type, shift_name, shift_time)
            ):
                raise ValidationError({
                    "shift": "shift_type, shift_name, and shift_time must be provided together."
                })

        shift_filter_requested = any(
            value is not None
            for value in (shift_id, shift_type, shift_name, shift_time)
        )
        if shift_filter_requested:
            if shift_type is not None and (
                not shift_type
                or shift_type not in dict(Shift.SHIFT_TYPE_CHOICES)
            ):
                raise ValidationError({"shift_type": "Invalid shift_type. Choose a valid shift type."})

            selected_shift = None
            if shift_id is not None:
                try:
                    parsed_shift_id = UUID(shift_id)
                except (ValueError, TypeError, AttributeError):
                    raise ValidationError({"shift_id": "Provide a valid shift UUID."})
                try:
                    selected_shift = Shift.objects.get(id=parsed_shift_id)
                except Shift.DoesNotExist:
                    raise ValidationError({"shift_id": "Shift does not exist."})

                if company:
                    try:
                        requested_company_id = UUID(company)
                    except (ValueError, TypeError, AttributeError):
                        raise ValidationError({"company": "Provide a valid company ID."})
                    if selected_shift.company_id != requested_company_id:
                        raise ValidationError({"shift_id": "Shift does not belong to the selected company."})
                if plant:
                    try:
                        requested_plant_id = UUID(plant)
                    except (ValueError, TypeError, AttributeError):
                        raise ValidationError({"plant": "Provide a valid plant ID."})
                    if selected_shift.plant_id != requested_plant_id:
                        raise ValidationError({"shift_id": "Shift does not belong to the selected plant."})

            if not company or not plant:
                if shift_name is not None or shift_time is not None:
                    raise ValidationError({
                        "shift": "company and plant are required when filtering by shift name or time."
                    })

            if shift_name is not None or shift_time is not None:
                try:
                    company_id = UUID(company)
                    plant_id = UUID(plant)
                except (ValueError, TypeError, AttributeError):
                    raise ValidationError({
                        "company": "Valid company and plant IDs are required for shift filters."
                    })
                try:
                    start_text, end_text = [part.strip() for part in shift_time.split("-")]
                    shift_start = datetime.strptime(start_text, "%H:%M").time()
                    shift_end = datetime.strptime(end_text, "%H:%M").time()
                except (ValueError, TypeError):
                    raise ValidationError({
                        "shift_time": "Use 24-hour HH:MM-HH:MM format."
                    })

                matching_shift = Shift.objects.filter(
                    company_id=company_id,
                    plant_id=plant_id,
                    shift_type=shift_type,
                    name__iexact=shift_name.strip(),
                    start_time=shift_start,
                    end_time=shift_end,
                    is_active=True,
                    is_deleted=False,
                )
                if not matching_shift.exists():
                    raise ValidationError({
                        "shift": "No active shift with these values exists for the selected company and plant."
                    })

            assignments = EmployeeShift.objects.filter(
                employee_id=OuterRef("employee_id"),
                effective_from__lte=OuterRef("attendance_date"),
                is_active=True,
                shift__is_active=True,
                shift__is_deleted=False,
                shift__company_id=OuterRef("company_id"),
                shift__plant_id=OuterRef("plant_id"),
            ).filter(
                Q(effective_to__isnull=True)
                | Q(effective_to__gte=OuterRef("attendance_date"))
            ).order_by("-effective_from")
            queryset = queryset.annotate(
                assigned_shift_id=Subquery(assignments.values("shift_id")[:1])
            )
            if shift_id is not None:
                queryset = queryset.filter(assigned_shift_id=parsed_shift_id)
            if shift_type is not None:
                queryset = queryset.filter(
                    assigned_shift_id__in=Shift.objects.filter(
                        shift_type=shift_type,
                        is_active=True,
                        is_deleted=False,
                    ).values("id")
                )
            if shift_name is not None or shift_time is not None:
                queryset = queryset.filter(
                    assigned_shift_id__in=matching_shift.values("id")
                )

        # =====================================================
        # NEW FILTERS
        # =====================================================

        department = self.request.query_params.get(
            "department"
        )

        week = self.request.query_params.get(
            "week"
        )

        month = self.request.query_params.get(
            "month"
        )

        year = self.request.query_params.get(
            "year"
        )

        # =====================================================
        # EMPLOYEE FILTER
        # =====================================================

        if employee:
            queryset = queryset.filter(
                employee_id=employee
            )

        # =====================================================
        # EMPLOYEE CODE FILTER
        # =====================================================

        if employee_code:
            queryset = queryset.filter(
                employee__employee_code=employee_code
            )

        # =====================================================
        # COMPANY FILTER
        # =====================================================

        if company:
            queryset = queryset.filter(
                company_id=company
            )

        # =====================================================
        # PLANT FILTER
        # =====================================================

        if plant:
            queryset = queryset.filter(
                plant_id=plant
            )

        # =====================================================
        # DEPARTMENT FILTER
        # =====================================================

        if department:
            queryset = queryset.filter(
                employee__department_id=department
            )

        # =====================================================
        # EXACT DATE FILTER
        # Example:
        # ?date=2026-09-17
        # =====================================================

        if attendance_date:
            queryset = queryset.filter(
                attendance_date=attendance_date
            )

        # =====================================================
        # WEEK FILTER
        # Example:
        # ?week=2026-W38
        #
        # ISO week:
        # Monday -> Sunday
        # =====================================================

        if week:

            try:

                week_year, week_number = week.split("-W")

                week_year = int(week_year)
                week_number = int(week_number)

                first_day_of_week = date.fromisocalendar(
                    week_year,
                    week_number,
                    1
                )

                last_day_of_week = first_day_of_week + timedelta(
                    days=6
                )

                queryset = queryset.filter(
                    attendance_date__range=[
                        first_day_of_week,
                        last_day_of_week
                    ]
                )

            except (ValueError, TypeError):

                queryset = queryset.none()

        # =====================================================
        # MONTH FILTER
        #
        # Example:
        # ?month=9&year=2026
        #
        # Returns:
        # 2026-09-01 -> 2026-09-30
        # =====================================================

        if month:

            try:

                month_number = int(month)

                if year:
                    year_number = int(year)
                else:
                    year_number = date.today().year

                if month_number < 1 or month_number > 12:
                    return queryset.none()

                first_day_of_month = date(
                    year_number,
                    month_number,
                    1
                )

                if month_number == 12:

                    first_day_of_next_month = date(
                        year_number + 1,
                        1,
                        1
                    )

                else:

                    first_day_of_next_month = date(
                        year_number,
                        month_number + 1,
                        1
                    )

                last_day_of_month = (
                    first_day_of_next_month -
                    timedelta(days=1)
                )

                queryset = queryset.filter(
                    attendance_date__range=[
                        first_day_of_month,
                        last_day_of_month
                    ]
                )

            except (ValueError, TypeError):

                queryset = queryset.none()

        # =====================================================
        # YEAR FILTER
        #
        # Example:
        # ?year=2026
        #
        # Returns:
        # 2026-01-01 -> 2026-12-31
        # =====================================================

        if year and not month:

            try:

                year_number = int(year)

                first_day_of_year = date(
                    year_number,
                    1,
                    1
                )

                last_day_of_year = date(
                    year_number,
                    12,
                    31
                )

                queryset = queryset.filter(
                    attendance_date__range=[
                        first_day_of_year,
                        last_day_of_year
                    ]
                )

            except (ValueError, TypeError):

                queryset = queryset.none()

        # =====================================================
        # CUSTOM DATE RANGE
        #
        # Example:
        # ?start_date=2026-09-01&end_date=2026-09-15
        # =====================================================

        if start_date:
            queryset = queryset.filter(
                attendance_date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                attendance_date__lte=end_date
            )

        # =====================================================
        # STATUS FILTER
        # =====================================================

        if status_filter:
            queryset = queryset.filter(
                status=status_filter
            )

        # =====================================================
        # SOURCE FILTER
        # =====================================================

        if source:
            queryset = queryset.filter(
                source=source
            )

        return queryset

    # =========================================================
    # ATTENDANCE LIST WITH SUMMARY COUNTS
    # =========================================================

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        data = AttendanceSerializer(
            queryset,
            many=True
        ).data

        summary = {
            "total": queryset.count(),
            "present": queryset.filter(status="present").count(),
            "absent": queryset.filter(status="absent").count(),
            "half_day": queryset.filter(status="half_day").count(),
            "leave": queryset.filter(status="leave").count(),
            "holiday": queryset.filter(status="holiday").count(),
            "weekly_off": queryset.filter(status="weekly_off").count(),
            "work_from_home": queryset.filter(status="work_from_home").count(),
            "total_overtime_minutes": sum(
                value or 0 for value in queryset.values_list(
                    "overtime_minutes", flat=True
                )
            ),
            "employee_summary": [],
        }

        # =====================================================
        # EMPLOYEE-WISE ATTENDANCE SUMMARY
        # =====================================================

        employee_summary = (
            queryset
            .values(
                "employee_id",
                "employee__employee_code",
                "employee__first_name",
                "employee__last_name",
                "employee__statutory__punching_code",
            )
            .annotate(
                total=Count("id"),
                present=Count("id", filter=Q(status="present")),
                absent=Count("id", filter=Q(status="absent")),
                half_day=Count("id", filter=Q(status="half_day")),
                leave=Count("id", filter=Q(status="leave")),
                holiday=Count("id", filter=Q(status="holiday")),
                weekly_off=Count("id", filter=Q(status="weekly_off")),
                work_from_home=Count("id", filter=Q(status="work_from_home")),
            )
            .order_by("employee__employee_code")
        )

        late_dates_by_employee = {}
        for employee_id, attendance_date in queryset.filter(
            is_late=True
        ).order_by("attendance_date", "id").values_list(
            "employee_id", "attendance_date"
        ):
            late_dates_by_employee.setdefault(employee_id, []).append(
                attendance_date
            )

        for employee in employee_summary:
            first_name = employee["employee__first_name"] or ""
            last_name = employee["employee__last_name"] or ""
            employee_name = f"{first_name} {last_name}".strip()

            late_dates = late_dates_by_employee.get(
                employee["employee_id"], []
            )

            summary["employee_summary"].append(
                {
                    "employee_id": str(employee["employee_id"]),
                    "employee_code": employee["employee__employee_code"],
                    "punching_code": employee[
                        "employee__statutory__punching_code"
                    ],
                    "employee_name": employee_name,
                    "total": employee["total"],
                    "present": employee["present"],
                    "absent": employee["absent"],
                    "half_day": employee["half_day"],
                    "leave": employee["leave"],
                    "holiday": employee["holiday"],
                    "weekly_off": employee["weekly_off"],
                    "work_from_home": employee["work_from_home"],
                    "late_count": len(late_dates),
                    "late_dates": late_dates,
                }
            )

        return Response(
            {
                "success": True,
                "summary": summary,
                "count": queryset.count(),
                "data": data,
            }
        )
    # =========================================================
    # CHECK-IN API
    # =========================================================

    @action(
        detail=False,
        methods=["post"],
        url_path="check-in"
    )
    def in_time(self, request):

        employee_id = request.data.get(
            "employee"
        )

        if not employee_id:

            return Response(
                {
                    "success": False,
                    "message": "Employee is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            employee = Employee.objects.get(
                id=employee_id,
                status="active"
            )

        except Employee.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Active employee not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        now = datetime.now().astimezone()

        attendance = AttendanceService.add_punch(
            employee=employee,
            punch_time=now,
            punch_type="in_time",
            source="manual"
        )

        return Response(
            {
                "success": True,
                "message": "Check-in recorded successfully.",
                "data": AttendanceSerializer(
                    attendance
                ).data
            },
            status=status.HTTP_201_CREATED
        )

    # =========================================================
    # CHECK-OUT API
    # =========================================================

    @action(
        detail=False,
        methods=["post"],
        url_path="check-out"
    )
    def out_time(self, request):

        employee_id = request.data.get(
            "employee"
        )

        if not employee_id:

            return Response(
                {
                    "success": False,
                    "message": "Employee is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            employee = Employee.objects.get(
                id=employee_id,
                status="active"
            )

        except Employee.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Active employee not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        now = datetime.now().astimezone()

        attendance = AttendanceService.add_punch(
            employee=employee,
            punch_time=now,
            punch_type="out_time",
            source="manual"
        )

        return Response(
            {
                "success": True,
                "message": "Check-out recorded successfully.",
                "data": AttendanceSerializer(
                    attendance
                ).data
            }
        )

    # =========================================================
    # EXISTING SUMMARY API
    # =========================================================

    @action(
        detail=False,
        methods=["get"],
        url_path="summary"
    )
    def summary(self, request):

        queryset = self.get_queryset()

        data = {
            "total": queryset.count(),

            "present": queryset.filter(
                status="present"
            ).count(),

            "absent": queryset.filter(
                status="absent"
            ).count(),

            "half_day": queryset.filter(
                status="half_day"
            ).count(),

            "leave": queryset.filter(
                status="leave"
            ).count(),

            "holiday": queryset.filter(
                status="holiday"
            ).count(),

            "weekly_off": queryset.filter(
                status="weekly_off"
            ).count(),

            "work_from_home": queryset.filter(
                status="work_from_home"
            ).count(),

            "total_overtime_minutes": sum(
                queryset.values_list(
                    "overtime_minutes",
                    flat=True
                )
            ),
        }

        return Response(
            {
                "success": True,
                "data": data
            }
        )

    # =========================================================
    # NEW DAILY ATTENDANCE SUMMARY API
    #
    # GET:
    # /api/hrms/attendance/today-summary/
    #
    # Returns today's:
    # Total
    # Present
    # Absent
    # Half Day
    # Leave
    # Overtime
    # =========================================================

    @action(
        detail=False,
        methods=["get"],
        url_path="today-summary"
    )
    def today_summary(self, request):

        # Get current date according to
        # Django application timezone
        today = timezone.localdate()

        # Get only today's attendance records
        queryset = Attendance.objects.filter(
            attendance_date=today
        )

        # -----------------------------------------------------
        # TOTAL
        # -----------------------------------------------------

        total = queryset.count()

        # -----------------------------------------------------
        # PRESENT
        # -----------------------------------------------------

        present = queryset.filter(
            status="present"
        ).count()

        # -----------------------------------------------------
        # ABSENT
        # -----------------------------------------------------

        absent = queryset.filter(
            status="absent"
        ).count()

        # -----------------------------------------------------
        # HALF DAY
        #
        # Half day is counted from the status already
        # calculated and saved by AttendanceService/import.
        # -----------------------------------------------------

        half_day = queryset.filter(
            status="half_day"
        ).count()

        # -----------------------------------------------------
        # LEAVE
        # -----------------------------------------------------

        leave = queryset.filter(
            status="leave"
        ).count()

        # -----------------------------------------------------
        # OVERTIME
        #
        # Count employees/attendance records having
        # overtime greater than 0 minutes.
        # -----------------------------------------------------

        overtime = queryset.filter(
            overtime_minutes__gt=0
        ).count()

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        return Response(
            {
                "success": True,
                "date": today,
                "data": {
                    "total": total,
                    "present": present,
                    "absent": absent,
                    "half_day": half_day,
                    "leave": leave,
                    "overtime": overtime,
                }
            },
            status=status.HTTP_200_OK
        )


class AttendanceLogViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = (
        AttendanceLog.objects
        .select_related(
            "employee",
            "attendance"
        )
        .order_by("-punch_time")
    )

    serializer_class = AttendanceLogSerializer

    def get_queryset(self):

        queryset = super().get_queryset()

        employee = self.request.query_params.get(
            "employee"
        )

        source = self.request.query_params.get(
            "source"
        )

        punch_type = self.request.query_params.get(
            "punch_type"
        )

        if employee:
            queryset = queryset.filter(
                employee_id=employee
            )

        if source:
            queryset = queryset.filter(
                source=source
            )

        if punch_type:
            queryset = queryset.filter(
                punch_type=punch_type
            )

        return queryset
