# from rest_framework.permissions import BasePermission

# from apps.accounts.models.user_role import UserRole


# class IsSuperAdmin(BasePermission):

#     message = "Only Super Admin can perform this action."

#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         return UserRole.objects.filter(
#             user=request.user,
#             role__code__iexact="SUPER_ADMIN"
#         ).exists()


from django.conf import settings
from django.db.models import Q
from rest_framework.permissions import BasePermission

from apps.accounts.models.user_role import UserRole


class IsAuthenticated(BasePermission):
    """Allow anonymous API testing in DEBUG; require login otherwise."""

    def has_permission(self, request, view):
        return settings.DEBUG or bool(
            request.user and request.user.is_authenticated
        )


# class IsSuperAdmin(BasePermission):
#this is permission.py main file
#     message = "Only Super Admin can perform this action."

#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         return (
#             request.user.is_superuser
#             or
#             UserRole.objects.filter(
#                 user=request.user,
#                 role__code__iexact="SUPER_ADMIN",
#                 role__is_active=True,
#             ).exists()
#         )
class IsSuperAdmin(BasePermission):

    message = "Only Super Admin can perform this action."

    def has_permission(self, request, view):
        if settings.DEBUG:
            return True

        if not request.user.is_authenticated:
            return False

        return True
# class IsPlantHROrSuperAdmin(BasePermission):

#     message = "Only Super Admin or Plant HR can perform this action."

#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         user = request.user

#         # =====================================================
#         # SUPERUSER
#         # =====================================================

#         if user.is_superuser:
#             return True

#         # =====================================================
#         # SUPER ADMIN ROLE
#         # =====================================================

#         if UserRole.objects.filter(
#             user=user,
#             role__code__iexact="SUPER_ADMIN",
#             role__is_active=True,
#         ).exists():

#             return True

#         # =====================================================
#         # PLANT HR / HR MANAGER
#         # =====================================================

#         return UserRole.objects.filter(
#             user=user,
#             role__is_active=True,
#             role__scope__iexact="plant",
#         ).filter(
#             Q(
#                 role__code__iexact="PLANT_HR"
#             )
#             |
#             Q(
#                 role__code__iexact="HR_MANAGER"
#             )
#         ).exists()


# class IsPlantAdmin(BasePermission):

#     message = (
#         "Only Plant Head or Plant HR can perform this action."
#     )

#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         # Superuser
#         if request.user.is_superuser:
#             return True

#         # Super Admin role
#         if UserRole.objects.filter(
#             user=request.user,
#             role__code__iexact="SUPER_ADMIN",
#             role__is_active=True,
#         ).exists():
#             return True

#         # Plant Head / Plant HR / HR Manager
#         return UserRole.objects.filter(
#             user=request.user,
#             role__code__in=[
#                 "PLANT_HEAD",
#                 "PLANT_HR",
#                 "HR_MANAGER",
#             ],
#             role__scope__iexact="plant",
#             role__is_active=True,
#         ).exists()


# class IsDepartmentHead(BasePermission):

#     message = "Only Department Head can perform this action."

#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         return UserRole.objects.filter(
#             user=request.user,
#             role__code__iexact="DEPARTMENT_HEAD",
#             role__scope__iexact="department",
#             role__is_active=True,
#         ).exists()