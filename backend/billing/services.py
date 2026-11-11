import datetime
import random
from decimal import Decimal, InvalidOperation
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone
from populate_core.policy.engine import PolicyEngine
from populate_core.registry import BaseService, register_service
from populate_core.response.exceptions import AuthorizationError, ValidationError

from products.models import Product
from .models import Order, OrderItem


@register_service("order")
class OrderService(BaseService):
    def check_permission(self, context):
        if getattr(context, "is_superadmin", False):
            return True

        if context.action in ("report", "statistics", "aggregate"):
            if PolicyEngine.has_capability(context, "order.report"):
                return True
            raise AuthorizationError(
                "Store analytics and sales reports require 'order.report' capability.",
                code="PERMISSION_DENIED",
                status_code=403,
            )

        # Defer read/create/update/delete cleanly to PolicyEngine (DB-backed AccessPolicy)
        return None

    def get_policy_scope(self, context):
        return Q(status=1)

    def before_create(self, context, data):
        raw_items = data.get("items")
        if not raw_items or not isinstance(raw_items, list):
            raise ValidationError("Your cart is empty. Please add at least one item before completing the order.")

        # Validate payment method
        payment_method = (data.get("payment_method") or "cash").strip().lower()
        if payment_method not in ("cash", "upi", "card"):
            raise ValidationError("Please select a valid payment method (Cash, UPI, or Card).")
        data["payment_method"] = payment_method

        # Validate discount and tax percentages
        try:
            discount_pct = Decimal(str(data.get("discount_percentage") if data.get("discount_percentage") not in (None, "") else "0"))
            tax_pct = Decimal(str(data.get("tax_percentage") if data.get("tax_percentage") not in (None, "") else "5"))
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError("Discount and tax percentages must be valid numeric values.")

        if discount_pct < Decimal("0") or discount_pct > Decimal("100"):
            raise ValidationError("Discount percentage must be between 0% and 100%.")
        if tax_pct < Decimal("0") or tax_pct > Decimal("100"):
            raise ValidationError("Tax percentage must be between 0% and 100%.")

        # Bulk-fetch referenced products cleanly to avoid N+1 DB queries
        product_ids = []
        for idx, item in enumerate(raw_items, start=1):
            pid = item.get("product_id") or item.get("product")
            if not pid:
                raise ValidationError(f"Line item #{idx} is missing a product identifier.")
            try:
                product_ids.append(int(pid))
            except (ValueError, TypeError):
                raise ValidationError(f"Line item #{idx} has an invalid product identifier.")

        products_map = {
            p.id: p for p in Product.objects.filter(id__in=product_ids, status=1)
        }

        subtotal = Decimal("0.00")
        validated_items = []

        for idx, item in enumerate(raw_items, start=1):
            pid = int(item.get("product_id") or item.get("product"))
            product = products_map.get(pid)
            if not product:
                raise ValidationError(f"Product ID {pid} could not be found or is no longer active.")
            if not product.is_available:
                raise ValidationError(f"'{product.name}' is currently out of stock and cannot be billed.")

            try:
                qty = int(item.get("quantity", 1))
            except (ValueError, TypeError):
                raise ValidationError(f"Quantity for '{product.name}' must be a valid whole number.")

            if qty <= 0:
                raise ValidationError(f"Quantity for '{product.name}' must be at least 1.")

            unit_price = Decimal(str(product.price))
            line_total = (unit_price * qty).quantize(Decimal("0.01"))
            subtotal += line_total

            validated_items.append({
                "product": product,
                "product_name": product.name,
                "quantity": qty,
                "unit_price": unit_price,
                "total_price": line_total,
                "customization": (item.get("customization") or "").strip(),
            })

        discount_amount = (subtotal * discount_pct / Decimal("100")).quantize(Decimal("0.01"))
        taxable_amount = max(Decimal("0.00"), subtotal - discount_amount)
        tax_amount = (taxable_amount * tax_pct / Decimal("100")).quantize(Decimal("0.01"))
        grand_total = (taxable_amount + tax_amount).quantize(Decimal("0.01"))

        # Server-generated bill number (BILL-YYYYMMDD-HHMMSS-RAND)
        now = timezone.localtime(timezone.now())
        date_str = now.strftime("%Y%m%d-%H%M%S")
        rand_num = random.randint(100, 999)
        bill_number = f"BILL-{date_str}-{rand_num}"
        while Order.objects.filter(bill_number=bill_number).exists():
            rand_num = random.randint(100, 999)
            bill_number = f"BILL-{date_str}-{rand_num}"

        customer_name = (data.get("customer_name") or "").strip() or "Walk-in Customer"
        customer_phone = (data.get("customer_phone") or "").strip()

        data["bill_number"] = bill_number
        data["customer_name"] = customer_name
        data["customer_phone"] = customer_phone
        data["subtotal"] = subtotal
        data["discount_amount"] = discount_amount
        data["tax_amount"] = tax_amount
        data["grand_total"] = grand_total
        data["cashier_id"] = getattr(context.user, "id", None)

        context._pending_order_items = validated_items
        return data

    def after_create(self, context, instance):
        pending_items = getattr(context, "_pending_order_items", None)
        if pending_items:
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=instance,
                    product=item["product"],
                    product_name=item["product_name"],
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                    total_price=item["total_price"],
                    customization=item["customization"],
                    status=1,
                )
                for item in pending_items
            ])
        return instance

    def execute_report(self, context, queryset):
        today = timezone.localdate()

        overall = queryset.aggregate(
            total_revenue=Sum("grand_total"),
            total_orders=Count("id"),
            avg_order_value=Avg("grand_total"),
        )

        today_stats = queryset.filter(created_at__date=today).aggregate(
            today_revenue=Sum("grand_total"),
            today_orders=Count("id"),
        )

        payment_breakdown = list(
            queryset.values("payment_method")
            .annotate(count=Count("id"), total=Sum("grand_total"))
            .order_by("-total")
        )

        top_products = list(
            OrderItem.objects.filter(order__in=queryset, status=1)
            .values("product_name")
            .annotate(total_qty=Sum("quantity"), total_sales=Sum("total_price"))
            .order_by("-total_qty")[:5]
        )

        recent_orders = list(
            queryset.order_by("-id")[:10].values(
                "id",
                "bill_number",
                "customer_name",
                "grand_total",
                "payment_method",
                "created_at",
            )
        )

        stats = {
            "total_revenue": float(overall["total_revenue"] or 0),
            "total_orders": int(overall["total_orders"] or 0),
            "avg_order_value": float(overall["avg_order_value"] or 0),
            "today_revenue": float(today_stats["today_revenue"] or 0),
            "today_orders": int(today_stats["today_orders"] or 0),
            "paymentBreakdown": [
                {
                    "payment_method": row["payment_method"],
                    "count": row["count"],
                    "total": float(row["total"] or 0),
                }
                for row in payment_breakdown
            ],
            "topProducts": [
                {
                    "product_name": row["product_name"],
                    "total_qty": int(row["total_qty"] or 0),
                    "total_sales": float(row["total_sales"] or 0),
                }
                for row in top_products
            ],
            "recentOrders": [
                {
                    "id": row["id"],
                    "bill_number": row["bill_number"],
                    "customer_name": row["customer_name"],
                    "grand_total": float(row["grand_total"] or 0),
                    "payment_method": row["payment_method"],
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                }
                for row in recent_orders
            ],
        }

        return {
            "data": stats,
            "count": 1,
            "stats": stats,
        }


@register_service("order_item")
class OrderItemService(BaseService):
    def check_permission(self, context):
        # Defer authorization cleanly to PolicyEngine (DB-backed AccessPolicy)
        return None

    def get_policy_scope(self, context):
        return Q(status=1)

