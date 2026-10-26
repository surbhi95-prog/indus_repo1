from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.accounts.models.role import Role
from apps.accounts.models.user_role import UserRole


class UserRoleService:

    @staticmethod
    def can_assign_role(assigner, target_user, role):

        # ==================================================
        # SUPER ADMIN
        # ==================================================

        if (
            assigner.is_superuser
            or UserRoleService._has_role(
                assigner,
                "SUPER_ADMIN"
            )
        ):
            return True

        # ==================================================
        # COMPANY ADMIN
        # ==================================================

        if UserRoleService._has_role(
            assigner,
            "COMPANY_ADMIN"
        ):

            if assigner.company_id != target_user.company_id:
                raise ValidationError({
                    "user":
                    "Target user does not belong to your company."
                })

            if role.company_id != assigner.company_id:
                raise ValidationError({
                    "role":
                    "You can only assign roles from your company."
                })

            return True

        # ==================================================
        # PLANT HEAD / PLANT HR
        # ==================================================

        if UserRoleService._has_any_role(
            assigner,
            [
                "PLANT_HEAD",
                "PLANT_HR"
            ]
        ):

            if not assigner.plant_id:
                raise ValidationError({
                    "plant":
                    "You are not assigned to a plant."
                })

            if target_user.plant_id != assigner.plant_id:
                raise ValidationError({
                    "user":
                    "You can only manage users from your plant."
                })

            if role.plant_id != assigner.plant_id:
                raise ValidationError({
                    "role":
                    "You can only assign roles from your plant."
                })

            # Plant admin can assign plant roles
            # and department roles inside own plant.

            if role.scope not in [
                "plant",
                "department"
            ]:
                raise ValidationError({
                    "role":
                    "You cannot assign company-level roles."
                })

            return True

        # ==================================================
        # DEPARTMENT HEAD
        # ==================================================

        if UserRoleService._has_role(
            assigner,
            "DEPARTMENT_HEAD"
        ):

            if not assigner.department_id:
                raise ValidationError({
                    "department":
                    "You are not assigned to a department."
                })

            if target_user.department_id != assigner.department_id:
                raise ValidationError({
                    "user":
                    "You can only manage users from your department."
                })

            if role.department_id != assigner.department_id:
                raise ValidationError({
                    "role":
                    "You can only assign roles from your department."
                })

            if role.scope != "department":
                raise ValidationError({
                    "role":
                    "Department Head can only assign department roles."
                })

            return True

        raise ValidationError({
            "permission":
            "You do not have permission to assign roles."
        })

    @staticmethod
    def _has_role(user, role_code):

        return UserRole.objects.filter(
            user=user,
            role__code__iexact=role_code,
            role__is_active=True
        ).exists()

    @staticmethod
    def _has_any_role(user, role_codes):

        return UserRole.objects.filter(
            user=user,
            role__code__in=role_codes,
            role__is_active=True
        ).exists()

    @staticmethod
    @transaction.atomic
    def assign_role(
        assigner,
        target_user,
        role
    ):

        UserRoleService.can_assign_role(
            assigner,
            target_user,
            role
        )

        if UserRole.objects.filter(
            user=target_user,
            role=role
        ).exists():

            raise ValidationError({
                "role":
                "Role already assigned to this user."
            })

        return UserRole.objects.create(
            user=target_user,
            role=role,
            assigned_by=assigner
        )

    @staticmethod
    @transaction.atomic
    def remove_role(
        assigner,
        target_user,
        role
    ):

        # Validate same rules before removing
        UserRoleService.can_assign_role(
            assigner,
            target_user,
            role
        )

        deleted, _ = UserRole.objects.filter(
            user=target_user,
            role=role
        ).delete()

        if deleted == 0:
            raise ValidationError({
                "role":
                "Role is not assigned to this user."
            })

        return True