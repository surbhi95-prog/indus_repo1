# import uuid

# from django.db import models

# from .plant import Plant


# class Department(models.Model):

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=True
#     )
#     plant = models.ForeignKey(
#         Plant,
#         on_delete= models.CASCADE,
#         related_name="departments"

#     )
#     name = models.CharField(
#         max_length=255

#     )
#     is_active = models.BooleanField(
#         default=True
#     )

#     created_at = models.DateTimeField(
#         auto_now_add = True
#     )

#     updated_at = models.DateField(
#         auto_now = True
#     ) 

#     class MEta :
#         db_table = "departments"
#         ordering = ['name']

#         constraints= [
#             models.UniqueConstraint(
#                 fields = ["plant","name"],
#                 name = "unique_department_name_per_plant"
#             )
#         ]

#         def __str__(self):
#             return self.name
import uuid

from django.db import models

from .company import Company
from .plant import Plant


class Department(models.Model):

    # =========================================================
    # BASIC
    # =========================================================

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # =========================================================
    # COMPANY
    # =========================================================

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="departments",
         null=True,
    blank=True
    )

    # =========================================================
    # PLANT
    # =========================================================

    plant = models.ForeignKey(
        Plant,
        on_delete=models.PROTECT,
        related_name="departments",
         null=True,
    blank=True
    )

    # =========================================================
    # DEPARTMENT
    # =========================================================

    name = models.CharField(
        max_length=255,
         null=True,
            blank=True
    )

    code = models.CharField(
    max_length=50,
    null=True,
    blank=True
)

    description = models.TextField(
        blank=True,
        null=True
    )

    # =========================================================
    # DEPARTMENT HEAD
    # No Employee dependency
    # =========================================================

    department_head = models.UUIDField(
        null=True,
        blank=True
    )

    # =========================================================
    # STATUS
    # =========================================================

    is_active = models.BooleanField(
        default=True
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================================
    # META
    # =========================================================

    class Meta:
        db_table = "departments"
        ordering = ["name"]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "company",
                    "plant",
                    "name"
                ],
                name="unique_department_name_per_company_plant"
            ),

            models.UniqueConstraint(
                fields=[
                    "company",
                    "plant",
                    "code"
                ],
                name="unique_department_code_per_company_plant"
            ),
        ]

    def __str__(self):
        return self.name