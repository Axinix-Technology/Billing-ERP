# End-to-End Data Flow: Orders & Billing

## 1. Flow 1: POS Order Checkout & Bill Generation

- **Trigger:** Cashier clicks "Complete Order" or "Pay Now" in `CartDrawer.jsx`.
- **Starting Screen:** `frontend/src/components/CartDrawer.jsx`
- **Frontend Logic:**
  - Compiles order payload:
    ```json
    {
      "customer_name": "Walk-in Customer",
      "customer_phone": "9876543210",
      "items": [
        { "product_id": 1, "quantity": 2, "customization": "Extra Ginger" }
      ],
      "discount_percentage": 0,
      "tax_percentage": 5,
      "payment_method": "cash"
    }
    ```
  - Calls `api.createOrder(orderData)`.
- **API Request:**
  - `POST /api/orders`
- **Backend Service / Handler:**
  - `backend/billing/services.py:OrderService.create_order`
  - Validates products exist and are available in `catalog_products`.
  - Calculates subtotal, discount, tax, and grand total authoritatively.
  - Generates unique bill number: `BILL-YYYYMMDD-HHMMSS-RAND`.
  - Executes atomic commit:
    - Inserts `Order` row.
    - Inserts all `OrderItem` rows.
- **Database Entities Involved:**
  - `billing_order`
  - `billing_orderitem`
- **Response Shape:**
  - Status `201 Created`:
    ```json
    {
      "success": true,
      "message": "Order created successfully",
      "order": {
        "id": 101,
        "bill_number": "BILL-20261106-120000-456",
        "customer_name": "Walk-in Customer",
        "grand_total": "42.00",
        "payment_method": "cash",
        "created_at": "2026-11-06T12:00:00Z",
        "items": [...]
      }
    }
    ```
- **State Update & Resulting Screen:**
  - Cart is cleared.
  - Cashier receives confirmation and can open/print invoice.

---

## 2. Flow 2: Invoice Thermal PDF Download

- **Trigger:** Operator clicks "Print Bill" or visits invoice URL.
- **API Request:** `GET /api/orders/<id>/pdf`
- **Backend Handler:** `backend/billing/views.py:download_invoice_pdf`
- **Logic:** Queries order with items, formats 80mm thermal receipt using ReportLab, and streams binary `application/pdf` with `Content-Disposition: inline; filename=invoice-<bill_number>.pdf`.

