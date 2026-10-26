# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# from apps.accounts.models.permission import Permission
# from apps.accounts.models.user_permission import UserPermission

# User = get_user_model()


# class UserPermissionAssignSerializer(serializers.Serializer):
#     """
#     Assign Direct Permission to User
#     """

#     user_id = serializers.UUIDField()
#     permission_id = serializers.UUIDField()

#     def validate(self, attrs):

#         user_id = attrs.get("user_id")
#         permission_id = attrs.get("permission_id")

#         # -------------------------------------
#         # Validate User
#         # -------------------------------------

#         try:
#             user = User.objects.get(
#                 id=user_id,
#                 is_active=True
#             )
#         except User.DoesNotExist:
#             raise serializers.ValidationError({
#                 "user_id": "User not found."
#             })

#         # -------------------------------------
#         # Validate Permission
#         # -------------------------------------

#         try:
#             permission = Permission.objects.get(
#                 id=permission_id
#             )
#         except Permission.DoesNotExist:
#             raise serializers.ValidationError({
#                 "permission_id": "Permission not found."
#             })

#         # -------------------------------------
#         # Duplicate Check
#         # -------------------------------------

#         if UserPermission.objects.filter(
#             user=user,
#             permission=permission
#         ).exists():

#             raise serializers.ValidationError({
#                 "permission": "Permission already assigned to this user."
#             })

#         attrs["user"] = user
#         attrs["permission"] = permission

#         return attrs


# class UserPermissionSerializer(serializers.ModelSerializer):

#     user = serializers.EmailField(
#         source="user.email",
#         read_only=True
#     )

#     permission = serializers.CharField(
#         source="permission.code",
#         read_only=True
#     )

#     class Meta:
#         model = UserPermission
#         fields = [
#             "id",
#             "user",
#             "permission",
#             "created_at",
#         ]



from rest_framework import serializers

from apps.accounts.models.user import User
from apps.accounts.models.permission import Permission
from apps.accounts.models.user_permission import UserPermission


class UserPermissionAssignSerializer(
    serializers.Serializer
):

    user_id = serializers.UUIDField()

    permission_id = serializers.UUIDField()

    def validate(self, attrs):

        try:

            user = User.objects.get(
                id=attrs["user_id"],
                is_active=True
            )

        except User.DoesNotExist:

            raise serializers.ValidationError({
                "user_id":
                    "User not found."
            })

        try:

            permission = Permission.objects.get(
                id=attrs["permission_id"]
            )

        except Permission.DoesNotExist:

            raise serializers.ValidationError({
                "permission_id":
                    "Permission not found."
            })

        # ---------------------------------------------
        # Company validation
        # ---------------------------------------------

        if not user.is_superuser:

            if user.company_id != permission.company_id:

                raise serializers.ValidationError({
                    "permission":
                        "Permission does not belong to user's company."
                })

        # ---------------------------------------------
        # Duplicate
        # ---------------------------------------------

        if UserPermission.objects.filter(
            user=user,
            permission=permission
        ).exists():

            raise serializers.ValidationError({
                "permission":
                    "Permission already assigned to user."
            })

        attrs["user"] = user

        attrs["permission"] = permission

        return attrs


class UserPermissionSerializer(
    serializers.ModelSerializer
):

    user_email = serializers.CharField(
        source="user.email",
        read_only=True
    )

    permission_code = serializers.CharField(
        source="permission.code",
        read_only=True
    )

    class Meta:

        model = UserPermission

        fields = [
            "id",
            "user_email",
            "permission_code",
            "created_at",
        ]