from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from populate_core.models import AccessPolicy, AuditLog
from populate_core.policy.engine import PolicyEngine
from rest_framework.test import APIClient

from billing.models import Order, OrderItem
from products.models import Category, Product
from users.models import Role

User = get_user_model()


class BillingErpCoreIntegrationTests(TestCase):
    def setUp(self):
        PolicyEngine._policy_cache.clear()
        self.client = APIClient()

        self.admin_role = Role.objects.create(name="admin", is_superadmin=True, status=1)
        self.cashier_role = Role.objects.create(name="cashier", is_superadmin=False, status=1)

        for model_name, actions in [
            ("category", ["read"]),
            ("product", ["read"]),
            ("order", ["read", "create"]),
            ("order_item", ["read"]),
        ]:
            AccessPolicy.objects.create(
                role=self.cashier_role,
                model_name=model_name,
                actions=actions,
                status=1,
            )

        self.admin_user = User.objects.create_user(
            username="admin",
            password="admin123",
            name="Store Manager",
            role=self.admin_role,
            is_superuser=True,
            is_staff=True,
        )
        self.cashier_user = User.objects.create_user(
            username="cashier",
            password="cashier123",
            name="Front Cashier",
            role=self.cashier_role,
        )

        self.cat = Category.objects.create(name="Hot Chai", icon="Coffee", status=1)
        self.prod1 = Product.objects.create(
            category=self.cat,
            name="Kulhad Masala Chai",
            price=Decimal("25.00"),
            is_available=True,
            status=1,
        )
        self.prod2 = Product.objects.create(
            category=self.cat,
            name="Sold Out Tea",
            price=Decimal("30.00"),
            is_available=False,
            status=1,
        )

    def _login(self, username, password):
        res = self.client.post(
            "/api/auth/login",
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        return res.json()["token"]

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "OK")

    def test_auth_login_and_me(self):
        # Missing credentials
        bad_res = self.client.post("/api/auth/login", {"username": ""}, format="json")
        self.assertEqual(bad_res.status_code, 400)
        self.assertIn("username and password", bad_res.json()["message"].lower())

        # Invalid password
        wrong_res = self.client.post(
            "/api/auth/login", {"username": "admin", "password": "wrong"}, format="json"
        )
        self.assertEqual(wrong_res.status_code, 401)

        # Valid login + /api/auth/me
        token = self._login("admin", "admin123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        me_res = self.client.get("/api/auth/me")
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()["user"]["role"], "admin")
        self.assertTrue(me_res.json()["user"]["is_superadmin"])

    def test_populate_catalog_and_permissions(self):
        cashier_token = self._login("cashier", "cashier123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {cashier_token}")

        # Cashier can read categories and products via /api/populate/
        cat_res = self.client.post("/api/populate/read/category", {}, format="json")
        self.assertEqual(cat_res.status_code, 200)
        self.assertTrue(cat_res.json()["success"])
        self.assertEqual(len(cat_res.json()["data"]), 1)

        prod_res = self.client.post(
            "/api/populate/read/product",
            {"populateFields": ["category"]},
            format="json",
        )
        self.assertEqual(prod_res.status_code, 200)
        self.assertEqual(len(prod_res.json()["data"]), 2)

        # Cashier cannot create products
        deny_res = self.client.post(
            "/api/populate/create/product",
            {"category_id": self.cat.id, "name": "Test Tea", "price": "10.00"},
            format="json",
        )
        self.assertEqual(deny_res.status_code, 403)

        # Admin can create products; invalid price fails explicitly
        admin_token = self._login("admin", "admin123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")

        bad_price = self.client.post(
            "/api/populate/create/product",
            {"category_id": self.cat.id, "name": "Free Tea", "price": "-5"},
            format="json",
        )
        self.assertEqual(bad_price.status_code, 400)

        create_res = self.client.post(
            "/api/populate/create/product",
            {"category_id": self.cat.id, "name": "Ginger Chai", "price": "20.00"},
            format="json",
        )
        self.assertEqual(create_res.status_code, 201)
        self.assertEqual(create_res.json()["data"]["name"], "Ginger Chai")

    def test_populate_order_checkout_report_and_pdfs(self):
        cashier_token = self._login("cashier", "cashier123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {cashier_token}")

        # Reject empty cart
        empty_res = self.client.post(
            "/api/populate/create/order",
            {"items": [], "payment_method": "cash"},
            format="json",
        )
        self.assertEqual(empty_res.status_code, 400)

        # Reject out-of-stock item
        oos_res = self.client.post(
            "/api/populate/create/order",
            {"items": [{"product_id": self.prod2.id, "quantity": 1}], "payment_method": "cash"},
            format="json",
        )
        self.assertEqual(oos_res.status_code, 400)

        # Successful atomic order checkout
        order_res = self.client.post(
            "/api/populate/create/order",
            {
                "customer_name": "Arun",
                "customer_phone": "9876543210",
                "payment_method": "upi",
                "discount_percentage": 10,
                "tax_percentage": 5,
                "items": [
                    {"product_id": self.prod1.id, "quantity": 2, "customization": "Less sugar"}
                ],
            },
            format="json",
        )
        self.assertEqual(order_res.status_code, 201)
        order_data = order_res.json()["data"]
        # 2 * 25.00 = 50.00; 10% discount = 5.00; taxable = 45.00; 5% tax = 2.25; grand = 47.25
        self.assertEqual(float(order_data["subtotal"]), 50.00)
        self.assertEqual(float(order_data["discount_amount"]), 5.00)
        self.assertEqual(float(order_data["tax_amount"]), 2.25)
        self.assertEqual(float(order_data["grand_total"]), 47.25)
        self.assertTrue(order_data["bill_number"].startswith("BILL-"))
        self.assertEqual(OrderItem.objects.filter(order_id=order_data["id"]).count(), 1)

        # Invoice PDF binary stream
        pdf_res = self.client.get(f"/api/orders/{order_data['id']}/pdf")
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res["Content-Type"], "application/pdf")
        self.assertTrue(pdf_res.content.startswith(b"%PDF"))

        # Cashier denied report, update, and delete endpoints on order
        rep_deny = self.client.post("/api/populate/report/order", {}, format="json")
        self.assertEqual(rep_deny.status_code, 403)

        upd_deny = self.client.post(
            f"/api/populate/update/order/{order_data['id']}",
            {"customer_name": "Tampered"},
            format="json",
        )
        self.assertEqual(upd_deny.status_code, 403)

        del_deny = self.client.post(
            f"/api/populate/delete/order/{order_data['id']}",
            {},
            format="json",
        )
        self.assertEqual(del_deny.status_code, 403)

        # Admin can run /api/populate/report/order and /api/reports/pdf
        admin_token = self._login("admin", "admin123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")

        rep_res = self.client.post("/api/populate/report/order", {}, format="json")
        self.assertEqual(rep_res.status_code, 200)
        stats = rep_res.json()["data"]
        self.assertEqual(stats["total_orders"], 1)
        self.assertEqual(stats["total_revenue"], 47.25)
        self.assertEqual(len(stats["topProducts"]), 1)

        rep_pdf_res = self.client.get("/api/reports/pdf")
        self.assertEqual(rep_pdf_res.status_code, 200)
        self.assertEqual(rep_pdf_res["Content-Type"], "application/pdf")
        self.assertTrue(rep_pdf_res.content.startswith(b"%PDF"))

        # Verify audit logs recorded
        self.assertGreater(AuditLog.objects.count(), 0)

