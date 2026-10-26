from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import JWTAuthentication

from apps.accounts.models.user_role import UserRole

from apps.accounts.serializers.user_role_serializer import (
    UserRoleAssignSerializer,
    UserRoleSerializer,
)

from apps.accounts.services.user_role_service import (
    UserRoleService,
)


class UserRoleView(APIView):

    authentication_classes = [
        JWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = UserRoleAssignSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        target_user = serializer.validated_data["user"]

        role = serializer.validated_data["role"]

        user_role = UserRoleService.assign_role(
            assigner=request.user,
            target_user=target_user,
            role=role
        )

        return Response(
            {
                "success": True,
                "message":
                    "Role assigned successfully.",
                "data":
                    UserRoleSerializer(
                        user_role
                    ).data
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request):

        user_id = request.query_params.get(
            "user_id"
        )

        role_id = request.query_params.get(
            "role_id"
        )

        queryset = UserRole.objects.select_related(
            "user",
            "role",
            "assigned_by"
        )

        if user_id:
            queryset = queryset.filter(
                user_id=user_id
            )

        if role_id:
            queryset = queryset.filter(
                role_id=role_id
            )

        serializer = UserRoleSerializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "data": serializer.data
            }
        )

    def delete(self, request):

        user_id = request.data.get(
            "user_id"
        )

        role_id = request.data.get(
            "role_id"
        )

        serializer = UserRoleAssignSerializer(
            data={
                "user_id": user_id,
                "role_id": role_id
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        UserRoleService.remove_role(
            assigner=request.user,
            target_user=serializer.validated_data["user"],
            role=serializer.validated_data["role"]
        )

        return Response(
            {
                "success": True,
                "message":
                    "Role removed successfully."
            },
            status=status.HTTP_200_OK
        )