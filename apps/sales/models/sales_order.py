from django.db import models
class SalesOrder(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        CONFIRMED = "CONFIRMED", "Confirmed"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        PARTIALLY_DELIVERED = (
            "PARTIALLY_DELIVERED",
            "Partially Delivered",
        )
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    # id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False,
    # )
    so_number = models.CharField(max_length=50, unique=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales_orders",
    )

    customer_po = models.ForeignKey(
        CustomerPO,
        on_delete=models.PROTECT,
        related_name="sales_orders",
        null=True,
        blank=True,
    )

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.PROTECT,
        related_name="sales_orders",
        null=True,
        blank=True,
    )

    order_date = models.DateField()
    expected_delivery_date = models.DateField(
        null=True, blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    currency = models.CharField(max_length=3, default="INR")
    payment_terms = models.CharField(max_length=100)

    billing_address = models.TextField()
    shipping_address = models.TextField(blank=True)

    subtotal = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )
    discount_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )
    tax_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )
    grand_total = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.so_number

