# Method & Symbol Index: Orders & Billing

| Symbol | Type | File Path | Lines | Responsibility | Related Symbols |
|---|---|---|---|---|---|
| `Order` | Django Model | `backend/billing/models.py` | Verify by symbol search | Master order record with bill number, customer details, and financial totals | `OrderItem`, `User` |
| `OrderItem` | Django Model | `backend/billing/models.py` | Verify by symbol search | Item row linking product, historical price, quantity, and customization | `Order`, `Product` |
| `OrderService` | Domain Service | `backend/billing/services.py` | Verify by symbol search | Transactional checkout service, bill number generator, and price calculator | `BaseService` |
| `download_invoice_pdf` | View / Controller | `backend/billing/views.py` | Verify by symbol search | Generates and streams ReportLab thermal receipt PDF | `generate_invoice_pdf` |
| `OrdersPage` | React Page Component | `frontend/src/pages/OrdersPage.jsx` | 1-220 | Orders list view with bill search, customer filter, and details drawer | `api.getOrders` |
| `CartDrawer` | React Component | `frontend/src/components/CartDrawer.jsx` | 1-350 | POS cart summary, discount, tax, payment method selector, and submit | `api.createOrder` |
| `InvoiceModal` | React Component | `frontend/src/components/InvoiceModal.jsx` | 1-180 | Receipt preview modal (to be converted to dedicated `/orders/invoice` page) | `api.getInvoicePdfUrl` |
