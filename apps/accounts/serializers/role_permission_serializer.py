# from rest_framework import serializers

# from apps.accounts.models.role import Role
# from apps.accounts.models.permission import Permission
# from apps.accounts.models.role_permission import RolePermission


# class RolePermissionAssignSerializer(serializers.Serializer):

#     role_id = serializers.UUIDField()
#     permission_id = serializers.UUIDField()

#     def validate(self, attrs):

#         try:
#             role = Role.objects.get(
#                 id=attrs["role_id"],
#                 is_active=True
#             )
#         except Role.DoesNotExist:
#             raise serializers.ValidationError({
#                 "role_id": "Role not found."
#             })

#         try:
#             permission = Permission.objects.get(
#                 id=attrs["permission_id"]
#             )
#         except Permission.DoesNotExist:
#             raise serializers.ValidationError({
#                 "permission_id": "Permission not found."
#             })

#         # -----------------------------------
#         # Same Company
#         # -----------------------------------

#         if role.company_id != permission.company_id:

#             raise serializers.ValidationError({
#                 "company":
#                 "Role and Permission belong to different companies."
#             })

#         # -----------------------------------
#         # Plant Validation
#         # -----------------------------------

#         if permission.scope == "plant":

#             if role.plant_id != permission.plant_id:

#                 raise serializers.ValidationError({
#                     "plant":
#                     "Role and Permission belong to different plants."
#                 })

#         # -----------------------------------
#         # Department Validation
#         # -----------------------------------

#         if permission.scope == "department":

#             if role.department_id != permission.department_id:

#                 raise serializers.ValidationError({
#                     "department":
#                     "Role and Permission belong to different departments."
#                 })

#         if RolePermission.objects.filter(
#             role=role,
#             permission=permission
#         ).exists():

#             raise serializers.ValidationError({
#                 "permission":
#                 "Permission already assigned."
#             })

#         attrs["role"] = role
#         attrs["permission"] = permission

#         return attrs

# class RolePermissionSerializer(serializers.ModelSerializer):

#     role_id = serializers.UUIDField(
#         source="role.id",
#         read_only=True
#     )

#     role_name = serializers.CharField(
#         source="role.name",
#         read_only=True
#     )

#     company = serializers.CharField(
#         source="permission.company.name",
#         read_only=True
#     )

#     plant = serializers.CharField(
#         source="permission.plant.name",
#         read_only=True
#     )

#     department = serializers.CharField(
#         source="permission.department.name",
#         read_only=True
#     )

#     scope = serializers.CharField(
#         source="permission.scope",
#         read_only=True
#     )

#     module = serializers.CharField(
#         source="permission.module",
#         read_only=True
#     )

#     action = serializers.CharField(
#         source="permission.action",
#         read_only=True
#     )

#     permission = serializers.CharField(
#         source="permission.code",
#         read_only=True
#     )

#     class Meta:
#         model = RolePermission
#         fields = [
#             "id",
#             "role_id",
#             "role_name",
#             "company",
#             "plant",
#             "department",
#             "scope",
#             "module",
#             "action",
#             "permission",
#             "created_at",
#         ]




from rest_framework import serializers

from apps.accounts.models.role import Role
from apps.accounts.models.permission import Permission
from apps.accounts.models.role_permission import RolePermission


class RolePermissionAssignSerializer(
    serializers.Serializer
):

    role_id = serializers.UUIDField()

    permission_id = serializers.UUIDField()

    def validate(self, attrs):

        role_id = attrs["role_id"]

        permission_id = attrs["permission_id"]

        try:

            role = Role.objects.get(
                id=role_id,
                is_active=True
            )

        except Role.DoesNotExist:

            raise serializers.ValidationError({
                "role_id":
                    "Role not found."
            })

        try:

            permission = Permission.objects.get(
                id=permission_id
            )

        except Permission.DoesNotExist:

            raise serializers.ValidationError({
                "permission_id":
                    "Permission not found."
            })

        # ---------------------------------------------
        # Company validation
        # ---------------------------------------------

        if role.company_id != permission.company_id:

            raise serializers.ValidationError({
                "permission":
                    "Permission does not belong to role company."
            })

        # ---------------------------------------------
        # Plant role validation
        # ---------------------------------------------

        # if role.scope == "plant":

        #     if permission.scope== "plant":

        #         if role.plant_id != permission.plant_id:

        #             raise serializers.ValidationError({
        #                 "permission":
        #                     "Permission does not belong to role plant."
        #             })

        #     elif permission.scope == "department":

        #         if role.plant_id != permission.plant_id:

        #             raise serializers.ValidationError({
        #                 "permission":
        #                     "Permission does not belong to role plant."
        #             })

        # # ---------------------------------------------
        # # Department role validation
        # # ---------------------------------------------

        # if role.scope == "department":

        #     if permission.scope == "plant":

        #         if role.plant_id != permission.plant_id:

        #             raise serializers.ValidationError({
        #                 "permission":
        #                     "Permission does not belong to role plant."
        #             })

        #     if permission.scope == "department":

        #         if (
        #             role.plant_id != permission.plant_id
        #             or
        #             role.department_id != permission.department_id
        #         ):

        #             raise serializers.ValidationError({
        #                 "permission":
        #                     "Permission does not belong to role department."
        #             })
        # ---------------------------------------------
# ROLE + PERMISSION SCOPE VALIDATION
# ---------------------------------------------

