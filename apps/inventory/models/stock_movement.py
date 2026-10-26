import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant

from apps.inventory.models.item import Item
from apps.inventory.models.batch import Batch
from apps.inventory.models.warehouse import Warehouse
from apps.inventory.models.storage_location import StorageLocation


class StockMovement(models.Model):

    MOVEMENT_TYPE_CHOICES = (
        ("receipt", "Receipt"),
        ("issue", "Issue"),
        ("transfer", "Transfer"),
        ("adjustment_in", "Adjustment In"),
        ("adjustment_out", "Adjustment Out"),
        ("return", "Return"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="inventory_stock_movements"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="inventory_stock_movements"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="stock_movements"
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="stock_movements"
    )

    movement_type = models.CharField(
        max_length=30,
        choices=MOVEMENT_TYPE_CHOICES
    )

    quantity = models.DecimalField(
        max_digits=18,
        decimal_places=3
    )

    # Source
    from_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="outgoing_stock_movements"
    )

    from_location = models.ForeignKey(
        StorageLocation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="outgoing_stock_movements"
    )

    # Destination
    to_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="incoming_stock_movements"
    )

    to_location = models.ForeignKey(
        StorageLocation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="incoming_stock_movements"
    )

    reference_number = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "inventory_stock_movements"

        indexes = [
            models.Index(
                fields=["plant", "item"]
            ),
            models.Index(
                fields=["movement_type"]
            ),
            models.Index(
                fields=["created_at"]
            ),
        ]