# Reports & Analytics (`reports_analytics`)

## 1. Module Name and Status
- **Canonical Name:** `reports_analytics`
- **Status:** Active / Core Module

## 2. Purpose and Business Responsibility
Aggregates sales metrics, daily and all-time revenue, average order value, payment method distributions, top-selling tea shop items, and generates exportable sales report PDFs.

## 3. Scope
- Overall KPIs: `total_revenue`, `total_orders`, `avg_order_value`.
- Today's metrics: `today_revenue`, `today_orders`.
- Breakdown by payment method (`cash`, `upi`, `card`).
- Top 5 selling items by quantity and sales volume.
- Recent orders summary table.
- Range-filtered sales report PDF export (`/api/reports/pdf`).

## 4. Explicit Non-Scope
- Order creation or checkout mutations (handled by `orders_billing`).
- Inventory definitions and price updates (handled by `catalog_products`).
- User authentication and login (handled by `auth_users`).

## 5. Main Screens and Entry Points
- Reports Dashboard: `frontend/src/pages/ReportsPage.jsx`

## 6. Main User Roles and Permissions
- `admin`: Exclusive access to revenue analytics and reports dashboard.
- `cashier`: Access prohibited (`403 Forbidden`).

## 7. Main Workflows and Business Rules
1. Admin opens `ReportsPage.jsx`.
2. Frontend queries `GET /api/reports/dashboard`.
3. Displays single-line KPI summary, payment method distribution, and top products.
4. Admin selects date range (Start Date, End Date) and exports PDF via `GET /api/reports/pdf?startDate=...&endDate=...`.

## 8. Important Validations and Edge Cases
- When zero orders exist, revenue returns `0.00` and displays as `—` (dash) per Commercial Engineering Rules.
- Dates must be validated in ISO `YYYY-MM-DD` format.
- Non-admin access strictly rejected with `403 Forbidden`.

## 9. Important API/Service/Model References
- Views:
  - `GET /api/reports/dashboard` (`get_dashboard_stats`)
  - `GET /api/reports/pdf` (`export_sales_report_pdf`)
- PDF Generator: `backend/reports/pdf.py`

## 10. Dependencies on Other Modules
- `orders_billing`: Reads `Order` and `OrderItem` records.
- `auth_users`: Guards access to administrative users.

## 11. Known Bug Recipes Relevant to This Module
- [Soft-Delete Index Trap on Active Rows](../engine_core/known_bug_recipes/soft_delete_index_trap.md)

## 12. Related Skills
- [Axinix Core Integration & Service Declaration](../engine_core/skills/axinix_core_integration.md)

## 13. Last Verified Date
- 2026-11-06 (Initial Axinix Django Core specification).
