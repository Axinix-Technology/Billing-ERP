from decimal import Decimal, InvalidOperation
from django.db.models import Q
from populate_core.registry import BaseService, register_service
from populate_core.response.exceptions import ValidationError


@register_service("category")
class CategoryService(BaseService):
    def check_permission(self, context):
        # Defer authorization cleanly to PolicyEngine (is_superadmin + DB-backed AccessPolicy)
        return None

    def get_policy_scope(self, context):
        return Q(status=1)

    def before_create(self, context, data):
        name = (data.get("name") or "").strip()
        if not name:
            raise ValidationError("Category name is required.")
        data["name"] = name
        return data


@register_service("product")
class ProductService(BaseService):
    def check_permission(self, context):
        # Defer authorization cleanly to PolicyEngine (is_superadmin + DB-backed AccessPolicy)
        return None

    def get_policy_scope(self, context):
        return Q(status=1)

    @staticmethod
    def validate_product_payload(data, is_update=False):
        if not is_update or "name" in data:
            name = (data.get("name") or "").strip()
            if not name:
                raise ValidationError("Product name is required. Please enter a valid item name.")
            data["name"] = name

        if not is_update or "category" in data or "category_id" in data:
            cat_id = data.get("category_id") or data.get("category")
            if not cat_id:
                raise ValidationError("Product category is required. Please select a category.")

        if not is_update or "price" in data:
            raw_price = data.get("price")
            if raw_price is None or raw_price == "":
                raise ValidationError("Product price is required. Please enter an amount.")
            try:
                price_val = Decimal(str(raw_price))
            except (InvalidOperation, ValueError, TypeError):
                raise ValidationError("Product price must be a valid numeric amount (e.g. 25.00).")
            if price_val <= Decimal("0.00"):
                raise ValidationError("Product price must be greater than zero.")
            data["price"] = price_val

        return data

    def before_create(self, context, data):
        return self.validate_product_payload(data, is_update=False)

    def before_update(self, context, instance, data):
        return self.validate_product_payload(data, is_update=True)
