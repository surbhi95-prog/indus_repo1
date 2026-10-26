from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import JWTAuthentication
from apps.accounts.models.role import Role
from apps.accounts.serializers.role_serializer import (
    RoleCreateSerializer,
    RoleUpdateSerializer,
    RoleListSerializer,
)
from apps.accounts.services.role_service import RoleService
from apps.accounts.permissions import IsSuperAdmin


# class RoleCreateView(APIView):

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         if not request.user.is_superuser:
#             return Response(
#                 {
#                     "message": "Only Super Admin can create roles."
#                 },
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         serializer = RoleCreateSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         role = RoleService.create_role(
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "message": "Role created successfully.",
#                 "data": RoleListSerializer(role).data,
#             },
#             status=status.HTTP_201_CREATED,
#         )



class RoleCreateView(APIView):

    authentication_classes = [
        JWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin
    ]
    

    def post(self, request):

        serializer = RoleCreateSerializer(
            data=request.data
        )

        # ---------------------------------------------------------
        # VALIDATION
        # ---------------------------------------------------------

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message":
                        "Role validation failed.",
                    "errors":
                        serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------------------------------------------------------
        # CREATE ROLE
        # ---------------------------------------------------------

        try:

            role = RoleService.create_role(
                serializer.validated_data
            )

        except Exception as exc:

            return Response(
                {
                    "success": False,
                    "message":
                        "Failed to create role.",
                    "errors": {
                        "detail": str(exc)
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------------------------------------------------------
        # SUCCESS
        # ---------------------------------------------------------

        return Response(
            {
                "success": True,
                "message":
                    "Role created successfully.",
                "data":
                    RoleListSerializer(
                        role
                    ).data
            },
            status=status.HTTP_201_CREATED
        )


class RoleListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # def get(self, request):

    #     roles = RoleService.get_roles()

    #     serializer = RoleListSerializer(
    #         roles,
    #         many=True
    #     )

    #     return Response(
    #         {
    #             "message": "Roles fetched successfully.",
    #             "data": serializer.data,
    #         },
    #         status=status.HTTP_200_OK,
    #     )
    def get(self, request):

        company_id = request.query_params.get(
            "company_id"
        )

        plant_id = request.query_params.get(
            "plant_id"
        )

        roles = RoleService.get_roles(
            company_id=company_id,
            plant_id=plant_id
        )

        serializer = RoleListSerializer(
            roles,
            many=True
        )

        return Response(
            {
                "message": "Roles fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class RoleDetailView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, role_id):

        try:
            role = RoleService.get_role(
                role_id
            )

        except Role.DoesNotExist:
            return Response(
                {
                    "message": "Role not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RoleListSerializer(
            role
        )

        return Response(
            {
                "message": "Role fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # def put(self, request, role_id):

    #     if not request.user.is_superuser:
    #         return Response(
    #             {
    #                 "message": "Only Super Admin can update roles."
    #             },
    #             status=status.HTTP_403_FORBIDDEN,
    #         )

        # try:
        #     role = RoleService.get_role(
        #         role_id
        #     )

        # except Role.DoesNotExist:
        #     return Response(
        #         {
        #             "message": "Role not found."
        #         },
        #         status=status.HTTP_404_NOT_FOUND,
        #     )

        # serializer = RoleUpdateSerializer(
        #     role,
        #     data=request.data,
        #     partial=True,
        # )

        # serializer.is_valid(
        #     raise_exception=True
        # )

        # role = RoleService.update_role(
        #     role,
        #     serializer.validated_data,
        # )

        # return Response(
        #     {
        #         "message": "Role updated successfully.",
        #         "data": RoleListSerializer(role).data,
        #     },
        #     status=status.HTTP_200_OK,
        # )

    # def delete(self, request, role_id):

    #     if not request.user.is_superuser:
    #         return Response(
    #             {
    #                 "message": "Only Super Admin can delete roles."
    #             },
    #             status=status.HTTP_403_FORBIDDEN,
    #         )

    #     try:
    #         role = RoleService.get_role(
    #             role_id
    #         )

    #     except Role.DoesNotExist:
    #         return Response(
    #             {
    #                 "message": "Role not found."
    #             },
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    #     RoleService.delete_role(
    #         role
    #     )

    #     return Response(
    #         {
    #             "message": "Role deleted successfully."
    #         },
    #         status=status.HTTP_204_NO_CONTENT,
    #     )