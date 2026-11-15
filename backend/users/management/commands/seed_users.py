import sys
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from rest_framework.authtoken.models import Token

from users.models import Role

try:
    from populate_core.models import AccessPolicy, Capability
    HAS_POPULATE_CORE = True
except ImportError:
    HAS_POPULATE_CORE = False

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Seeds, creates, and synchronizes login user credentials for frontend and API testing. "
        "Configures roles, demo accounts ('admin', 'cashier'), custom accounts, and Tier-2 ABAC permissions."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--username",
            type=str,
            help="Create or update a custom user with this username.",
        )
        parser.add_argument(
            "-p",
            "--password",
            type=str,
            help="Password for the custom user (defaults to 'password123' if omitted).",
        )
        parser.add_argument(
            "-r",
            "--role",
            type=str,
            default="admin",
            choices=["admin", "cashier"],
            help="Role for the custom user: 'admin' or 'cashier' (default: 'admin').",
        )
        parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="",
            help="Display name for the custom user.",
        )
        parser.add_argument(
            "--admin-pass",
            type=str,
            default="admin123",
            help="Password to set for 'admin' user (default: 'admin123').",
        )
        parser.add_argument(
            "--cashier-pass",
            type=str,
            default="cashier123",
            help="Password to set for 'cashier' user (default: 'cashier123').",
        )
        parser.add_argument(
            "--keep-passwords",
            action="store_true",
            help="Preserve existing passwords for already registered accounts instead of resetting them.",
        )
        parser.add_argument(
            "--show-tokens",
            action="store_true",
            help="Include DRF authentication token keys in the credential summary.",
        )

    def handle(self, *args, **options):
        custom_username = (options.get("username") or "").strip()
        custom_password = (options.get("password") or "password123").strip()
        custom_role_name = (options.get("role") or "admin").strip().lower()
        custom_name = (options.get("name") or "").strip()

        admin_pw = options.get("admin_pass") or "admin123"
        cashier_pw = options.get("cashier_pass") or "cashier123"
        keep_passwords = options.get("keep_passwords", False)
        show_tokens = options.get("show_tokens", False)

        with transaction.atomic():
            # 1. Ensure Fundamental System Roles Exist
            admin_role, _ = Role.objects.get_or_create(
                name="admin",
                defaults={
                    "description": "Store Manager with full administrative privileges",
                    "is_superadmin": True,
                    "status": 1,
                },
            )
            if not admin_role.is_superadmin or admin_role.status != 1:
                admin_role.is_superadmin = True
                admin_role.status = 1
                admin_role.save(update_fields=["is_superadmin", "status"])

            cashier_role, _ = Role.objects.get_or_create(
                name="cashier",
                defaults={
                    "description": "POS Counter Cashier for billing and order lookup",
                    "is_superadmin": False,
                    "status": 1,
                },
            )
            if cashier_role.status != 1 or cashier_role.is_superadmin:
                cashier_role.status = 1
                cashier_role.is_superadmin = False
                cashier_role.save(update_fields=["status", "is_superadmin"])

            # 2. Provision Tier-2 ABAC Capabilities & Cashier Access Policies
            if HAS_POPULATE_CORE:
                self._provision_abac_policies(cashier_role)

            # 3. Compile User Seed List
            # (username, password, display_name, role_obj, is_superadmin)
            seed_definitions = [
                ("admin", admin_pw, "Store Manager", admin_role, True),
                ("cashier", cashier_pw, "Front Cashier", cashier_role, False),
                ("teashop", "teashop", "Tea Shop Owner", admin_role, True),
                ("teashop123", "teashop123", "Tea Shop Admin", admin_role, True),
            ]

            if custom_username:
                chosen_role = admin_role if custom_role_name == "admin" else cashier_role
                is_super = (custom_role_name == "admin")
                display = custom_name or f"Custom {custom_role_name.capitalize()}"
                seed_definitions.insert(0, (custom_username, custom_password, display, chosen_role, is_super))

            # 4. Upsert Users & Track Results
            seeded_records = []
            for uname, raw_pwd, display_name, role_obj, is_super in seed_definitions:
                record = self._upsert_user(
                    username=uname,
                    raw_password=raw_pwd,
                    display_name=display_name,
                    role_obj=role_obj,
                    is_superadmin=is_super,
                    keep_passwords=keep_passwords,
                )
                seeded_records.append(record)

        # 5. Output Beautiful Terminal Credential Table
        self._print_credential_summary(seeded_records, show_tokens)

    def _upsert_user(self, username, raw_password, display_name, role_obj, is_superadmin, keep_passwords):
        user = User.objects.filter(username__iexact=username).first()
        created = False
        pwd_updated = False

        if not user:
            user = User(username=username)
            created = True

        user.name = display_name or user.name or username
        user.role = role_obj
        user.is_staff = is_superadmin
        user.is_superuser = is_superadmin
        user.is_active = True
        user.is_deleted = False
        user.status = 1

        if created:
            user.set_password(raw_password)
            pwd_updated = True
            user.save()
        else:
            if not keep_passwords:
                user.set_password(raw_password)
                pwd_updated = True
            user.save()

        token_obj, _ = Token.objects.get_or_create(user=user)

        return {
            "user": user,
            "created": created,
            "pwd_updated": pwd_updated,
            "raw_password": raw_password if (created or not keep_passwords) else "[Kept Unchanged]",
            "token": token_obj.key,
        }

    def _provision_abac_policies(self, cashier_role):
        capability_seeds = [
            ("category.read", "read", "View Categories", "View product categories", "products"),
            ("product.read", "read", "View Products", "View POS menu products", "products"),
            ("order.read", "read", "View Orders", "View billing orders and receipts", "billing"),
            ("order.create", "create", "Create Orders", "Create POS billing orders", "billing"),
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

    def _print_credential_summary(self, seeded_records, show_tokens):
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 86))
        self.stdout.write(self.style.SUCCESS("           BILLING-ERP USER CREDENTIALS SEED SETUP - READY FOR FRONTEND"))
        self.stdout.write(self.style.SUCCESS("=" * 86))
        self.stdout.write("")

        headers = ["STATUS", "USERNAME", "PASSWORD", "ROLE", "SUPERADMIN", "NAME"]
        col_format = "{:<10} | {:<12} | {:<14} | {:<9} | {:<10} | {:<20}"

        self.stdout.write(col_format.format(*headers))
        self.stdout.write("-" * 86)

        for item in seeded_records:
            u = item["user"]
            status_tag = "[CREATED]" if item["created"] else ("[UPDATED]" if item["pwd_updated"] else "[UNCHANGED]")
            role_label = u.role.name if u.role else "none"
            super_label = "Yes" if u.is_superadmin else "No"
            pwd_disp = item["raw_password"]

            line = col_format.format(
                status_tag,
                u.username,
                pwd_disp,
                role_label,
                super_label,
                u.name or u.username,
            )
            if item["created"]:
                self.stdout.write(self.style.SUCCESS(line))
            elif item["pwd_updated"]:
                self.stdout.write(self.style.NOTICE(line))
            else:
                self.stdout.write(line)

            if show_tokens:
                self.stdout.write(f"   --> DRF Token: {item['token']}")

        self.stdout.write("=" * 86)
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("Frontend Quick-Login Instructions:"))
        self.stdout.write("  1. Open Frontend: http://localhost:5173 (or http://localhost:5173/login)")
        self.stdout.write("  2. Quick Demo Fill:")
        self.stdout.write("     - Click 'Admin Demo'   -> User: 'admin',   Pass: 'admin123'   (Full Access: POS + Manage + Reports)")
        self.stdout.write("     - Click 'Cashier Demo' -> User: 'cashier', Pass: 'cashier123' (POS Terminal & Order Placement)")
        self.stdout.write("  3. Custom User Creation Example:")
        self.stdout.write("     & <python> manage.py seed_users --username testuser --password secret --role cashier")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Authentication API Endpoints:"))
        self.stdout.write("  - POST /api/auth/login  {\"username\": \"admin\", \"password\": \"admin123\"}")
        self.stdout.write("  - GET  /api/auth/me     Header: Authorization: Bearer <jwt_token>")
        self.stdout.write("=" * 86)
        self.stdout.write("")