# Only company permissions are allowed to be
# assigned to roles.

        if permission.scope != "company":

            raise serializers.ValidationError({
                "permission": (
                    "Only company-level permissions "
                    "can be assigned to roles."
                )
            })


        # Only company and plant roles are supported.

        if role.scope not in ["company", "plant"]:

            raise serializers.ValidationError({
                "role_id": (
                    f"Role '{role.name}' uses unsupported "
                    f"scope '{role.scope}'. "
                    "Only company and plant roles are "
                    "allowed."
                )
            })
        # ---------------------------------------------
        # Duplicate
        # ---------------------------------------------

        if RolePermission.objects.filter(
            role=role,
            permission=permission
        ).exists():

            raise serializers.ValidationError({
                "permission":
                    "Permission already assigned to this role."
            })

        attrs["role"] = role

        attrs["permission"] = permission

        return attrs


class RolePermissionSerializer(
    serializers.ModelSerializer
):

    role_name = serializers.CharField(
        source="role.name",
        read_only=True
    )

    role_code = serializers.CharField(
        source="role.code",
        read_only=True
    )
    scope = serializers.CharField(
        source="role.scope",
        read_only=True
    )

    company = serializers.CharField(
        source="role.company.name",
        read_only=True,
        allow_null=True
    )

    plant = serializers.CharField(
        source="role.plant.name",
        read_only=True,
        allow_null=True
    )
    permission_code = serializers.CharField(
        source="permission.code",
        read_only=True
    )

    class Meta:

        model = RolePermission

        fields = [
            "id",

            "role_name",
            "role_code",
            "scope",
            "company",
            "plant",
            "permission_code",

            "created_at",
        ]



class BulkRolePermissionAssignSerializer(serializers.Serializer):

    role_id = serializers.UUIDField(
        required=True
    )

    permission_id = serializers.ListField(
        child=serializers.UUIDField(),
        required=True,
        allow_empty=False
    )

    def validate(self, attrs):

        role_id = attrs["role_id"]
        permission_ids = attrs["permission_id"]

        # =====================================================
        # ROLE
        # =====================================================

        try:

            role = Role.objects.get(
                id=role_id,
                is_active=True
            )

        except Role.DoesNotExist:

            raise serializers.ValidationError({
                "role_id":
                    "Role not found or inactive."
            })

        # =====================================================
        # DUPLICATE IDs IN REQUEST
        # =====================================================

        if len(permission_ids) != len(set(permission_ids)):

            raise serializers.ValidationError({
                "permission_id":
                    "Duplicate permission IDs found in request."
            })

        # =====================================================
        # GET PERMISSIONS
        # =====================================================

        permissions = Permission.objects.filter(
            id__in=permission_ids
        )

        permission_map = {
            str(permission.id): permission
            for permission in permissions
        }

        # =====================================================
        # CHECK MISSING PERMISSIONS
        # =====================================================

        missing_permissions = []

        for permission_id in permission_ids:

            if str(permission_id) not in permission_map:

                missing_permissions.append(
                    str(permission_id)
                )

        if missing_permissions:

            raise serializers.ValidationError({
                "permission_id": [
                    f"Permission not found: {permission_id}"
                    for permission_id in missing_permissions
                ]
            })

        # =====================================================
        # VALIDATE EACH PERMISSION
        # =====================================================

        for permission_id in permission_ids:

            permission = permission_map[
                str(permission_id)
            ]

            # -------------------------------------------------
            # COMPANY
            # -------------------------------------------------

            if role.company_id != permission.company_id:

                raise serializers.ValidationError({
                    "permission": (
                        f"Permission {permission.code} "
                        "does not belong to role company."
                    )
                })

            # # -------------------------------------------------
            # # PLANT ROLE
            # # -------------------------------------------------

            # if role.scope == "plant":

            #     if permission.scope == "plant":

            #         if role.plant_id != permission.plant_id:

            #             raise serializers.ValidationError({
            #                 "permission": (
            #                     f"Permission {permission.code} "
            #                     "does not belong to role plant."
            #                 )
            #             })

            #     elif permission.scope == "department":

            #         if role.plant_id != permission.plant_id:

            #             raise serializers.ValidationError({
            #                 "permission": (
            #                     f"Permission {permission.code} "
            #                     "does not belong to role plant."
            #                 )
            #             })

            # # -------------------------------------------------
            # # DEPARTMENT ROLE
            # # -------------------------------------------------

            # if role.scope == "department":

            #     if permission.scope == "plant":

            #         if role.plant_id != permission.plant_id:

            #             raise serializers.ValidationError({
            #                 "permission": (
            #                     f"Permission {permission.code} "
            #                     "does not belong to role plant."
            #                 )
            #             })

            #     elif permission.scope == "department":

            #         if (
            #             role.plant_id != permission.plant_id
            #             or
            #             role.department_id != permission.department_id
            #         ):

            #             raise serializers.ValidationError({
            #                 "permission": (
            #                     f"Permission {permission.code} "
            #                     "does not belong to role department."
            #                 )
            #             })
            # -------------------------------------------------
# PERMISSION SCOPE
# -------------------------------------------------

            if permission.scope != "company":

                raise serializers.ValidationError({
                    "permission": (
                        f"Permission {permission.code} "
                        "is not a company-level permission. "
                        "Only company-level permissions "
                        "can be assigned to roles."
                    )
                })


            # -------------------------------------------------
            # ROLE SCOPE
            # -------------------------------------------------

            if role.scope not in ["company", "plant"]:

                raise serializers.ValidationError({
                    "role_id": (
                        f"Role '{role.name}' uses unsupported "
                        f"scope '{role.scope}'. "
                        "Only company and plant roles "
                        "are allowed."
                    )
                })
        # =====================================================
        # STORE OBJECTS
        # =====================================================

        attrs["role"] = role

        attrs["permissions"] = [
            permission_map[str(permission_id)]
            for permission_id in permission_ids
        ]

        return attrs