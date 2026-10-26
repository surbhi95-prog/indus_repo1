from django.conf import settings
from rest_framework.permissions import BasePermission

from apps.accounts.models.user_role import UserRole


# class IsSuperAdmin(BasePermission):
#     """
#     Only Super Admin can access.
#     """

#     message = "Only Super Admin can perform this action."

#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         print("\n========== SUPER ADMIN CHECK ==========")
#         print("User ID:", request.user.id)
#         print("Email:", request.user.email)

#         roles = UserRole.objects.filter(
#             user_id=request.user.id
#         ).values(
#             "role__name",
#             "role__code"
#         )

#         print("Roles:", list(roles))

#         is_super_admin = UserRole.objects.filter(
#             user_id=request.user.id,
#             role__code__iexact="SUPER_ADMIN"
#         ).exists()

#         print("Is Super Admin:", is_super_admin)
#         print("=======================================\n")

#         return is_super_admin
class IsSuperAdmin(BasePermission):
    """
    Temporary: Any authenticated user can access.
    """

    message = "Only Super Admin can perform this action."

    def has_permission(self, request, view):
        if settings.DEBUG:
            return True

        if not request.user.is_authenticated:
            return False

        return True


# ---------------  ACTUAL IMPLEMENTATION LOOKS LIKE THIS --------------
# class IsSuperAdmin(BasePermission):

#     message = "Only Super Admin can perform this action."

#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         return request.user.role.name == "Super Admin"

# class IsSuperAdminOrCompanyAdmin(BasePermission):

#     message = "Permission denied."

#     def has_object_permission(self, request, view, obj):

#         if not request.user.is_authenticated:
#             return False

#         if UserRole.objects.filter(
#             user_id=request.user.id,
#             role__code__iexact="SUPER_ADMIN"
#         ).exists():
#             return True

#         if UserRole.objects.filter(
#             user_id=request.user.id,
#             role__code__iexact="COMPANY_ADMIN"
#         ).exists():

#             return request.user.company_id == obj.id

#         return False
class IsSuperAdminOrCompanyAdmin(BasePermission):

    message = "Permission denied."

    def has_object_permission(self, request, view, obj):
        if settings.DEBUG:
            return True

        if not request.user.is_authenticated:
            return False

        return True


# from rest_framework.permissions import BasePermission, SAFE_METHODS


# class IsOwnerOrReadOnly(BasePermission):

#     def has_object_permission(self, request, view, obj):

#         if request.method in SAFE_METHODS:
#             return True

#         return obj.created_by == request.user


# THIS IS HOW WE USE PERMISSION CLASS in the VIEW --------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import BasePermission


# class IsAuthenticatedUser(BasePermission):

#     def has_permission(self, request, view):
#         return request.user.is_authenticated


# class SalesView(APIView):

#     permission_classes = [IsAuthenticatedUser]

#     def get(self, request):
#         return Response({"message": "Sales data"})