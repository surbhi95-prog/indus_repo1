# import uuid

# from django.db import models
# from django.conf import settings

# from .permission import Permission


# class UserPermission(models.Model):

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )

#     permission = models.ForeignKey(
#         Permission,
#         on_delete=models.CASCADE
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     class Meta:

#         db_table = "user_permissions"

#         unique_together = (
#             "user",
#             "permission"
#         )


import uuid

from django.conf import settings
from django.db import models

from apps.accounts.models.user import User

from .permission import Permission
class UserPermission(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="custom_permissions"
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="user_permission_assignments"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "user_permissions"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "permission"],
                name="unique_user_permission"
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.permission.code}"