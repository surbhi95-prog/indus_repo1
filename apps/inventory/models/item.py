import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.inventory.models.category import Category
from apps.inventory.models.uom import UOM


class Item(models.Model):

    ITEM_TYPE_CHOICES = (
        ("raw_material", "Raw Material"),
        ("consumable", "Consumable"),
        ("spare", "Spare Part"),
        ("finished_goods", "Finished Goods"),
        ("packing", "Packing Material"),
        ("tool", "Tool"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="inventory_items"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="inventory_items"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="items"
    )

    uom = models.ForeignKey(
        UOM,
        on_delete=models.PROTECT,
        related_name="items"
    )

    code = models.CharField(
        max_length=50
    )

    name = models.CharField(
        max_length=255
    )

    item_type = models.CharField(
        max_length=30,
        choices=ITEM_TYPE_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    minimum_stock = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0
    )

    maximum_stock = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0
    )

    is_batch_required = models.BooleanField(
        default=False
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
        db_table = "inventory_items"

        constraints = [
            models.UniqueConstraint(
                fields=["plant", "code"],
                name="unique_item_code_per_plant"
            )
        ]