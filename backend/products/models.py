from django.db import models
from populate_core.registry import register_model


@register_model("category", table_type="master", aliases=["categories"])
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    icon = models.CharField(max_length=64, default="Coffee")
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return self.name


@register_model("product", table_type="master", aliases=["products"])
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, default="")
    image_url = models.CharField(max_length=500, blank=True, default="")
    is_available = models.BooleanField(default=True)
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"
        indexes = [
            models.Index(fields=["category", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return self.name

