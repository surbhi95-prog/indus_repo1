import uuid

from django.db import models

from apps.hrms.models.employee import Employee
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


class BiometricPunch(models.Model):

    PUNCH_TYPE_CHOICES = (
        ("in", "IN"),
        ("out", "OUT"),
        ("unknown", "Unknown"),
    )

    SOURCE_CHOICES = (
        ("biometric", "Biometric"),
        ("manual", "Manual"),
        ("api", "API"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="biometric_punches"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="biometric_punches"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="biometric_punches"
    )

    # ID received from biometric machine
    device_user_id = models.CharField(
        max_length=100,
        db_index=True
    )

    # Optional biometric device identifier
    device_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    punch_time = models.DateTimeField(
        db_index=True
    )

    punch_type = models.CharField(
        max_length=20,
        choices=PUNCH_TYPE_CHOICES,
        default="unknown"
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="biometric"
    )

    # Raw data received from biometric device/API
    raw_data = models.JSONField(
        null=True,
        blank=True
    )

    is_processed = models.BooleanField(
        default=False
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "biometric_punches"
        ordering = ["-punch_time"]

        indexes = [
            models.Index(
                fields=["employee", "punch_time"]
            ),
            models.Index(
                fields=["company", "plant", "punch_time"]
            ),
            models.Index(
                fields=["device_user_id", "punch_time"]
            ),
            models.Index(
                fields=["is_processed"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.employee} - "
            f"{self.punch_time} - "
            f"{self.punch_type}"
        )
    