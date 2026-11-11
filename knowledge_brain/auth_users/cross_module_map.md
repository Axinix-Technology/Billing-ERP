# Cross-Module Dependency Map: Authentication & Users

## 1. Upstream Dependencies (Modules This Module Depends On)
- **`engine_core` / `populate_core`**:
  - Provides ABAC authorization, token handling, and policy scoping engine.

## 2. Downstream Dependencies (Modules Depending On This Module)
- **`orders_billing`**:
  - Associates orders with `cashier_id` (foreign key to `User`).
  - Validates cashier permissions during checkout.
- **`catalog_products`**:
  - Restricts product creation/modification to users with `admin` role (`is_superadmin`).
- **`reports_analytics`**:
  - Restricts revenue and KPI analytics to administrative users.

## 3. Change-Impact Matrix
| Changed Item | Connected Surface | Why Connected | Required Verification |
|---|---|---|---|
| `User` model schema | `orders_billing:Order.cashier` | ForeignKey relationship | Database migration integrity, cashier order attribution |
| `Role.is_superadmin` logic | `catalog_products`, `reports_analytics` | Guarding administrative workflows | Test that cashier accounts cannot access management or reports |
| JWT Token Payload format | `frontend/src/context/AuthContext.jsx` | Parsing user profile and token | Verify login and page refresh keep user session intact |

