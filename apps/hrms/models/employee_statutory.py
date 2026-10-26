import uuid
from django.db import models
from apps.hrms.models.employee import Employee

class EmployeeStatutory(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="statutory"
    )

    ppf_account_no = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    uan_no = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    esic_no = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    aadhaar_no = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    pan_no = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    punching_code = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )