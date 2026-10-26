# import uuid

# from django.db import models

# from apps.masters.models.company import Company
# from apps.masters.models.plant import Plant
# from apps.masters.models.department import Department


# class Employee(models.Model):

#     STATUS_CHOICES = (
#         ("active", "Active"),
#         ("inactive", "Inactive"),
#         ("terminated", "Terminated"),
#         ("resigned", "Resigned"),
#     )

#     EMPLOYMENT_TYPE_CHOICES = (
#         ("permanent", "Permanent"),
#         ("contract", "Contract"),
#         ("temporary", "Temporary"),
#         ("intern", "Intern"),
#     )

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     employee_code = models.CharField(
#         max_length=50,
#         unique=True
#     )

#     # --------------------------------------------------
#     # Organization
#     # --------------------------------------------------

#     company = models.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         related_name="employees"
#     )

#     plant = models.ForeignKey(
#         Plant,
#         on_delete=models.CASCADE,
#         related_name="employees"
#     )

#     department = models.ForeignKey(
#         Department,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="employees"
#     )

#     # --------------------------------------------------
#     # Personal information
#     # --------------------------------------------------

#     first_name = models.CharField(
#         max_length=100
#     )

#     last_name = models.CharField(
#         max_length=100,
#         blank=True
#     )

#     email = models.EmailField(
#         blank=True,
#         null=True
#     )

#     phone = models.CharField(
#         max_length=20,
#         blank=True,
#         null=True
#     )

#     # --------------------------------------------------
#     # Employment
#     # --------------------------------------------------

#     employment_type = models.CharField(
#         max_length=20,
#         choices=EMPLOYMENT_TYPE_CHOICES,
#         default="permanent"
#     )

#     joining_date = models.DateField(
#         null=True,
#         blank=True
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="active"
#     )

#     # --------------------------------------------------
#     # Manager
#     # --------------------------------------------------

#     reporting_manager = models.ForeignKey(
#         "self",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="subordinates"
#     )

#     # --------------------------------------------------
#     # Audit
#     # --------------------------------------------------

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     class Meta:
#         db_table = "employees"

#         constraints = [
#             models.UniqueConstraint(
#                 fields=[
#                     "plant",
#                     "employee_code"
#                 ],
#                 name="unique_employee_code_per_plant"
#             )
#         ]

#     def __str__(self):
#         return f"{self.employee_code} - {self.first_name} {self.last_name}"



import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.masters.models.department import Department


class Employee(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("terminated", "Terminated"),
        ("resigned", "Resigned"),
    )

    EMPLOYMENT_TYPE_CHOICES = (
        ("permanent", "Permanent"),
        ("contract", "Contract"),
        ("temporary", "Temporary"),
        ("intern", "Intern"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee_code = models.CharField(
        max_length=50,
        unique=True
    )

    # --------------------------------------------------
    # Organization
    # --------------------------------------------------

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        # related_name="employees",
        null=True,
        blank=True,
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        # related_name="employees",
        null=True,
        blank=True,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # related_name="employees"
    )

    # --------------------------------------------------
    # Personal Information
    # --------------------------------------------------

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )
    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # --------------------------------------------------
    # Employment
    # --------------------------------------------------

    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default="permanent"
    )

    joining_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    # --------------------------------------------------
    # Manager
    # --------------------------------------------------

    reporting_manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates"
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    grade = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    designation = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    # --------------------------------------------------
    # Audit
    # --------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "employees"

        indexes = [
            models.Index(
                fields=["company"]
            ),
            models.Index(
                fields=["plant"]
            ),
            models.Index(
                fields=["department"]
            ),
            models.Index(
                fields=["status"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.employee_code} - "
            f"{self.first_name} {self.last_name}"
        )

