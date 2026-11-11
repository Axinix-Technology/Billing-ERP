# Method & Symbol Index: Orders & Billing

| Symbol | Type | File Path | Lines | Responsibility | Related Symbols |
|---|---|---|---|---|---|
| `Order` | Django Model | `backend/billing/models.py` | 6-41 | Master order record with server-generated bill number, customer details, and financial totals (`@register_model("order")`) | `OrderItem`, `User` |
| `OrderItem` | Django Model | `backend/billing/models.py` | 44-67 | Item row linking product, historical price, quantity, and customization (`@register_model("order_item")`) | `Order`, `Product` |
| `OrderService` | Domain Service | `backend/billing/services.py` | 14-228 | Populate service enforcing Tier-2 ABAC (`order.report` capability + `PolicyEngine`), atomic checkout, and report aggregation | `BaseService`, `PolicyEngine` |
| `OrderItemService` | Domain Service | `backend/billing/services.py` | 231-240 | Populate service deferring order item read permissions to `PolicyEngine` | `BaseService` |
| `OrderInvoicePDFView` | APIView | `backend/billing/views.py` | 11-28 | Binary PDF stream endpoint (`GET /api/orders/<id>/pdf`) | `generate_invoice_pdf_bytes` |
| `generate_invoice_pdf_bytes` | Utility Function | `backend/billing/pdf.py` | 9-121 | Generates A4/thermal invoice PDF using ReportLab | `OrderInvoicePDFView` |
| `BillingErpCoreIntegrationTests` | TestCase | `backend/billing/tests.py` | 14-233 | Integration suite testing auth, DB-backed ABAC, populate CRUD, atomic orders, reports, PDFs, and AuditLog | `OrderService`, `ProductService`, `AccessPolicy` |
| `OrdersPage` | React Page Component | `frontend/src/pages/OrdersPage.jsx` | 1-220 | Orders list view with bill search, customer filter, and details view | `api.getOrders` |
| `CartDrawer` | React Component | `frontend/src/components/CartDrawer.jsx` | 1-350 | POS cart summary, discount, tax, payment method selector, and submit | `api.createOrder` |
