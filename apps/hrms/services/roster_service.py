from datetime import time, timedelta
from uuid import UUID

from django.db import transaction
from django.db.models import Count, Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.hrms.models.employee import Employee
from apps.hrms.models.employee_shift import EmployeeShift
from apps.hrms.models.roster import Roster, RosterAssignment
from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type


def _actor_name(user):
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    return full_name or user.email or str(user.pk)


class RosterService:
    @staticmethod
    def _employee_display(employee):
        name = f"{employee.first_name or ''} {employee.last_name or ''}".strip()
        return f"{name} - {employee.employee_code}"

    @staticmethod
    def active_rosters():
        return Roster.objects.filter(is_deleted=False).annotate(
            total_employees=Count("assignments__employee_id", filter=Q(assignments__is_deleted=False), distinct=True)
        ).select_related("company", "plant", "department").order_by("-created_at")

    @staticmethod
    def _request_date(value, field):
        try:
            return serializers.DateField().run_validation(value)
        except ValidationError as exc:
            raise ValidationError({field: exc.detail})

    @staticmethod
    def _uuid(value, field):
        try:
            return UUID(str(value))
        except (ValueError, TypeError, AttributeError):
            raise ValidationError({field: "Enter a valid UUID."})

    @staticmethod
    @transaction.atomic
    def generate_assignments(roster, payload, user):
        employee_ids = payload.get("employee_ids")
        if not isinstance(employee_ids, list) or not employee_ids:
            raise ValidationError({"employee_ids": "Provide a non-empty list of employee UUIDs."})
        parsed_employee_ids = [RosterService._uuid(value, "employee_ids") for value in employee_ids]
        if len(set(parsed_employee_ids)) != len(parsed_employee_ids):
            raise ValidationError({"employee_ids": "Duplicate employee IDs are not allowed."})

        start_date = RosterService._request_date(payload.get("start_date"), "start_date")
        end_date = RosterService._request_date(payload.get("end_date"), "end_date")
        if start_date > end_date:
            raise ValidationError({"end_date": "end_date must be on or after start_date."})
        if start_date < roster.start_date or end_date > roster.end_date:
            raise ValidationError({"start_date": "Request dates must be inside the roster date range."})

        requested_shift_type = payload.get("shift_type")
        if requested_shift_type is not None:
            requested_shift_type = normalize_shift_type(requested_shift_type)
            allowed_types = {choice[0] for choice in Shift.SHIFT_TYPE_CHOICES}
            if requested_shift_type not in allowed_types:
                raise ValidationError({"shift_type": f"Use one of: {', '.join(sorted(allowed_types))}."})

        employees = list(Employee.objects.filter(
            id__in=parsed_employee_ids,
            company_id=roster.company_id,
            plant_id=roster.plant_id,
        ).select_related("department"))
        employee_by_id = {employee.id: employee for employee in employees}
        missing = [str(item) for item in parsed_employee_ids if item not in employee_by_id]
        if missing:
            raise ValidationError({"employee_ids": f"Employees not found in this roster's company and plant: {', '.join(missing)}."})
        if roster.department_id:
            wrong_department = [str(item) for item in parsed_employee_ids if employee_by_id[item].department_id != roster.department_id]
            if wrong_department:
                raise ValidationError({"employee_ids": "Every employee must belong to the roster department."})

        schedule = payload.get("schedule")
        if not isinstance(schedule, list) or not schedule:
            raise ValidationError({"schedule": "Provide a non-empty schedule."})
        parsed_schedule = []
        allowed_day_types = {choice[0] for choice in RosterAssignment.DAY_TYPE_CHOICES}
        for index, item in enumerate(schedule):
            if not isinstance(item, dict):
                raise ValidationError({"schedule": f"Schedule item {index + 1} must be an object."})
            item_start = RosterService._request_date(item.get("start_date"), f"schedule.{index}.start_date")
            item_end = RosterService._request_date(item.get("end_date"), f"schedule.{index}.end_date")
            if item_start > item_end or item_start < start_date or item_end > end_date:
                raise ValidationError({"schedule": f"Schedule item {index + 1} has dates outside the request range."})
            day_type = str(item.get("day_type", "WORKING_DAY")).strip().upper()
            if day_type not in allowed_day_types:
                raise ValidationError({"schedule": f"Invalid day_type in schedule item {index + 1}."})

            shift = None
            raw_shift_id = item.get("shift_id")
            if day_type == "WORKING_DAY":
                if raw_shift_id in (None, ""):
                    raise ValidationError({"schedule": f"shift_id is required for working schedule item {index + 1}."})
                shift_id = RosterService._uuid(raw_shift_id, f"schedule.{index}.shift_id")
                shift = Shift.objects.filter(id=shift_id, is_deleted=False, is_active=True).first()
                if not shift:
                    raise ValidationError({"schedule": f"Shift in schedule item {index + 1} was not found or is inactive."})
                if shift.company_id != roster.company_id or shift.plant_id != roster.plant_id:
                    raise ValidationError({"schedule": f"Shift in schedule item {index + 1} is outside the roster company and plant."})
                if not requested_shift_type:
                    raise ValidationError({"shift_type": "shift_type is required when assigning working days."})
                if shift.shift_type.lower() != requested_shift_type:
                    raise ValidationError({"schedule": f"Shift in schedule item {index + 1} does not match shift_type."})
            elif raw_shift_id not in (None, ""):
                raise ValidationError({"schedule": f"shift_id must be null for non-working schedule item {index + 1}."})
            elif "day_type" not in item:
                raise ValidationError({"schedule": f"day_type is required for non-working schedule item {index + 1}."})

            parsed_schedule.append((item_start, item_end, shift, day_type))

        parsed_schedule.sort(key=lambda row: row[0])
        next_date = start_date
        for item_start, item_end, _shift, _day_type in parsed_schedule:
            if item_start < next_date:
                raise ValidationError({"schedule": "Schedule ranges must not overlap."})
            if item_start > next_date:
                raise ValidationError({"schedule": "Schedule ranges must cover every date without gaps."})
            next_date = item_end + timedelta(days=1)
        if next_date != end_date + timedelta(days=1):
            raise ValidationError({"schedule": "Schedule ranges must cover every date without gaps."})

        dates = []
        for item_start, item_end, shift, day_type in parsed_schedule:
            current = item_start
            while current <= item_end:
                dates.append((current, shift, day_type))
                current += timedelta(days=1)

        if RosterAssignment.objects.filter(roster=roster, employee_id__in=parsed_employee_ids, assignment_date__range=(start_date, end_date), is_deleted=False).exists():
            raise ValidationError({"assignments": "One or more employees already have active assignments in this roster and date range."})

        actor = _actor_name(user)
        assignment_rows = [
            RosterAssignment(
                roster=roster,
                employee=employee_by_id[employee_id],
                assignment_date=assignment_date,
                shift=shift,
                day_type=day_type,
                source="manual",
                created_by_name=actor,
                updated_by_name=actor,
            )
            for employee_id in parsed_employee_ids
            for assignment_date, shift, day_type in dates
        ]
        RosterAssignment.objects.bulk_create(assignment_rows)
        return len(assignment_rows)

    @staticmethod
    def assignment_grid(roster):
        assignments = roster.assignments.filter(is_deleted=False).select_related("employee", "shift").order_by("assignment_date", "employee__employee_code")
        return {
            "roster": {
                "id": str(roster.id), "name": roster.name,
                "company": {"id": str(roster.company_id), "name": roster.company.name},
                "plant": {"id": str(roster.plant_id), "name": roster.plant.name},
                "department": ({"id": str(roster.department_id), "name": roster.department.name} if roster.department_id else None),
                "start_date": roster.start_date, "end_date": roster.end_date, "status": roster.status,
            },
            "assignments": [
                {
                    "id": str(item.id),
                    "employee": {"id": str(item.employee_id), "employee_code": item.employee.employee_code, "name": f"{item.employee.first_name} {item.employee.last_name}".strip()},
                    "assignment_date": item.assignment_date,
                    "day_type": item.day_type,
                    "source": item.source,
                    "shift_id": str(item.shift_id) if item.shift_id else None,
                    "shift_name": item.shift.name if item.shift_id else None,
                    "shift_code": item.shift.code if item.shift_id else None,
                    "shift_time": f"{item.shift.start_time.strftime('%H:%M')} - {item.shift.end_time.strftime('%H:%M')}" if item.shift_id else None,
                    "shift_type": item.shift.shift_type if item.shift_id else None,
                    "shift": ({
                        "id": str(item.shift_id), "name": item.shift.name, "code": item.shift.code,
                        "time": f"{item.shift.start_time.strftime('%H:%M')} - {item.shift.end_time.strftime('%H:%M')}",
                        "type": item.shift.shift_type,
                    } if item.shift_id else None),
                }
                for item in assignments
            ],
        }

    @staticmethod
    @transaction.atomic
    def rotate_roster(roster, payload, user):
        if not isinstance(payload, dict):
            raise ValidationError({"request": "Request body must be a JSON object."})
        if roster.start_date > roster.end_date:
            raise ValidationError({"roster": "Roster has an invalid date range."})
        employee_ids = payload.get("employee_ids")
        if not isinstance(employee_ids, list) or not employee_ids:
            raise ValidationError({"employee_ids": "Provide a non-empty list of employee UUIDs."})

        parsed_ids = [RosterService._uuid(value, "employee_ids") for value in employee_ids]
        if len(set(parsed_ids)) != len(parsed_ids):
            raise ValidationError({"employee_ids": "Duplicate employee IDs are not allowed."})

        weeks = payload.get("weeks")
        if isinstance(weeks, bool) or not isinstance(weeks, int) or weeks <= 0:
            raise ValidationError({"weeks": "weeks must be a positive integer."})

        employees = list(Employee.objects.filter(
            id__in=parsed_ids,
            company_id=roster.company_id,
            plant_id=roster.plant_id,
        ).select_related("department"))
        employee_by_id = {employee.id: employee for employee in employees}
        missing = [str(pk) for pk in parsed_ids if pk not in employee_by_id]
        if missing:
            raise ValidationError({"employee_ids": f"Employees do not belong to this roster's company and plant: {', '.join(missing)}."})
        if roster.department_id:
            wrong_department = [
                RosterService._employee_display(employee_by_id[pk])
                for pk in parsed_ids
                if employee_by_id[pk].department_id != roster.department_id
            ]
            if wrong_department:
                raise ValidationError({"employee_ids": f"Employees must belong to roster department {roster.department_id}: {', '.join(wrong_department)}."})

        shifts = list(Shift.objects.filter(
            company_id=roster.company_id,
            plant_id=roster.plant_id,
            shift_type="contract",
            is_active=True,
            is_deleted=False,
        ))
        shift_a = next((item for item in shifts if item.start_time == time(7, 0) and item.end_time == time(19, 0)), None)
        shift_b = next((item for item in shifts if item.start_time == time(19, 0) and item.end_time == time(7, 0)), None)
        if not shift_a or not shift_b:
            raise ValidationError({"shift_configuration": "Active CONTRACT Shift A (07:00-19:00) and Shift B (19:00-07:00) must both exist for this roster's company and plant."})

        applicable_assignments = EmployeeShift.objects.filter(
            employee_id__in=parsed_ids,
            effective_from__lte=roster.end_date,
            is_active=True,
            shift__is_active=True,
            shift__is_deleted=False,
        ).filter(Q(effective_to__isnull=True) | Q(effective_to__gte=roster.end_date)).select_related("shift").order_by("-effective_from")
        current_by_employee = {}
        for assignment in applicable_assignments:
            current_by_employee.setdefault(assignment.employee_id, assignment)

        source_rows = list(RosterAssignment.objects.filter(
            roster=roster,
            employee_id__in=parsed_ids,
            assignment_date__range=(roster.start_date, roster.end_date),
            is_deleted=False,
        ).select_related("shift", "employee").order_by("assignment_date"))
        source_by_employee = {pk: [] for pk in parsed_ids}
        for row in source_rows:
            source_by_employee[row.employee_id].append(row)

        shift_pair = {shift_a.id: shift_a, shift_b.id: shift_b}
        baseline_by_employee = {}
        work_offsets_by_employee = {}
        day_types_by_employee = {}
        last_week_start = roster.start_date + timedelta(days=((roster.end_date - roster.start_date).days // 7) * 7)

        for employee_id in parsed_ids:
            employee = employee_by_id[employee_id]
            employee_display = RosterService._employee_display(employee)
            current_assignment = current_by_employee.get(employee_id)
            if not current_assignment:
                raise ValidationError({"employee_ids": f"{employee_display} has no applicable shift assignment on {roster.end_date}."})
            if current_assignment.shift.company_id != roster.company_id or current_assignment.shift.plant_id != roster.plant_id:
                raise ValidationError({"employee_ids": f"{employee_display} has a shift outside the roster company and plant."})
            if current_assignment.shift.shift_type.lower() != "contract":
                raise ValidationError({"employee_ids": [f"{employee_display} is assigned to {current_assignment.shift.shift_type.upper()} shift type. Rotation is allowed only for CONTRACT shift type."]})

            employee_rows = source_by_employee[employee_id]
            if not employee_rows:
                raise ValidationError({"assignments": f"{employee_display} has no active source assignments in this roster date range."})
            for row in employee_rows:
                if row.day_type not in dict(RosterAssignment.DAY_TYPE_CHOICES):
                    raise ValidationError({"assignments": f"{employee_display} has an invalid day_type in the source roster."})
                if row.shift_id and (row.shift_id not in shift_pair or not row.shift.is_active or row.shift.is_deleted):
                    raise ValidationError({"assignments": f"{employee_display} has an invalid source shift; only active CONTRACT Shift A/B assignments can be rotated."})
                if row.day_type == "WORKING_DAY" and not row.shift_id:
                    raise ValidationError({"assignments": f"{employee_display} has a WORKING_DAY without a shift in the source roster."})
                if row.day_type != "WORKING_DAY" and row.shift_id:
                    raise ValidationError({"assignments": f"{employee_display} has a shift on a non-working source date."})

            working_rows = [row for row in employee_rows if row.shift_id]
            applicable_shift = current_assignment.shift
            if applicable_shift.id not in shift_pair:
                raise ValidationError({"employee_ids": f"{employee_display} is not assigned to the configured CONTRACT Shift A or Shift B."})
            baseline = working_rows[-1].shift if working_rows else applicable_shift
            if baseline.id not in shift_pair:
                raise ValidationError({"assignments": f"{employee_display} has no valid Shift A/B source assignment."})
            baseline_by_employee[employee_id] = baseline

            employee_day_types = {}
            # Preserve the roster's final week's active workday pattern. If
            # that partial week has no assignment rows, use the dates present
            # in the roster's own final week as working offsets.
            work_offsets = set()
            for row in employee_rows:
                if last_week_start <= row.assignment_date <= roster.end_date and row.shift_id:
                    work_offsets.add((row.assignment_date - last_week_start).days)
                    employee_day_types[(row.assignment_date - last_week_start).days] = row.day_type
                elif last_week_start <= row.assignment_date <= roster.end_date:
                    employee_day_types[(row.assignment_date - last_week_start).days] = row.day_type
            if not work_offsets:
                for row in employee_rows:
                    if row.shift_id:
                        work_offsets.add((row.assignment_date - last_week_start).days % 7)
            work_offsets_by_employee[employee_id] = work_offsets
            day_types_by_employee[employee_id] = employee_day_types

        roster_days = (roster.end_date - roster.start_date).days + 1
        completed_cycles = (roster_days + 6) // 7
        try:
            first_rotation_start = roster.start_date + timedelta(days=completed_cycles * 7)
            generated_end = first_rotation_start + timedelta(days=weeks * 7 - 1)
            padding_start = roster.end_date + timedelta(days=1)
            padding_end = first_rotation_start - timedelta(days=1)
        except (OverflowError, ValueError):
            raise ValidationError({"weeks": "The requested rotation date range is invalid."})

        actor = _actor_name(user)
        output_by_employee = {pk: [] for pk in parsed_ids}
        created_count = 0
        updated_count = 0

        for employee_id in parsed_ids:
            employee = employee_by_id[employee_id]
            active_existing = {
                item.assignment_date: item
                for item in RosterAssignment.objects.filter(
                    roster=roster,
                    employee_id=employee_id,
                    assignment_date__range=(padding_start, generated_end),
                    is_deleted=False,
                ).select_related("shift")
            }

            plan = []
            current_date = padding_start
            while current_date <= padding_end:
                plan.append((current_date, None, None))
                current_date += timedelta(days=1)

            for cycle_index in range(weeks):
                cycle_start = first_rotation_start + timedelta(days=cycle_index * 7)
                base_shift = baseline_by_employee[employee_id]
                rotated_shift = shift_b if base_shift.id == shift_a.id else shift_a
                if cycle_index % 2:
                    rotated_shift = base_shift
                for offset in range(7):
                    assignment_date = cycle_start + timedelta(days=offset)
                    if offset in work_offsets_by_employee[employee_id]:
                        target_shift = rotated_shift
                        day_type = "WORKING_DAY"
                    else:
                        target_shift = None
                        day_type = day_types_by_employee[employee_id].get(offset)
                    plan.append((assignment_date, target_shift, day_type))

            for assignment_date, target_shift, target_day_type in plan:
                existing = active_existing.get(assignment_date)
                if existing:
                    if existing.day_type is not None and existing.day_type not in dict(RosterAssignment.DAY_TYPE_CHOICES):
                        raise ValidationError({"assignments": f"Invalid existing day_type for {employee_display} on {assignment_date}."})
                    if existing.day_type == "WORKING_DAY" and existing.shift_id is None:
                        raise ValidationError({"assignments": f"Existing WORKING_DAY assignment has no shift for {employee_display} on {assignment_date}."})
                    if existing.day_type != "WORKING_DAY":
                        if existing.shift_id is not None:
                            raise ValidationError({"assignments": f"Conflicting non-working assignment for {employee_display} on {assignment_date}."})
                        # Preserve manual leave, holiday, and week-off rows.
                        output_by_employee[employee_id].append({
                            "date": assignment_date,
                            "shift": None,
                            "shift_id": None,
                            "day_type": existing.day_type,
                            "source": existing.source,
                        })
                        continue
                    if existing.shift_id not in shift_pair:
                        raise ValidationError({"assignments": f"Conflicting existing shift for {employee_display} on {assignment_date}."})
                    if target_shift is None:
                        raise ValidationError({"assignments": f"A working shift already exists for {employee_display} on padding date {assignment_date}."})
                    existing.shift = target_shift
                    existing.day_type = target_day_type
                    existing.source = "rotation"
                    existing.updated_by_name = actor
                    existing.save(update_fields=["shift", "day_type", "source", "updated_by_name", "updated_at"])
                    updated_count += 1
                    chosen_shift = target_shift
                    chosen_day_type = target_day_type
                else:
                    created = RosterAssignment.objects.create(
                        roster=roster,
                        employee=employee,
                        assignment_date=assignment_date,
                        shift=target_shift,
                        day_type=target_day_type,
                        source="rotation",
                        created_by_name=actor,
                        updated_by_name=actor,
                    )
                    created_count += 1
                    chosen_shift = created.shift
                    chosen_day_type = created.day_type
                output_by_employee[employee_id].append({
                    "date": assignment_date,
                    "shift": chosen_shift.name if chosen_shift else None,
                    "shift_id": str(chosen_shift.id) if chosen_shift else None,
                    "day_type": chosen_day_type,
                })

        return {
            "roster_id": str(roster.id),
            "employees_rotated": len(parsed_ids),
            "weeks": weeks,
            "generated_start_date": padding_start,
            "generated_end_date": generated_end,
            "assignments_created": created_count,
            "assignments_updated": updated_count,
            "rotation": [
                {
                    "employee_id": str(employee_id),
                    "employee_name": f"{employee_by_id[employee_id].first_name} {employee_by_id[employee_id].last_name}".strip(),
                    "employee_code": employee_by_id[employee_id].employee_code,
                    "assignments": output_by_employee[employee_id],
                }
                for employee_id in parsed_ids
            ],
        }
