from io import StringIO
from django.contrib.auth import authenticate, get_user_model
from django.core.management import call_command
from django.test import TestCase

from users.models import Role

User = get_user_model()


class SeedUsersCommandTests(TestCase):
    def test_seed_users_default_execution(self):
        out = StringIO()
        call_command("seed_users", stdout=out)
        output_text = out.getvalue()

        # Verify output summary
        self.assertIn("BILLING-ERP USER CREDENTIALS SEED SETUP", output_text)
        self.assertIn("admin", output_text)
        self.assertIn("cashier", output_text)

        # Verify roles
        admin_role = Role.objects.get(name="admin")
        self.assertTrue(admin_role.is_superadmin)

        cashier_role = Role.objects.get(name="cashier")
        self.assertFalse(cashier_role.is_superadmin)

        # Verify credentials authenticate correctly
        admin_auth = authenticate(username="admin", password="admin123")
        self.assertIsNotNone(admin_auth)
        self.assertTrue(admin_auth.is_superadmin)

        cashier_auth = authenticate(username="cashier", password="cashier123")
        self.assertIsNotNone(cashier_auth)
        self.assertFalse(cashier_auth.is_superadmin)

    def test_seed_users_custom_account_creation(self):
        out = StringIO()
        call_command(
            "seed_users",
            username="test_supervisor",
            password="SupervisorPass@2026",
            role="admin",
            name="Test Supervisor",
            stdout=out,
        )

        user = authenticate(username="test_supervisor", password="SupervisorPass@2026")
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Test Supervisor")
        self.assertEqual(user.role.name, "admin")
        self.assertTrue(user.is_superadmin)

    def test_seed_user_credentials_alias(self):
        out = StringIO()
        call_command("seed_user_credentials", stdout=out)
        output_text = out.getvalue()
        self.assertIn("BILLING-ERP USER CREDENTIALS SEED SETUP", output_text)

