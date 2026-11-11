# Orders & Billing (`orders_billing`)

## 1. Module Name and Status
- **Canonical Name:** `orders_billing`
- **Status:** Active / Core Module

## 2. Purpose and Business Responsibility
Manages POS shopping cart checkout, atomic database order persistence, sequential bill number generation (`BILL-YYYYMMDD-HHMMSS-RAND`), payment methods (Cash, UPI, Card), discount and tax calculations, and thermal invoice PDF generation.

## 3. Scope
- Order master records (`Order` model: bill_number, customer_name, customer_phone, subtotal, tax_amount, discount_amount, grand_total, payment_method, cashier_id, status, created_at).
- Order line items (`OrderItem` model: order_id, product_id, product_name, quantity, unit_price, total_price, customization).
- POS checkout transaction pipeline with atomic rollback on failures.
- Invoice generation and thermal PDF streaming (`/api/orders/<id>/pdf`).
- Orders history and order lookup by bill number or ID.

## 4. Explicit Non-Scope
- User identity or cashier login sessions (handled by `auth_users`).
- Product pricing definitions and menu items creation (handled by `catalog_products`).
- Broad cross-date financial analytics and charts (handled by `reports_analytics`).

## 5. Main Screens and Entry Points
- POS Checkout Drawer: `frontend/src/components/CartDrawer.jsx`
- Orders History Page: `frontend/src/pages/OrdersPage.jsx`
- Invoice View / Modal: `frontend/src/components/InvoiceModal.jsx` (to be migrated to dedicated page per Commercial Engineering Rules)

## 6. Main User Roles and Permissions
- `cashier`: Governed by DB-backed `AccessPolicy` (`order`: `["read", "create"]`, `order_item`: `["read"]`). Cannot run `report`/`statistics`/`aggregate` (requires `order.report` capability), `update`, or `delete` on orders (`403`).
- `admin`: Superadmin (`is_superadmin = True`). Can view/manage all orders, audit cashier performance, run `/api/populate/report/order`, and re-print invoices.

## 7. Main Workflows and Business Rules
1. **Checkout Calculation:** Subtotal is derived from authoritative product prices.
   - Discount amount: `subtotal * (discount_percentage / 100)`
   - Taxable amount: `max(0, subtotal - discount_amount)`
   - Tax amount: `taxable_amount * (tax_percentage / 100)`
   - Grand total: `taxable_amount + tax_amount`
2. **Server-Side Generation of Bill Number:** Generated as `BILL-YYYYMMDD-HHMMSS-RAND` strictly on the backend inside the transaction.
3. **Atomic Persistence:** Order and all `OrderItems` must commit together inside `transaction.atomic()`.

## 8. Important Validations and Edge Cases
- Cart items list cannot be empty.
- Quantity must be a positive integer $\ge 1$.
- Valid payment methods: `cash`, `upi`, `card`.
- DB lock holding time kept strictly under 10ms per Known Bug Recipe 01.

## 9. Important API/Service/Model References
- Models: `backend/billing/models.py:Order`, `backend/billing/models.py:OrderItem`
- Service: `backend/billing/services.py:OrderService`
- Views:
  - `POST /api/orders` (Create order)
  - `GET /api/orders` (List orders with search)
  - `GET /api/orders/<id>` (Get order details)
  - `GET /api/orders/<id>/pdf` (Stream thermal invoice PDF)

## 10. Dependencies on Other Modules
- `auth_users`: Assigns order to logged-in cashier.
- `catalog_products`: Validates product IDs and prices.

## 11. Known Bug Recipes Relevant to This Module
- [Transaction Lock Contention on High-Frequency Order Checkout](../engine_core/known_bug_recipes/transaction_lock_contention.md)
- [Soft-Delete Index Trap on Active Rows](../engine_core/known_bug_recipes/soft_delete_index_trap.md)

## 12. Related Skills
- [Axinix Core Integration & Service Declaration](../engine_core/skills/axinix_core_integration.md)

## 13. Last Verified Date
- 2026-11-11 (Updated with `PolicyEngine` Tier-2 ABAC + explicit `order.report` capability enforcement).

