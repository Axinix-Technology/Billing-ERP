from django.conf import settings
from django.db import models
from populate_core.registry import register_model


@register_model("order", table_type="transaction", aliases=["orders"])
class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("card", "Card"),
    ]

    bill_number = models.CharField(max_length=64, unique=True, blank=True, default="")
    customer_name = models.CharField(max_length=120, blank=True, default="Walk-in Customer")
    customer_phone = models.CharField(max_length=20, blank=True, default="")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cash",
    )
    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["cashier", "status"]),
            models.Index(fields=["payment_method", "status"]),
        ]

    def __str__(self):
        return self.bill_number


@register_model("order_item", table_type="transaction", aliases=["order_items"])
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )
    product_name = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customization = models.CharField(max_length=255, blank=True, default="")
    status = models.SmallIntegerField(default=1)

    class Meta:
        db_table = "order_items"
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["product", "status"]),
        ]

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
