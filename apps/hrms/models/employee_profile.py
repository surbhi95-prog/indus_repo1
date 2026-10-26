import uuid
from django.db import models

from apps.hrms.models.employee import Employee


class EmployeeProfile(models.Model):

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    marital_status = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    partner_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    current_address = models.TextField(
        blank=True,
        null=True
    )

    permanent_address = models.TextField(
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    blood_group = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    doctor_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    doctor_address = models.TextField(
        blank=True,
        null=True
    )

    doctor_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    health_issues = models.TextField(
        blank=True,
        null=True
    )

    qualification = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    experience = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
    )

    employer_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    employer_address = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.employee)