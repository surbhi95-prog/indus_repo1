# from django.db import transaction

# from rest_framework.exceptions import ValidationError

# from apps.accounts.models.user_permission import UserPermission


# class UserPermissionService:

#     @staticmethod
#     @transaction.atomic
#     def assign_permission(validated_data):
#         """
#         Assign Direct Permission to User
#         """

#         user = validated_data["user"]
#         permission = validated_data["permission"]

#         if UserPermission.objects.filter(
#             user=user,
#             permission=permission
#         ).exists():

#             raise ValidationError({
#                 "permission": "Permission already assigned to this user."
#             })

#         user_permission = UserPermission.objects.create(
#             user=user,
#             permission=permission
#         )

#         return user_permission

#     @staticmethod
#     @transaction.atomic
#     def remove_permission(user, permission):
#         """
#         Remove Direct Permission
#         """

#         deleted, _ = UserPermission.objects.filter(
#             user=user,
#             permission=permission
#         ).delete()

#         if deleted == 0:
#             raise ValidationError({
#                 "permission": "Permission is not assigned to this user."
#             })

#         return True
    



from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.accounts.models.user_permission import (
    UserPermission
)


class UserPermissionService:

    @staticmethod
    @transaction.atomic
    def assign_permission(validated_data):

        user = validated_data["user"]

        permission = validated_data["permission"]

        if UserPermission.objects.filter(
            user=user,
            permission=permission
        ).exists():

            raise ValidationError({
                "permission":
                    "Permission already assigned to user."
            })

        return UserPermission.objects.create(
            user=user,
            permission=permission
        )

    @staticmethod
    @transaction.atomic
    def remove_permission(
        user,
        permission
    ):

        deleted, _ = (
            UserPermission.objects
            .filter(
                user=user,
                permission=permission
            )
            .delete()
        )

        if deleted == 0:

            raise ValidationError({
                "permission":
                    "Permission is not assigned to user."
            })

        return True