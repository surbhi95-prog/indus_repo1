
import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


class AttendanceImport(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("partially_completed", "Partially Completed"),
        ("failed", "Failed"),
    )

    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="attendance_imports"
    )

    plant = models.ForeignKey(
    Plant,
    on_delete=models.CASCADE,
    related_name="attendance_imports"
)

    month = models.PositiveSmallIntegerField()

    year = models.PositiveSmallIntegerField()

    file_name = models.CharField(
    max_length=255
)

    file = models.FileField(
        upload_to="hrms/attendance/"
    )

    uploaded_by = models.CharField(
        max_length=100,
        blank=True
    )

    total_rows = models.PositiveIntegerField(
        default=0
    )

    successful_rows = models.PositiveIntegerField(
        default=0
    )

    failed_rows = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending"
    )

    error_message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "hrms_attendance_imports"

    def __str__(self):
        return self.file_name

