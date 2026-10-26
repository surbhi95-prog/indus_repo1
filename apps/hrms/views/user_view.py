# # from rest_framework.views import APIView
# # from rest_framework.permissions import IsAuthenticated
# # from rest_framework.response import Response
# # from rest_framework import status

# # from apps.accounts.permissions import (
# #     IsPlantHROrSuperAdmin,
# # )

# # from apps.hrms.serializers.user_serializer import (
# #     CreateUserSerializer,
# #     UserSerializer,
# # )

# # from apps.hrms.services.user_service import (
# #     UserService,
# # )


# # class UserCreateView(APIView):

# #     permission_classes = [
# #         IsAuthenticated,
# #         IsPlantHROrSuperAdmin,
# #     ]

# #     def post(self, request):

# #         serializer = CreateUserSerializer(
# #             data=request.data,
# #             context={
# #                 "request": request,
# #             }
# #         )

# #         serializer.is_valid(
# #             raise_exception=True
# #         )

# #         user = UserService.create_user(
# #             serializer.validated_data
# #         )

# #         return Response(
# #             {
# #                 "success": True,
# #                 "message":
# #                     "User created successfully.",
# #                 "data":
# #                     UserSerializer(user).data,
# #             },
# #             status=status.HTTP_201_CREATED,
# #         )


# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status

# # from apps.accounts.permissions import (
# #     # IsPlantHROrSuperAdmin,
# #     IsSuperAdmin,
# # )

# from apps.hrms.serializers.user_serializer import (
#     CreateUserSerializer,
#     UserListSerializer,
#     UserSerializer,
# )

# from apps.hrms.services.user_service import (
#     UserService,
# )


# # =========================================================
# # CREATE USER
# # =========================================================

# class UserCreateView(APIView):

#     permission_classes = [
#         IsAuthenticated,
#         # IsPlantHROrSuperAdmin,
#         # IsSuperAdmin,
#     ]

#     def post(self, request):

