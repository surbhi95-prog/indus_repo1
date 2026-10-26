import uuid

from django.db import models
from apps.sales.models.customer import Customer
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.accounts.models.user_role import UserRole

class Quotation(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
        ("converted", "Converted to Sales Order"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    quotation_number = models.CharField(
        max_length=50,
        unique=True,
    )

    company = models.ForeignKey(
            Company,
            on_delete=models.CASCADE,
            related_name="hrms_shifts"
    )
    
    plant = models.ForeignKey(
            Plant,
            on_delete=models.CASCADE,
            related_name="hrms_shifts"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="quotations",
    )

    quotation_date = models.DateField()

    valid_until = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    currency = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="currency_quotations",
        max_length=3,
        default="INR",
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    tax_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    grand_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    terms_and_conditions = models.TextField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        UserRole,
        on_delete=models.PROTECT,
        related_name="created_quotations",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # class Meta:
    #     db_table = "quotations"
    #     ordering = ["-created_at"]

    # def __str__(self):
    #     return self.quotation_number
