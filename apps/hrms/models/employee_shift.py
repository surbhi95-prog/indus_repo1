
import uuid

from django.db import models

from apps.hrms.models.employee import Employee
from apps.hrms.models.shift import Shift


class EmployeeShift(models.Model):

    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="shift_assignments"
    )

    shift = models.ForeignKey(
        Shift,
        on_delete=models.PROTECT,
        related_name="employee_assignments"
    )

    effective_from = models.DateField()

    effective_to = models.DateField(
        null=True,
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
        db_table = "hrms_employee_shifts"

        indexes = [
            models.Index(
                fields=["employee", "effective_from"]
            ),
            models.Index(
                fields=["shift"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.employee.employee_code} - "
            f"{self.shift.code}"
        )

