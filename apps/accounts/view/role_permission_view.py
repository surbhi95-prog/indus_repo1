# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.accounts.permissions import IsSuperAdmin

# from apps.accounts.models.role_permission import RolePermission

# from apps.accounts.serializers.role_permission_serializer import (
#     RolePermissionAssignSerializer,
#     RolePermissionSerializer,
# )

# from apps.accounts.services.role_permission_service import (
#     RolePermissionService,
# )
# class RolePermissionView(APIView):

#     permission_classes = [
#         IsAuthenticated,
#         IsSuperAdmin,
#     ]

#     def post(self, request):

#         serializer = RolePermissionAssignSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         role_permission = RolePermissionService.assign_permission(
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "Permission assigned successfully.",
#             "data": RolePermissionSerializer(
#                 role_permission
#             ).data
#         })

#     def get(self, request):

#         role_id = request.query_params.get("role_id")

#         queryset = RolePermission.objects.select_related(
#             "role",
#             "permission",
#             "permission__company",
#             "permission__plant",
#             "permission__department"
#         )

#         if role_id:
#             queryset = queryset.filter(
#                 role_id=role_id
#             )

#         serializer = RolePermissionSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })




from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsSuperAdmin

from apps.accounts.models.role_permission import (
    RolePermission
)

from apps.accounts.serializers.role_permission_serializer import (
    BulkRolePermissionAssignSerializer,
    RolePermissionAssignSerializer,
    RolePermissionSerializer,
)

from apps.accounts.services.role_permission_service import (
    RolePermissionService,
)


class RolePermissionView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def post(self, request):

        serializer = RolePermissionAssignSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        role_permission = (
            RolePermissionService
            .assign_permission(
                serializer.validated_data
            )
        )

        return Response(
            {
                "success": True,

                "message":
                    "Permission assigned successfully.",

                "data":
                    RolePermissionSerializer(
                        role_permission
                    ).data,
            },
            status=status.HTTP_201_CREATED
        )

    # def get(self, request):

    #     queryset = (
    #         RolePermission.objects
    #         .select_related(
    #             "role",
    #             "permission"
    #         )
    #         .order_by(
    #             "role__name",
    #             "permission__module",
    #             "permission__action"
    #         )
    #     )

    #     serializer = RolePermissionSerializer(
    #         queryset,
    #         many=True
    #     )

    #     return Response(
    #         {
    #             "success": True,

    #             "count": queryset.count(),

    #             "data": serializer.data,
    #         }
    #     )
    def get(self, request):

        # =====================================================
        # QUERY PARAMETERS
        # =====================================================

        company_id = request.query_params.get(
            "company_id"
        )

        plant_id = request.query_params.get(
            "plant_id"
        )

        scope = request.query_params.get(
            "scope"
        )

        # =====================================================
        # NORMALIZE SCOPE
        # =====================================================

        if scope:
            scope = scope.strip().lower()

        # =====================================================
        # VALIDATE SCOPE
        # =====================================================

        valid_scopes = [
            "company",
            "plant",
            "department",
        ]

        if scope and scope not in valid_scopes:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Invalid scope. "
                        "Allowed values are: "
                        "company, plant, department."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================================
        # COMPANY SCOPE + PLANT VALIDATION
        # =====================================================

        if scope == "company" and plant_id:

            return Response(
                {
                    "success": False,
                    "message": (
                        "plant_id cannot be used when "
                        "scope is company because "
                        "company-scope roles do not have "
                        "a plant."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================================
        # PLANT FILTER REQUIRES COMPANY
        # =====================================================

        if plant_id and not company_id:

            return Response(
                {
                    "success": False,
                    "message": (
                        "company_id is required when "
                        "plant_id is provided."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================================
        # BASE QUERY
        # =====================================================

        queryset = (
            RolePermission.objects
            .select_related(
                "role",
                "role__company",
                "role__plant",
                "permission"
            )
        )

        # =====================================================
        # COMPANY FILTER
        # =====================================================

        if company_id:

            queryset = queryset.filter(
                role__company_id=company_id
            )

        # =====================================================
        # PLANT FILTER
        # =====================================================

        if plant_id:

            queryset = queryset.filter(
                role__plant_id=plant_id
            )

        # =====================================================
        # SCOPE FILTER
        # =====================================================

        if scope:

            queryset = queryset.filter(
                role__scope=scope
            )

        # =====================================================
        # ORDERING
        # =====================================================

        queryset = queryset.order_by(
            "role__name",
            "permission__module",
            "permission__action"
        )

        # =====================================================
        # RESPONSE
        # =====================================================

        serializer = RolePermissionSerializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,

                "count": queryset.count(),

                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )


class BulkRolePermissionView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def post(self, request):

        serializer = BulkRolePermissionAssignSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        role = serializer.validated_data["role"]

        permissions = serializer.validated_data[
            "permissions"
        ]

        result = (
            RolePermissionService
            .assign_permissions_bulk(
                role=role,
                permissions=permissions
            )
        )

        return Response(
            {
                "success": True,

                "message":
                    "Permissions assigned successfully.",

                "role": {
                    "id": str(role.id),
                    "name": role.name,
                    "code": role.code,
                },

                "created_count":
                    len(result["created"]),

                "already_assigned_count":
                    len(result["already_assigned"]),

                "created":
                    result["created"],

                "already_assigned":
                    result["already_assigned"],
            },
            status=status.HTTP_201_CREATED
        )