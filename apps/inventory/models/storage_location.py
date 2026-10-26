import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant

from apps.inventory.models.warehouse import Warehouse

class StorageLocation(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # --------------------------------------------------
    # Organization
    # --------------------------------------------------

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="storage_locations"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="storage_locations"
    )

    # --------------------------------------------------
    # Warehouse
    # --------------------------------------------------

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="storage_locations"
    )

    # --------------------------------------------------
    # Location
    # --------------------------------------------------

    code = models.CharField(
        max_length=50
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    # --------------------------------------------------
    # Optional physical information
    # --------------------------------------------------

    rack = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    bin = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    is_active = models.BooleanField(
        default=True
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

        db_table = "storage_locations"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "warehouse",
                    "code"
                ],
                name="unique_storage_location_per_warehouse"
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"