from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hrms.models.employee_skill import EmployeeSkill

from apps.hrms.serializers.employee_skill_serializer import (
    EmployeeSkillSerializer
)


class EmployeeSkillListCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        queryset = (
            EmployeeSkill.objects
            .select_related(
                "employee",
                "skill",
                "assessed_by"
            )
            .order_by(
                "employee__first_name",
                "skill__name"
            )
        )

        employee_id = request.query_params.get(
            "employee"
        )

        if employee_id:

            queryset = queryset.filter(
                employee_id=employee_id
            )

        serializer = EmployeeSkillSerializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

    def post(self, request):

        serializer = EmployeeSkillSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        employee_skill = serializer.save()

        return Response(
            {
                "success": True,
                "message":
                    "Employee skill created successfully.",
                "data":
                    EmployeeSkillSerializer(
                        employee_skill
                    ).data
            },
            status=status.HTTP_201_CREATED
        )


class EmployeeSkillDetailView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, skill_id):

        try:

            employee_skill = (
                EmployeeSkill.objects
                .select_related(
                    "employee",
                    "skill",
                    "assessed_by"
                )
                .get(id=skill_id)
            )

        except EmployeeSkill.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message":
                        "Employee skill not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "success": True,
            "data":
                EmployeeSkillSerializer(
                    employee_skill
                ).data
        })

    def put(self, request, skill_id):

        try:

            employee_skill = EmployeeSkill.objects.get(
                id=skill_id
            )

        except EmployeeSkill.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message":
                        "Employee skill not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeSkillSerializer(
            employee_skill,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response({
            "success": True,
            "message":
                "Employee skill updated successfully.",
            "data": serializer.data
        })

    def delete(self, request, skill_id):

        try:

            employee_skill = EmployeeSkill.objects.get(
                id=skill_id
            )

        except EmployeeSkill.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message":
                        "Employee skill not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        employee_skill.delete()

        return Response({
            "success": True,
            "message":
                "Employee skill deleted successfully."
        })