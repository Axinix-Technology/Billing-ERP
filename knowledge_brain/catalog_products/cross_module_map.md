# Cross-Module Dependency Map: Catalog & Products

## 1. Upstream Dependencies (Modules This Module Depends On)
- **`auth_users`**:
  - Requires admin role capability to mutate products and categories.
- **`engine_core` / `populate_core`**:
  - Provides query planning, field projection, and cache layer for product reads.

## 2. Downstream Dependencies (Modules Depending On This Module)
- **`orders_billing`**:
  - POS cart checkout resolves items from `Product` to verify current price and availability.
  - `OrderItem` maintains `product_id` foreign key.
- **`reports_analytics`**:
  - Aggregates top-selling products by joining `OrderItem` with `Product`.

## 3. Change-Impact Matrix
| Changed Item | Connected Surface | Why Connected | Required Verification |
|---|---|---|---|
| `Product.price` field | `orders_billing:OrderItem.unit_price` | Source of truth for item price | Ensure existing order totals remain unchanged (captured historically) |
| `Product.is_available` flag | `frontend/src/pages/POSPage.jsx` | Filter criteria | Test that unavailable products do not appear on POS order grid |
| `Category.name` or deletion | `Product.category_id` | Foreign key relationship | Verify CASCADE or PROTECT integrity; categories cannot be deleted with active products |
