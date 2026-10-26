from django.db import models
import uuid

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant

# Category of the Item (Fkey in Item model)
class Category(models.Model):

    id: models.UUIDField = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False
     )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="inventory_categories"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="inventory_categories"
    )

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=50
    )

    description = models.TextField(
        blank=True
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
        db_table = "inventory_categories"

        constraints = [
            models.UniqueConstraint(
                fields=["plant", "code"],
                name="unique_category_code_per_plant"
            )
        ]