#         serializer = CreateUserSerializer(
#             data=request.data,
#             context={
#                 "request": request,
#             }
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         user = UserService.create_user(
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "success": True,
#                 "message":
#                     "User created successfully.",
#                 "data":
#                     UserSerializer(user).data,
#             },
#             status=status.HTTP_201_CREATED,
#         )


# # =========================================================
# # FETCH USERS
# # =========================================================
# # class UserListView(APIView):

# #     permission_classes = [
# #         IsAuthenticated,
# #         IsPlantHROrSuperAdmin,
# #     ]

# #     def get(self, request):

# #         company_id = request.query_params.get("company")
# #         plant_id = request.query_params.get("plant")
# #         department_id = request.query_params.get("department")

# #         users = UserService.get_users(
# #             logged_in_user=request.user,
# #             company_id=company_id,
# #             plant_id=plant_id,
# #             department_id=department_id,
# #         )

# #         serializer = UserListSerializer(
# #             users,
# #             many=True
# #         )

# #         return Response(
# #             {
# #                 "success": True,
# #                 "count": users.count(),
# #                 "data": serializer.data,
# #             },
# #             status=status.HTTP_200_OK,
# #         )


# class UserListView(APIView):

#     permission_classes = [
#         IsAuthenticated,
#         # IsPlantHROrSuperAdmin,
#         # IsSuperAdmin,
#     ]

#     # =====================================================
#     # GET USERS
#     # =====================================================

#     def get(self, request):

#         # =================================================
#         # ORGANIZATION FILTERS
#         # =================================================

#         company_id = request.query_params.get(
#             "company"
#         )

#         plant_id = request.query_params.get(
#             "plant"
#         )

#         department_id = request.query_params.get(
#             "department"
#         )

#         # =================================================
#         # USER FILTERS
#         # =================================================

#         employee_code = request.query_params.get(
#             "employee_code"
#         )

#         email = request.query_params.get(
#             "email"
#         )

#         first_name = request.query_params.get(
#             "first_name"
#         )

#         last_name = request.query_params.get(
#             "last_name"
#         )

#         search = request.query_params.get(
#             "search"
#         )

#         # =================================================
#         # BOOLEAN FILTERS
#         # =================================================

#         is_active = self.get_boolean_param(
#             request,
#             "is_active"
#         )

#         is_staff = self.get_boolean_param(
#             request,
#             "is_staff"
#         )

#         is_superuser = self.get_boolean_param(
#             request,
#             "is_superuser"
#         )

#         # =================================================
#         # ROLE
#         # =================================================

#         role_id = request.query_params.get(
#             "role"
#         )

#         # =================================================
#         # FETCH USERS
#         # =================================================

#         users = UserService.get_users(

#             logged_in_user=request.user,

#             company_id=company_id,

#             plant_id=plant_id,

#             department_id=department_id,

#             employee_code=employee_code,

#             email=email,

#             first_name=first_name,

#             last_name=last_name,

#             search=search,

#             is_active=is_active,

#             is_staff=is_staff,

#             is_superuser=is_superuser,

#             role_id=role_id,
#         )

#         # =================================================
#         # SERIALIZE
#         # =================================================

#         serializer = UserListSerializer(
#             users,
#             many=True
#         )

#         # =================================================
#         # RESPONSE
#         # =================================================

#         return Response(
#             {
#                 "success": True,
#                 "count": users.count(),
#                 "data": serializer.data,
#             },
#             status=status.HTTP_200_OK,
#         )

#     # =====================================================
#     # BOOLEAN PARAMETER
#     # =====================================================

#     @staticmethod
#     def get_boolean_param(
#         request,
#         parameter_name
#     ):

#         value = request.query_params.get(
#             parameter_name
#         )

#         if value is None:
#             return None

#         value = value.strip().lower()

#         if value in [
#             "true",
#             "1",
#             "yes",
#         ]:
#             return True

#         if value in [
#             "false",
#             "0",
#             "no",
#         ]:
#             return False

#         return None

# # =========================================================
# # FETCH USER BY ID
# # =========================================================

# # class UserDetailView(APIView):

# #     permission_classes = [
# #         IsAuthenticated,
# #         IsPlantHROrSuperAdmin,
# #     ]

# #     def get(self, request, user_id):

# #         user = UserService.get_user_by_id(
# #             logged_in_user=request.user,
# #             user_id=user_id,
# #         )

# #         if not user:

# #             return Response(
# #                 {
# #                     "success": False,
# #                     "message":
# #                         "User not found or you do not "
# #                         "have permission to access this user.",
# #                 },
# #                 status=status.HTTP_404_NOT_FOUND,
# #             )

# #         serializer = UserSerializer(user)

# #         return Response(
# #             {
# #                 "success": True,
# #                 "data": serializer.data,
# #             },
# #             status=status.HTTP_200_OK,
# #         )


# class UserDetailView(APIView):

#     permission_classes = [
#         IsAuthenticated,
#         # IsPlantHROrSuperAdmin,
#         # IsSuperAdmin,
#     ]

#     def get(self, request, user_id):

#         user = UserService.get_user_by_id(
#             logged_in_user=request.user,
#             user_id=user_id,
#         )

#         if not user:
#             return Response(
#                 {
#                     "success": False,
#                     "message": (
#                         "User not found or you do not "
#                         "have permission to access this user."
#                     ),
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = UserSerializer(user)

#         return Response(
#             {
#                 "success": True,
#                 "data": serializer.data,
#             },
#             status=status.HTTP_200_OK,
#         )

from rest_framework.views import APIView
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from uuid import UUID

from apps.masters.models.company import Company
from apps.masters.models.department import Department
from apps.masters.models.plant import Plant

from apps.hrms.serializers.user_serializer import (
    CreateUserSerializer,
    UserListSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

from apps.hrms.services.user_service import (
    UserService,
)


# =========================================================
# CREATE USER
# =========================================================

class UserCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        serializer = CreateUserSerializer(
            data=request.data,
            context={
                "request": request,
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        # user = UserService.create_user(
        #     serializer.validated_data,
        #     created_by=request.user,
        #     documents=request.FILES.getlist("documents"),
        # )
        documents = request.FILES.getlist(
            "documents"
        )
        if len(documents) > 4:
            return Response(
                {
                    "success": False,
                    "message":
                        "Maximum 4 documents can be uploaded."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = UserService.create_user(
            serializer.validated_data,
            created_by=request.user,
            documents=documents,
        )

        return Response(
            {
                "success": True,
                "message": "User created successfully.",
                "data": UserSerializer(
                    user,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# FETCH USERS
# =========================================================

class UserListView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        # =================================================
        # ORGANIZATION FILTERS
        # =================================================

        company_id = request.query_params.get(
            "company_id"
        )

        plant_id = request.query_params.get(
            "plant_id"
        )

        department_id = (
            request.query_params.get("department_id")
            or request.query_params.get("department")
        )
        scope = request.query_params.get(
           "scope"
        )
        if plant_id and not company_id:
            return Response(
                {
                    "success": False,
                    "message": "company_id is required when plant_id is provided."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        parsed_company_id = None
        parsed_plant_id = None
        if company_id:
            try:
                parsed_company_id = UUID(company_id)
            except (ValueError, TypeError, AttributeError):
                return Response(
                    {"success": False, "message": "Provide a valid company_id."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not Company.objects.filter(pk=parsed_company_id).exists():
                return Response(
                    {"success": False, "message": "Company not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if plant_id:
            try:
                parsed_plant_id = UUID(plant_id)
            except (ValueError, TypeError, AttributeError):
                return Response(
                    {"success": False, "message": "Provide a valid plant_id."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not Plant.objects.filter(
                pk=parsed_plant_id,
                company_id=parsed_company_id,
            ).exists():
                return Response(
                    {"success": False, "message": "The selected plant does not belong to the selected company."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if department_id:
            if not plant_id:
                return Response(
                    {"success": False, "message": "plant_id is required when filtering by department."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                parsed_department_id = UUID(department_id)
            except (ValueError, TypeError, AttributeError):
                return Response(
                    {"success": False, "message": "Provide a valid department_id."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not Department.objects.filter(
                pk=parsed_department_id,
                company_id=parsed_company_id,
                plant_id=parsed_plant_id,
            ).exists():
                return Response(
                    {"success": False, "message": "The selected department does not belong to the selected company and plant."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # =================================================
# VALIDATE SCOPE
# =================================================

        if scope:
            scope = scope.strip().lower()

            if scope not in ["company", "plant"]:
                return Response(
                    {
                        "success": False,
                        "message": "scope must be either 'company' or 'plant'."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
                # =================================================
        # USER FILTERS
        # =================================================

        employee_code = request.query_params.get(
            "employee_code"
        )

        email = request.query_params.get(
            "email"
        )

        first_name = request.query_params.get(
            "first_name"
        )

        last_name = request.query_params.get(
            "last_name"
        )

        search = request.query_params.get(
            "search"
        )

        # =================================================
        # BOOLEAN FILTERS
        # =================================================

        is_active = self.get_boolean_param(
            request,
            "is_active"
        )

        is_staff = self.get_boolean_param(
            request,
            "is_staff"
        )

        is_superuser = self.get_boolean_param(
            request,
            "is_superuser"
        )

        # =================================================
        # ROLE
        # =================================================

        role_id = request.query_params.get(
            "role"
        )
        
        shift_id = request.query_params.get("shift_id")
        shift_type = request.query_params.get("shift_type")
        # =================================================
        # FETCH USERS
        # =================================================

        users = UserService.get_users(
            logged_in_user=request.user,
            company_id=company_id,
            plant_id=plant_id,
            department_id=department_id,
            scope=scope,
            employee_code=employee_code,
            email=email,
            first_name=first_name,
            last_name=last_name,
            search=search,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            role_id=role_id,
            shift_id=shift_id,
            shift_type=shift_type,
        )

        # =================================================
        # SERIALIZE
        # =================================================

        serializer = UserListSerializer(
            users,
            many=True
        )

        # =================================================
        # RESPONSE
        # =================================================

        return Response(
            {
                "success": True,
                "count": users.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # =====================================================
    # BOOLEAN PARAMETER
    # =====================================================

    @staticmethod
    def get_boolean_param(
        request,
        parameter_name
    ):

        value = request.query_params.get(
            parameter_name
        )

        if value is None:
            return None

        value = value.strip().lower()

        if value in [
            "true",
            "1",
            "yes",
        ]:
            return True

        if value in [
            "false",
            "0",
            "no",
        ]:
            return False

        return None


# =========================================================
# FETCH USER BY ID
# =========================================================

class UserDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, user_id):

        user = UserService.get_user_by_id(
            logged_in_user=request.user,
            user_id=user_id,
        )

        if not user:

            return Response(
                {
                    "success": False,
                    "message": (
                        "User not found or you do not "
                        "have permission to access this user."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(user)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
        # =====================================================
    # UPDATE USER
    # =====================================================

    def put(self, request, user_id):

        user = UserService.get_user_by_id(
            logged_in_user=request.user,
            user_id=user_id,
        )

        if not user:

            return Response(
                {
                    "success": False,
                    "message": (
                        "User not found or you do not "
                        "have permission to update this user."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # =================================================
        # VALIDATE UPDATE DATA
        # =================================================

        update_serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True,
            context={
                "request": request,
            },
        )

        update_serializer.is_valid(
            raise_exception=True
        )

        documents = request.FILES.getlist(
            "documents"
        )

        user = UserService.update_user(
            user,
            update_serializer.validated_data,
            updated_by=request.user,
            documents=documents,
        )

        # update_user receives the prefetched instance used for validation.
        # Re-fetch so the response serializer sees the committed document set.
        user = UserService.get_user_by_id(
            logged_in_user=request.user,
            user_id=user.id,
        )

        return Response(
            {
                "success": True,
                "message": "User updated successfully.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

    # =====================================================
    # DELETE USER
    # =====================================================

    def delete(self, request, user_id):

        user = UserService.get_user_by_id(
            logged_in_user=request.user,
            user_id=user_id,
        )

        if not user:

            return Response(
                {
                    "success": False,
                    "message": (
                        "User not found or you do not "
                        "have permission to delete this user."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        UserService.delete_user(
            user,
            deleted_by=request.user,
        )

        return Response(
            {
                "success": True,
                "message": "User deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )
