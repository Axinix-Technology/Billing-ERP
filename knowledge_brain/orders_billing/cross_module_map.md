# Cross-Module Dependency Map: Orders & Billing

## 1. Upstream Dependencies (Modules This Module Depends On)
- **`catalog_products`**:
  - `OrderItem.product` foreign key references `Product`.
  - Authoritative prices are read from `Product` on checkout.
- **`auth_users`**:
  - `Order.cashier` references `User`.
- **`engine_core` / `populate_core`**:
  - Transaction and audit logging integration.

## 2. Downstream Dependencies (Modules Depending On This Module)
- **`reports_analytics`**:
  - Reads `Order` and `OrderItem` to compute revenue, order count, and sales trends.

## 3. Change-Impact Matrix
| Changed Item | Connected Surface | Why Connected | Required Verification |
|---|---|---|---|
| `Order.bill_number` format | Thermal invoice PDF & search | Primary search identifier | Verify receipt rendering and search by bill number |
| `Order` financial calculation logic | `reports_analytics` | Revenue totals rely on accurate grand total | Test subtotal, tax, discount, and grand total math with edge cases |
| `payment_method` options | `reports_analytics:paymentBreakdown` | Aggregates count and revenue by payment method | Test adding or updating payment methods reflects in report |
