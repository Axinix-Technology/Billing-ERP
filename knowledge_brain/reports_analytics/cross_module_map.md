# Cross-Module Dependency Map: Reports & Analytics

## 1. Upstream Dependencies (Modules This Module Depends On)
- **`orders_billing`**:
  - Consumes `Order` and `OrderItem` tables to aggregate sales metrics, order counts, and item performance.
- **`auth_users`**:
  - Restricts access to operators with `admin` role.

## 2. Downstream Dependencies (Modules Depending On This Module)
- None (terminal reporting module).

## 3. Change-Impact Matrix
| Changed Item | Connected Surface | Why Connected | Required Verification |
|---|---|---|---|
| `Order` payment method choices | `ReportsPage.jsx:paymentBreakdown` | Displaying breakdown percentages | Test chart rendering when new payment methods are used |
| `OrderItem.product_name` | Top selling products table | Displays top products by name | Verify aggregation groups correctly even if product is deleted |
