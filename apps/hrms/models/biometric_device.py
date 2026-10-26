
import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


class BiometricDevice(models.Model):

    DEVICE_TYPE_CHOICES = (
        ("zkteco", "ZKTeco"),
        ("essl", "eSSL"),
        ("hikvision", "Hikvision"),
        ("other", "Other"),
    )

    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="biometric_devices"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="biometric_devices"
    )

    name = models.CharField(
        max_length=100
    )

    device_code = models.CharField(
        max_length=100
    )

    device_type = models.CharField(
        max_length=30,
        choices=DEVICE_TYPE_CHOICES,
        default="other"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    port = models.PositiveIntegerField(
        default=4370
    )

    serial_number = models.CharField(
        max_length=150,
        blank=True
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    last_sync_at = models.DateTimeField(
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
        db_table = "hrms_biometric_devices"

        constraints = [
            models.UniqueConstraint(
                fields=["plant", "device_code"],
                name="unique_biometric_device_per_plant"
            )
        ]

    def __str__(self):
        return f"{self.device_code} - {self.name}"

