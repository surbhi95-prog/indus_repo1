import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


class UOM(models.Model):

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

    name = models.CharField(
        max_length=50
    )

    code = models.CharField(
        max_length=20
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "inventory_uoms"

        constraints = [
            models.UniqueConstraint(
                fields=["plant", "code"],
                name="unique_uom_code_per_plant"
            )
        ]