from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsSuperAdmin

from apps.accounts.models.user_permission import UserPermission

from apps.accounts.serializers.user_permission_serializer import (
    UserPermissionAssignSerializer,
    UserPermissionSerializer,
)

from apps.accounts.services.user_permission_service import (
    UserPermissionService,
)


class UserPermissionView(APIView):
    """
    POST -> Assign Direct Permission
    GET  -> List User Permissions
    """

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def post(self, request):

        serializer = UserPermissionAssignSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user_permission = (
            UserPermissionService.assign_permission(
                serializer.validated_data
            )
        )

        return Response(
            {
                "success": True,
                "message": "Permission assigned successfully.",
                "data": UserPermissionSerializer(
                    user_permission
                ).data
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request):

        queryset = UserPermission.objects.select_related(
            "user",
            "permission"
        ).order_by(
            "user__email"
        )

        serializer = UserPermissionSerializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "data": serializer.data,
            }
        )