# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# from apps.accounts.permissions import IsSuperAdmin

# from apps.accounts.serializers.permission_serializer import (
#     PermissionCreateSerializer,
#     PermissionSerializer,
# )

# from apps.accounts.services.permission_service import PermissionService

# from apps.accounts.models.permission import Permission


# class PermissionView(APIView):

#     permission_classes = [
#         IsAuthenticated,
#         IsSuperAdmin,
#     ]

#     def post(self, request):

#         serializer = PermissionCreateSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         permission = PermissionService.create_permission(
#             serializer.validated_data
#         )

#         return Response({

#             "success": True,

#             "message": "Permission created successfully.",

#             "data": PermissionSerializer(
#                 permission
#             ).data

#         }, status=status.HTTP_201_CREATED)

#     def get(self, request):

#         permissions = Permission.objects.select_related(
#             "company",
#             "plant",
#             "department"
#         ).order_by(
#             "module",
#             "action"
#         )

#         serializer = PermissionSerializer(
#             permissions,
#             many=True
#         )

#         return Response({

#             "success": True,

#             "count": permissions.count(),

#             "data": serializer.data

#         })


# class PermissionListAPIView(APIView):

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def get(self, request):

#         permissions = PermissionService.get_permissions_for_user(
#             request.user
#         )

#         serializer = PermissionSerializer(
#             permissions,
#             many=True
#         )

#         return Response({

#             "success": True,

#             "count": permissions.count(),

#             "data": serializer.data

#         })




from rest_framework import status
from rest_framework.exceptions import ValidationError
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsSuperAdmin

from apps.accounts.models.permission import Permission

from apps.accounts.serializers.permission_serializer import (
    PermissionCreateSerializer,
    PermissionSerializer,
)

from apps.accounts.services.permission_service import (
    PermissionService,
)


class PermissionView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def post(self, request):

        serializer = PermissionCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        permission = PermissionService.create_permission(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message":
                    "Permission created successfully.",

                "data": PermissionSerializer(
                    permission
                ).data,
            },
            status=status.HTTP_201_CREATED
        )


# class PermissionListAPIView(APIView):

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def get(self, request):

#         permissions = (
#             PermissionService
#             .get_permissions_for_user(
#                 request.user
#             )
#         )

#         serializer = PermissionSerializer(
#             permissions,
#             many=True
#         )

#         return Response(
#             {
#                 "success": True,

#                 "count": permissions.count(),

#                 "data": serializer.data,
#             },
#             status=status.HTTP_200_OK
#         )

class PermissionListAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        # -----------------------------------------------------
        # GET FILTERS
        # -----------------------------------------------------

        company_id = request.query_params.get(
            "company_id"
        )

        plant_id = request.query_params.get(
            "plant_id"
        )

        # -----------------------------------------------------
        # PLANT DEPENDS ON COMPANY
        # -----------------------------------------------------

        if plant_id and not company_id:

            return Response(
                {
                    "success": False,
                    "message":
                        "Company ID is required when filtering by plant.",
                    "errors": {
                        "company_id":
                            "company_id is required when plant_id is provided."
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------------------
        # GET PERMISSIONS
        # -----------------------------------------------------

        try:

            permissions = (
                PermissionService
                .get_permissions_for_user(
                    request.user,
                    company_id=company_id,
                    plant_id=plant_id,
                )
            )
        except ValidationError as exc:

            return Response(
                {
                    "success": False,
                    "message":
                        "Invalid permission filter.",
                    "errors":
                        exc.detail,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exc:

            return Response(
                {
                    "success": False,
                    "message":
                        "Failed to fetch permissions.",
                    "errors": {
                        "detail": str(exc)
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------------------
        # SERIALIZE
        # -----------------------------------------------------

        serializer = PermissionSerializer(
            permissions,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": permissions.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )