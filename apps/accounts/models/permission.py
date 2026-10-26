# import uuid

# from django.db import models

# from apps.masters.models.company import Company
# from apps.masters.models.plant import Plant
# from apps.masters.models.department import Department


# class Permission(models.Model):

#     SCOPE_CHOICES = (
#         ("company", "Company"),
#         ("plant", "Plant"),
#         ("department", "Department"),
#     )

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     company = models.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="permissions",
#     )

#     plant = models.ForeignKey(
#         Plant,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="permissions",
#     )

#     department = models.ForeignKey(
#         Department,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="permissions",
#     )

#     scope = models.CharField(
#         max_length=20,
#         choices=SCOPE_CHOICES,
#         default="company",
#     )

#     module = models.CharField(
#         max_length=100
#     )

#     action = models.CharField(
#         max_length=100
#     )

#     code = models.CharField(
#         max_length=100
#     )

#     description = models.TextField(
#         blank=True,
#         null=True
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     class Meta:
#         db_table = "permissions"

#         constraints = [
#             models.UniqueConstraint(
#                 fields=[
#                     "company",
#                     "plant",
#                     "department",
#                     "module",
#                     "action",
#                 ],
#                 name="unique_permission_scope",
#             )
#         ]

#     def __str__(self):
#         return self.code



import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.masters.models.department import Department


class Permission(models.Model):

    # =========================================================
    # SCOPE
    # =========================================================

    SCOPE_CHOICES = (
        ("company", "Company"),
        ("plant", "Plant"),
        ("department", "Department"),
    )

    # =========================================================
    # ID
    # =========================================================

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # =========================================================
    # COMPANY
    # =========================================================

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="permissions",
    )

    # =========================================================
    # PLANT
    # =========================================================

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="permissions",
    )

    # =========================================================
    # DEPARTMENT
    # =========================================================

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="permissions",
    )

    # =========================================================
    # SCOPE
    # =========================================================

    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        default="company",
    )

    # =========================================================
    # MODULE
    # =========================================================

    module = models.CharField(
        max_length=100,
    )
    tab = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    # =========================================================
    # ACTION
    # =========================================================

    action = models.CharField(
        max_length=100,
    )

    # =========================================================
    # PERMISSION CODE
    # =========================================================

    code = models.CharField(
        max_length=100,
    )

    # =========================================================
    # DESCRIPTION
    # =========================================================

    description = models.TextField(
        blank=True,
        null=True,
    )

    # =========================================================
    # CREATED AT
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # =========================================================
    # META
    # =========================================================

    class Meta:

        db_table = "permissions"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "plant",
                    "department",
                    "scope",
                    "code",
                ],
                name="unique_permission_scope_code",
            ),
        ]

        ordering = [
            "module",
            "code",
        ]

    # =========================================================
    # STRING
    # =========================================================

    def __str__(self):

        return self.code