
import uuid

from django.db import models

from apps.hrms.models.employee import Employee
from apps.hrms.models.attendance import Attendance


class AttendanceLog(models.Model):

    PUNCH_TYPE_CHOICES = (
        ("in_time", "in_time"),
        ("out_time", "out_time"),
        ("break_in", "Break In"),
        ("break_out", "Break Out"),
    )

    SOURCE_CHOICES = (
        ("biometric", "Biometric"),
        ("excel", "Excel"),
        ("mobile", "Mobile"),
        ("web", "Web"),
        ("manual", "Manual"),
    )

    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_logs"
    )

    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name="logs",
        null=True,
        blank=True
    )

    punch_type = models.CharField(
        max_length=20,
        choices=PUNCH_TYPE_CHOICES
    )

    punch_time = models.DateTimeField()

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    device_id = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "hrms_attendance_logs"

        indexes = [
            models.Index(
                fields=["employee", "punch_time"]
            ),
            models.Index(
                fields=["punch_time"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.employee.employee_code} - "
            f"{self.punch_type} - "
            f"{self.punch_time}"
        )

