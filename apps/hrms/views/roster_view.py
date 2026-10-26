from uuid import UUID

from django.db import IntegrityError, transaction
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.exceptions import ValidationError
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import JWTAuthentication
from apps.hrms.models.roster import Roster, RosterAssignment
from apps.hrms.models.employee import Employee
from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.hrms.serializers.roster_serializer import (
    RosterAssignmentUpdateSerializer,
    RosterAssignmentListSerializer,
    RosterEditSerializer,
    RosterSerializer,
)
from apps.hrms.services.roster_service import RosterService, _actor_name


class RosterAssignmentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _error(message, field=None):
        body = {"success": False, "message": message}
        if field:
            body["errors"] = {field: message}
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        params = request.query_params
        ids = {}
        if params.get("plant_id") and not params.get("company_id"):
            return self._error("company_id is required when plant_id is provided.", "company_id")

        models = {
            "company_id": Company,
            "plant_id": Plant,
            "shift_id": Shift,
            "employee_id": Employee,
        }
        for field, model in models.items():
            raw_value = params.get(field)
            if raw_value is None:
                continue
            try:
                ids[field] = UUID(raw_value)
            except (ValueError, TypeError, AttributeError):
                return self._error(f"Provide a valid {field}.", field)

            lookup = {"pk": ids[field]}
            if model is Shift:
                lookup.update(is_deleted=False, is_active=True)
            if not model.objects.filter(**lookup).exists():
                return self._error(f"{field.removesuffix('_id').replace('_', ' ').capitalize()} not found.", field)

        if "plant_id" in ids and not Plant.objects.filter(pk=ids["plant_id"], company_id=ids["company_id"]).exists():
            return self._error("The selected plant does not belong to the selected company.", "plant_id")

        parsed_dates = {}
        for field in ("start_date", "end_date"):
            raw_value = params.get(field)
            if raw_value is None:
                continue
            parsed = parse_date(raw_value)
            if parsed is None:
                return self._error(f"Provide a valid {field} in YYYY-MM-DD format.", field)
            parsed_dates[field] = parsed
        if parsed_dates.get("start_date") and parsed_dates.get("end_date") and parsed_dates["start_date"] > parsed_dates["end_date"]:
            return self._error("start_date must be on or before end_date.", "start_date")

        shift_type = params.get("shift_type")
        if shift_type is not None:
            shift_type = normalize_shift_type(shift_type)
            valid_shift_types = {value for value, _ in Shift.SHIFT_TYPE_CHOICES}
            if shift_type not in valid_shift_types:
                return self._error("Invalid shift_type. Allowed values are GENERAL and CONTRACT.", "shift_type")

        queryset = RosterAssignment.objects.filter(is_deleted=False, roster__is_deleted=False).select_related(
            "roster__company", "roster__plant", "roster__department", "employee", "shift"
        )
        if "company_id" in ids:
            queryset = queryset.filter(roster__company_id=ids["company_id"])
        if "plant_id" in ids:
            queryset = queryset.filter(roster__plant_id=ids["plant_id"])
        if "shift_id" in ids:
            queryset = queryset.filter(shift_id=ids["shift_id"])
        if "employee_id" in ids:
            queryset = queryset.filter(employee_id=ids["employee_id"])
        if "start_date" in parsed_dates:
            queryset = queryset.filter(assignment_date__gte=parsed_dates["start_date"])
        if "end_date" in parsed_dates:
            queryset = queryset.filter(assignment_date__lte=parsed_dates["end_date"])
        if shift_type:
            queryset = queryset.filter(shift__shift_type__iexact=shift_type)

        queryset = queryset.order_by(
            "roster__start_date", "roster_id", "employee__first_name",
            "employee__last_name", "employee__employee_code", "assignment_date", "id",
        )
        rows = RosterAssignmentListSerializer(queryset, many=True).data

        grouped_rosters = {}
        for row in rows:
            roster_id = row["roster_id"]
            roster = grouped_rosters.setdefault(roster_id, {
                "roster": {
                    "id": roster_id,
                    "name": row["roster_name"],
                    "company_id": row["company_id"],
                    "company_name": row["company_name"],
                    "plant_id": row["plant_id"],
                    "plant_name": row["plant_name"],
                    "department_id": row["department_id"],
                    "start_date": row["roster_start_date"],
                    "end_date": row["roster_end_date"],
                    "status": row["roster_status"],
                },
                "employees": [],
                "_employees_by_id": {},
            })
            employee = roster["_employees_by_id"].get(row["employee_id"])
            if employee is None:
                employee = {
                    "employee_id": row["employee_id"],
                    "employee_code": row["employee_code"],
                    "employee_name": row["employee_name"],
                    "assignments": [],
                }
                roster["_employees_by_id"][row["employee_id"]] = employee
                roster["employees"].append(employee)

            employee["assignments"].append({
                "assignment_id": row["assignment_id"],
                "date": row["assignment_date"],
                "shift_id": row["shift_id"],
                "shift_name": row["shift_name"],
                "shift_code": row["shift_code"],
                "shift_time": row["shift_time"],
                "shift_type": row["shift_type"],
                "day_type": row["day_type"],
                "source": row["source"],
            })

        data = []
        for roster in grouped_rosters.values():
            roster.pop("_employees_by_id")
            data.append(roster)
        return Response({
            "success": True,
            "message": "Roster assignments fetched successfully.",
            "data": data,
        })


class RosterListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = RosterService.active_rosters()
        return Response({"success": True, "count": queryset.count(), "data": RosterSerializer(queryset, many=True).data})

    def post(self, request):
        serializer = RosterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        actor = _actor_name(request.user)
        try:
            roster = serializer.save(created_by_name=actor, updated_by_name=actor)
        except IntegrityError:
            return Response({"success": False, "message": "An active roster with this name and date range already exists for the selected plant."}, status=status.HTTP_409_CONFLICT)
        return Response({"success": True, "message": "Roster created successfully.", "data": RosterSerializer(roster).data}, status=status.HTTP_201_CREATED)


class RosterDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get(roster_id):
        return Roster.objects.select_related("company", "plant", "department").get(pk=roster_id, is_deleted=False)

    def patch(self, request, roster_id):
        try:
            roster = self._get(roster_id)
        except Roster.DoesNotExist:
            return Response({"success": False, "message": "Roster not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RosterEditSerializer(roster, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            roster = serializer.save(updated_by_name=_actor_name(request.user))
        except IntegrityError:
            return Response({"success": False, "message": "An active roster with this name and date range already exists."}, status=status.HTTP_409_CONFLICT)
        return Response({"success": True, "message": "Roster updated successfully.", "data": RosterSerializer(roster).data})

    @transaction.atomic
    def delete(self, request, roster_id):
        try:
            roster = self._get(roster_id)
        except Roster.DoesNotExist:
            return Response({"success": False, "message": "Roster not found."}, status=status.HTTP_404_NOT_FOUND)
        roster.is_deleted = True
        roster.updated_by_name = _actor_name(request.user)
        roster.save(update_fields=["is_deleted", "updated_by_name", "updated_at"])
        return Response({"success": True, "message": "Roster deleted successfully."}, status=status.HTTP_200_OK)


class RosterAssignView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get(roster_id):
        return Roster.objects.select_related("company", "plant", "department").get(pk=roster_id, is_deleted=False)

    def get(self, request, roster_id):
        try:
            roster = self._get(roster_id)
        except Roster.DoesNotExist:
            return Response({"success": False, "message": "Roster not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"success": True, "data": RosterService.assignment_grid(roster)})

    def post(self, request, roster_id):
        try:
            roster = self._get(roster_id)
        except Roster.DoesNotExist:
            return Response({"success": False, "message": "Roster not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            created = RosterService.generate_assignments(roster, request.data, request.user)
        except ValidationError:
            raise
        except IntegrityError:
            return Response({"success": False, "message": "Duplicate roster assignments are not allowed."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": True, "message": "Roster assignments generated successfully.", "created_assignments": created}, status=status.HTTP_201_CREATED)


class RosterRotateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, roster_id):
        try:
            roster = Roster.objects.select_related("company", "plant", "department").get(
                pk=roster_id,
                is_deleted=False,
            )
        except Roster.DoesNotExist:
            return Response({"success": False, "message": "Roster not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = RosterService.rotate_roster(roster, request.data, request.user)
        except ValidationError as exc:
            errors = exc.detail
            employee_errors = errors.get("employee_ids") if isinstance(errors, dict) else None
            rotation_only_error = (
                isinstance(employee_errors, list)
                and any("Rotation is allowed only for CONTRACT shift type" in str(item) for item in employee_errors)
            )
            return Response({
                "success": False,
                "message": (
                    "Rotation roster can only be applied to employees assigned to CONTRACT shift type."
                    if rotation_only_error else "Roster rotation validation failed."
                ),
                "errors": errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({
                "success": False,
                "message": "Roster rotation conflicts with an existing assignment.",
                "errors": {"assignments": "Duplicate or conflicting assignments are not allowed."},
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Roster rotation applied successfully.",
            "data": result,
        }, status=status.HTTP_201_CREATED)


class RosterAssignmentDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get(assignment_id):
        return RosterAssignment.objects.select_related("roster", "shift").get(pk=assignment_id, is_deleted=False, roster__is_deleted=False)

    def patch(self, request, assignment_id):
        try:
            assignment = self._get(assignment_id)
        except RosterAssignment.DoesNotExist:
            return Response({"success": False, "message": "Roster assignment not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RosterAssignmentUpdateSerializer(assignment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by_name=_actor_name(request.user))
        data = next(
            item for item in RosterService.assignment_grid(assignment.roster)["assignments"]
            if item["id"] == str(assignment.id)
        )
        return Response({"success": True, "message": "Roster assignment updated successfully.", "data": data})

    @transaction.atomic
    def delete(self, request, assignment_id):
        try:
            assignment = self._get(assignment_id)
        except RosterAssignment.DoesNotExist:
            return Response({"success": False, "message": "Roster assignment not found."}, status=status.HTTP_404_NOT_FOUND)
        assignment.is_deleted = True
        assignment.updated_by_name = _actor_name(request.user)
        assignment.save(update_fields=["is_deleted", "updated_by_name", "updated_at"])
        return Response({"success": True, "message": "Roster assignment deleted successfully."}, status=status.HTTP_200_OK)
