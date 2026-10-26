from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.accounts.models.role import Role

User = get_user_model()


class UserRoleAssignSerializer(serializers.Serializer):

    user_id = serializers.UUIDField()

    role_id = serializers.UUIDField()

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
            role = Role.objects.select_related(
                "company",
                "plant",
                "department"
            ).get(
                id=attrs["role_id"],
                is_active=True
            )
        except Role.DoesNotExist:

            raise serializers.ValidationError({
                "role_id":
                "Role not found."
            })

        attrs["user"] = user
        attrs["role"] = role

        return attrs


class UserRoleSerializer(serializers.Serializer):

    id = serializers.UUIDField()

    user_id = serializers.UUIDField(
        source="user.id"
    )

    user_email = serializers.EmailField(
        source="user.email"
    )

    role_id = serializers.UUIDField(
        source="role.id"
    )

    role_name = serializers.CharField(
        source="role.name"
    )

    role_code = serializers.CharField(
        source="role.code"
    )

    role_scope = serializers.CharField(
        source="role.scope"
    )

    assigned_by = serializers.EmailField(
        source="assigned_by.email",
        allow_null=True
    )

    assigned_at = serializers.DateTimeField()