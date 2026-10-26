
import uuid

from django.db import models

from apps.hrms.models.employee import Employee
from apps.hrms.models.biometric_device import BiometricDevice


class BiometricEmployee(models.Model):

    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="biometric_mappings"
    )

    device = models.ForeignKey(
        BiometricDevice,
        on_delete=models.CASCADE,
        related_name="employee_mappings"
    )

    biometric_user_id = models.CharField(
        max_length=100
    )

    card_number = models.CharField(
        max_length=100,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "hrms_biometric_employees"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "device",
                    "biometric_user_id"
                ],
                name="unique_biometric_user_per_device"
            )
        ]

    def __str__(self):
        return (
            f"{self.employee.employee_code} - "
            f"{self.biometric_user_id}"
        )

