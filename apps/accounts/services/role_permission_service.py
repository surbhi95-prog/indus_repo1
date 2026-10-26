# from django.db import transaction

# from rest_framework.exceptions import ValidationError

# from apps.accounts.models.role_permission import RolePermission


# class RolePermissionService:

#     @staticmethod
#     @transaction.atomic
#     def assign_permission(validated_data):

#         role = validated_data["role"]
#         permission = validated_data["permission"]

#         if RolePermission.objects.filter(
#             role=role,
#             permission=permission
#         ).exists():

#             raise ValidationError({
#                 "permission": "Permission already assigned."
#             })

#         return RolePermission.objects.create(
#             role=role,
#             permission=permission
#         )

#     @staticmethod
#     def get_role_permissions(role_id):

#         return RolePermission.objects.select_related(
#             "role",
#             "permission",
#             "permission__company",
#             "permission__plant",
#             "permission__department"
#         ).filter(
#             role_id=role_id
#         ).order_by(
#             "permission__module",
#             "permission__action"
#         )

#     @staticmethod
#     @transaction.atomic
#     def remove_permission(role, permission):

#         deleted, _ = RolePermission.objects.filter(
#             role=role,
#             permission=permission
#         ).delete()

#         if deleted == 0:
#             raise ValidationError({
#                 "permission":
#                 "Permission is not assigned."
#             })

#         return True


from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.accounts.models.role_permission import RolePermission


class RolePermissionService:

    # @staticmethod
    # @transaction.atomic
    # def assign_permission(validated_data):

    #     role = validated_data["role"]

    #     permission = validated_data["permission"]

    #     if RolePermission.objects.filter(
    #         role=role,
    #         permission=permission
    #     ).exists():

    #         raise ValidationError({
    #             "permission":
    #                 "Permission already assigned to this role."
    #         })

    #     return RolePermission.objects.create(
    #         role=role,
    #         permission=permission
    #     )

    @staticmethod
    @transaction.atomic
    def assign_permission(validated_data):

        role = validated_data["role"]

        permission = validated_data["permission"]

        # -------------------------------------------------
        # VALIDATE ROLE SCOPE
        # -------------------------------------------------

        if role.scope not in ["company", "plant"]:

            raise ValidationError({
                "role_id": (
                    f"Role '{role.name}' uses unsupported "
                    f"scope '{role.scope}'. "
                    "Only company and plant roles "
                    "are allowed."
                )
            })

        # -------------------------------------------------
        # VALIDATE PERMISSION SCOPE
        # -------------------------------------------------

        if permission.scope != "company":

            raise ValidationError({
                "permission": (
                    "Only company-level permissions "
                    "can be assigned to roles."
                )
            })

        # -------------------------------------------------
        # VALIDATE COMPANY
        # -------------------------------------------------

        if role.company_id != permission.company_id:

            raise ValidationError({
                "permission": (
                    "Permission does not belong "
                    "to role company."
                )
            })

        # -------------------------------------------------
        # DUPLICATE
        # -------------------------------------------------

        if RolePermission.objects.filter(
            role=role,
            permission=permission
        ).exists():

            raise ValidationError({
                "permission":
                    "Permission already assigned to this role."
            })

        return RolePermission.objects.create(
            role=role,
            permission=permission
        )

    # =====================================================
    # BULK ASSIGN
    # =====================================================

    @staticmethod
    @transaction.atomic
    def assign_permissions_bulk(
        role,
        permissions
    ):

        created = []
        already_assigned = []

        # -----------------------------------------------------
        # VALIDATE ROLE SCOPE
        # -----------------------------------------------------

        if role.scope not in ["company", "plant"]:

            raise ValidationError({
                "role_id": (
                    f"Role '{role.name}' uses unsupported "
                    f"scope '{role.scope}'. "
                    "Only company and plant roles "
                    "are allowed."
                )
            })

        # -----------------------------------------------------
        # VALIDATE PERMISSIONS
        # -----------------------------------------------------

        for permission in permissions:

            # Only company permissions are allowed
            if permission.scope != "company":

                raise ValidationError({
                    "permission": (
                        f"Permission '{permission.code}' "
                        "is not a company-level permission. "
                        "Only company-level permissions "
                        "can be assigned to roles."
                    )
                })

            # Permission and role must belong to same company
            if role.company_id != permission.company_id:

                raise ValidationError({
                    "permission": (
                        f"Permission '{permission.code}' "
                        "does not belong to role company."
                    )
                })

        # -----------------------------------------------------
        # Existing assignments
        # -----------------------------------------------------

        existing_permission_ids = set(
            RolePermission.objects.filter(
                role=role,
                permission__in=permissions
            ).values_list(
                "permission_id",
                flat=True
            )
        )

        # -----------------------------------------------------
        # Prepare new assignments
        # -----------------------------------------------------

        new_assignments = []

        for permission in permissions:

            if permission.id in existing_permission_ids:

                already_assigned.append({
                    "permission_id": str(
                        permission.id
                    ),
                    "permission_code": permission.code,
                })

                continue

            new_assignments.append(
                RolePermission(
                    role=role,
                    permission=permission
                )
            )

        # -----------------------------------------------------
        # Bulk create
        # -----------------------------------------------------

        if new_assignments:

            created_objects = (
                RolePermission.objects.bulk_create(
                    new_assignments
                )
            )

            for obj in created_objects:

                created.append({
                    "id": str(obj.id),
                    "permission_id": str(
                        obj.permission_id
                    ),
                    "permission_code":
                        obj.permission.code,
                })

        # -----------------------------------------------------
        # Response
        # -----------------------------------------------------

        return {
            "created": created,
            "already_assigned": already_assigned,
        }

    # =========================================================
    # REMOVE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def remove_permission(
        role,
        permission
    ):

        deleted, _ = (
            RolePermission.objects
            .filter(
                role=role,
                permission=permission
            )
            .delete()
        )

        if deleted == 0:

            raise ValidationError({
                "permission":
                    "Permission is not assigned to this role."
            })

        return True