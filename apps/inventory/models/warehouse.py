import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


class Warehouse(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="warehouses"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="warehouses"
    )

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

    warehouse_type = models.CharField(
        max_length=30,
        choices=[
            ("raw_material", "Raw Material"),
            ("finished_goods", "Finished Goods"),
            ("semi_finished", "Semi Finished"),
            ("tool", "Tool Store"),
            ("spares", "Spare Parts"),
            ("general", "General"),
        ],
        default="general"
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
        db_table = "warehouses"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "plant",
                    "code"
                ],
                name="unique_warehouse_code_per_plant"
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"