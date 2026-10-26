import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.inventory.models.batch import Batch
from apps.inventory.models.item import Item
from apps.inventory.models.storage_location import StorageLocation
from apps.inventory.models.warehouse import Warehouse


class Stock(models.Model):

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
        related_name="stocks"
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="stocks"
    )

    storage_location = models.ForeignKey(
        StorageLocation,
        on_delete=models.PROTECT,
        related_name="stocks"
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="stocks"
    )

    quantity = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=0
    )

    # Quantity reserved for PO
    reserved_quantity = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    class Meta:
        db_table = "inventory_stock"