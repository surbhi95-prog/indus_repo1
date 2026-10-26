
import uuid

from django.db import models
from apps.sales.models.quotation import Quotation
from apps.inventory.models.uom import UOM
class QuotationItem(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items",
    )

    item = models.ForeignKey(
        "inventory.Item",
        on_delete=models.PROTECT,
        related_name="quotation_items",
    )

    description = models.TextField(
        blank=True,
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
    )

    uom = models.ForeignKey(
        UOM,
        on_delete=models.PROTECT,
        related_name="quotation_items",
    )

    unit_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    tax_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    line_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # class Meta:
    #     db_table = "quotation_items"
    #     ordering = ["created_at"]

    # def __str__(self):
    #     return f"{self.quotation.quotation_number} - {self.item}"
