from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from populate_core.models import AccessPolicy, Capability

from products.models import Category, Product
from users.models import Role

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds initial roles, default users, product categories, and menu items for Billing-ERP."

    def handle(self, *args, **options):
        with transaction.atomic():
            # 1. Roles
            admin_role, _ = Role.objects.get_or_create(
                name="admin",
                defaults={
                    "description": "Store Manager with full administrative privileges",
                    "is_superadmin": True,
                    "status": 1,
                },
            )
            if not admin_role.is_superadmin:
                admin_role.is_superadmin = True
                admin_role.save(update_fields=["is_superadmin"])

            cashier_role, _ = Role.objects.get_or_create(
                name="cashier",
                defaults={
                    "description": "POS Counter Cashier for billing and order lookup",
                    "is_superadmin": False,
                    "status": 1,
                },
            )

            # 2. Default Accounts
            user_seeds = [
                ("admin", "admin123", "Store Manager", admin_role, True),
                ("cashier", "cashier123", "Front Cashier", cashier_role, False),
                ("teashop", "teashop", "Tea Shop Owner", admin_role, True),
                ("teashop123", "teashop123", "Tea Shop Admin", admin_role, True),
            ]

            for username, raw_pw, display_name, role_obj, is_super in user_seeds:
                user_obj, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "name": display_name,
                        "role": role_obj,
                        "is_staff": is_super,
                        "is_superuser": is_super,
                        "is_active": True,
                        "status": 1,
                    },
                )
                if created:
                    user_obj.set_password(raw_pw)
                    user_obj.save()

            # 3. Categories
            category_seeds = [
                ("Hot Chai", "Coffee"),
                ("Iced Tea & Cold Drinks", "CupSoda"),
                ("Coffee Specialties", "Coffee"),
                ("Snacks & Bites", "Utensils"),
                ("Bakery & Desserts", "Cake"),
            ]

            category_map = {}
            for cat_name, cat_icon in category_seeds:
                cat_obj, _ = Category.objects.get_or_create(
                    name=cat_name,
                    defaults={"icon": cat_icon, "status": 1},
                )
                category_map[cat_name] = cat_obj

            # 4. Products (only seed if table has no active products)
            if not Product.objects.filter(status=1).exists():
                product_seeds = [
                    ("Hot Chai", "Kulhad Masala Chai", Decimal("25.00"), "Traditional spiced milk tea served in clay kulhad cup", "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500"),
                    ("Hot Chai", "Adrak Elaichi Chai", Decimal("20.00"), "Fresh crushed ginger & green cardamom aromatic chai", "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500"),
                    ("Hot Chai", "Cutting Chai", Decimal("15.00"), "Strong Mumbai style half-cup energy tea", "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=500"),
                    ("Hot Chai", "Organic Green Tea", Decimal("35.00"), "Himalayan green tea infused with honey and lemon", "https://images.unsplash.com/photo-1627435601361-ec25f5b1d0e5?w=500"),
                    ("Iced Tea & Cold Drinks", "Lemon Mint Iced Tea", Decimal("45.00"), "Chilled refreshing tea brewed with fresh mint & lemon", "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500"),
                    ("Iced Tea & Cold Drinks", "Peach Hibiscus Cooler", Decimal("60.00"), "Fruity iced tea blend with natural peach syrup", "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500"),
                    ("Coffee Specialties", "Filter Coffee (South Indian)", Decimal("30.00"), "Authentic chicory blend frothed filter coffee", "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500"),
                    ("Coffee Specialties", "Espresso Cappuccino", Decimal("75.00"), "Rich espresso topped with steamed milk froth", "https://images.unsplash.com/photo-1572442388796-11668ba67e53?w=500"),
                    ("Snacks & Bites", "Amul Maska Bun", Decimal("30.00"), "Soft fresh bun loaded with salted Amul butter", "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500"),
                    ("Snacks & Bites", "Crispy Hot Samosa (2 pcs)", Decimal("35.00"), "Golden potato samosas served with spicy mint chutney", "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500"),
                    ("Snacks & Bites", "Cheese Garlic Toast", Decimal("65.00"), "Grilled bread slices with garlic herb butter & melted cheese", "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=500"),
                    ("Bakery & Desserts", "Paneer Tikka Sandwich", Decimal("85.00"), "Grilled multi-grain sandwich filled with spiced paneer", "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500"),
                    ("Bakery & Desserts", "Choco Lava Muffin", Decimal("55.00"), "Warm chocolate muffin with molten fudge center", "https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=500"),
                ]

                Product.objects.bulk_create([
                    Product(
                        category=category_map[cat_name],
                        name=name,
                        price=price,
                        description=desc,
                        image_url=img,
                        is_available=True,
                        status=1,
                    )
                    for cat_name, name, price, desc, img in product_seeds
                ])

            # 5. Tier-2 ABAC Capabilities & Role AccessPolicies
            capability_seeds = [
                ("category.read", "read", "View Categories", "View product categories", "products"),
                ("product.read", "read", "View Products", "View POS menu products", "products"),
                ("product.create", "create", "Create Products", "Create POS menu products", "products"),
                ("product.update", "update", "Update Products", "Update POS menu products", "products"),
                ("product.delete", "delete", "Delete Products", "Delete POS menu products", "products"),
                ("order.read", "read", "View Orders", "View billing orders and receipts", "billing"),
                ("order.create", "create", "Create Orders", "Create POS billing orders", "billing"),
                ("order.report", "report", "Order Reports", "Run aggregate sales analytics and reports", "billing"),
                ("order_item.read", "read", "View Order Items", "View order line items", "billing"),
            ]
            for key, action, label, description, module in capability_seeds:
                Capability.objects.update_or_create(
                    key=key,
                    defaults={
                        "action": action,
                        "label": label,
                        "description": description,
                        "module": module,
                        "type": "business",
                        "status": 1,
                    },
                )

            cashier_policies = [
                ("category", ["read"]),
                ("product", ["read"]),
                ("order", ["read", "create"]),
                ("order_item", ["read"]),
            ]
            for model_name, actions in cashier_policies:
                AccessPolicy.objects.update_or_create(
                    role=cashier_role,
                    model_name=model_name,
                    defaults={
                        "actions": actions,
                        "allow_access": {},
                        "forbidden_access": {},
                        "conditions": {},
                        "status": 1,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Billing-ERP roles, users, categories, products, and ABAC policies."))

