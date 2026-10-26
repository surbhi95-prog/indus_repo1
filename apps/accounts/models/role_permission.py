# import uuid

# from django.db import models

# from .role import Role
# from .permission import Permission


# class RolePermission(models.Model):

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     role = models.ForeignKey(
#         Role,
#         on_delete=models.CASCADE,
#         related_name="role_permissions"
#     )

#     permission = models.ForeignKey(
#         Permission,
#         on_delete=models.CASCADE,
#         related_name="permission_roles"
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     class Meta:

#         db_table = "role_permissions"

#         unique_together = (
#             "role",
#             "permission"
#         )

#         ordering = [
#             "role__name",
#             "permission__module",
#             "permission__action"
#         ]

#     def __str__(self):
#         return f"{self.role.name} - {self.permission.code}"

import uuid

from django.db import models

from .role import Role
from .permission import Permission


class RolePermission(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions"
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="permission_roles"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "role_permissions"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "role",
                    "permission"
                ],
                name="unique_role_permission"
            )
        ]

    def __str__(self):
        return f"{self.role.name} - {self.permission.code}"