from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hrms.models.department_skill import (
    DepartmentSkill
)

from apps.hrms.serializers.department_skill_serializer import (
    DepartmentSkillSerializer
)


class DepartmentSkillListCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        queryset = (
            DepartmentSkill.objects
            .select_related(
                "department",
                "skill"
            )
            .order_by(
                "department__name",
                "skill__name"
            )
        )

        department_id = request.query_params.get(
            "department"
        )

        if department_id:

            queryset = queryset.filter(
                department_id=department_id
            )

        serializer = DepartmentSkillSerializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

    def post(self, request):

        serializer = DepartmentSkillSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        department_skill = serializer.save()

        return Response(
            {
                "success": True,
                "message":
                    "Department skill assigned successfully.",
                "data":
                    DepartmentSkillSerializer(
                        department_skill
                    ).data
            },
            status=status.HTTP_201_CREATED
        )