import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.inventory.models.item import Item


class Batch(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="batches"
    )

    batch_number = models.CharField(
        max_length=100
    )

    manufacture_date = models.DateField(
        null=True,
        blank=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "inventory_batches"

        constraints = [
            models.UniqueConstraint(
                fields=["plant", "item", "batch_number"],
                name="unique_batch_per_item_plant"
            )
        ]