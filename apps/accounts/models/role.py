# import uuid

# from django.db import models

# from apps.masters.models.company import Company
# from apps.masters.models.plant import Plant
# from apps.masters.models.department import Department


# class Role(models.Model):

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     company = models.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         related_name="roles",
#         null=True,
#         blank=True
#     )

#     plant = models.ForeignKey(
#         Plant,
#         on_delete=models.CASCADE,
#         related_name="roles",
#         null=True,
#         blank=True
#     )

#     department = models.ForeignKey(
#         Department,
#         on_delete=models.CASCADE,
#         related_name="roles",
#         null=True,
#         blank=True
#     )

#     name = models.CharField(
#         max_length=100
#     )

#     code = models.CharField(
#         max_length=50
#     )

#     description = models.TextField(
#         blank=True,
#         null=True
#     )

#     is_active = models.BooleanField(
#         default=True
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     class Meta:
#         db_table = "roles"

#         constraints = [

#             models.UniqueConstraint(
#                 fields=["company", "plant", "department", "name"],
#                 name="unique_role_name"
#             ),

#             models.UniqueConstraint(
#                 fields=["company", "plant", "department", "code"],
#                 name="unique_role_code"
#             ),
#         ]

#     def __str__(self):
#         return self.name



import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.masters.models.department import Department


class Role(models.Model):

    SCOPE_CHOICES = (
        ("company", "Company"),
        ("plant", "Plant"),
        ("department", "Department"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="roles"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="roles"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="roles"
    )

    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        default="company"
    )

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_system = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "roles"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "plant",
                    "department",
                    "code"
                ],
                name="unique_role_scope"
            )
        ]

    def __str__(self):
        return self.name