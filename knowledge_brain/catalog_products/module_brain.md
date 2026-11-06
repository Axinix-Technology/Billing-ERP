# Catalog & Products (`catalog_products`)

## 1. Module Name and Status
- **Canonical Name:** `catalog_products`
- **Status:** Active / Core Module

## 2. Purpose and Business Responsibility
Manages tea shop product items, beverage categories, unit prices, product availability toggles, descriptions, and catalog images for POS billing and administration.

## 3. Scope
- Beverage and food categories (`Category` model: name, icon, status).
- Menu items and items catalog (`Product` model: name, price, description, image_url, is_available, category_id, status).
- Category filtering and search query resolution.
- Product availability toggle and pricing updates.

## 4. Explicit Non-Scope
- Shopping cart totals, order checkout, and bill printing (handled by `orders_billing`).
- User authentication and cashier permissions (handled by `auth_users`).
- Sales aggregations and financial reports (handled by `reports_analytics`).

## 5. Main Screens and Entry Points
- Menu Management Page: `frontend/src/pages/MenuManagePage.jsx`
- POS Product Grid & Filter: `frontend/src/pages/POSPage.jsx`
- POS Item Card: `frontend/src/components/POSItemCard.jsx`

## 6. Main User Roles and Permissions
- `cashier`: Read-only access to available products for POS order entry.
- `admin`: Full management rights to create, edit, toggle availability, and delete categories and products.

## 7. Main Workflows and Business Rules
1. **Catalog Browsing:** Cashier filters items by category tab or searches by text on `POSPage.jsx`.
2. **Product Creation/Editing:** Admin uses `MenuManagePage.jsx` to configure item name, category, price, and availability.
3. **Availability Toggle:** Admin toggles `is_available` to immediately hide sold-out items from the active POS view.
4. **Price Integrity:** Prices must be positive numbers; negative or zero pricing is rejected.

## 8. Important Validations and Edge Cases
- Product name and category are compulsory.
- Price must be a valid decimal $\ge 0.00$.
- Soft-delete compound indexing on `[category_id, status]` to prevent full table scans.

## 9. Important API/Service/Model References
- Models: `backend/products/models.py:Category`, `backend/products/models.py:Product`
- Services: `backend/products/services.py:CategoryService`, `backend/products/services.py:ProductService`
- Endpoints:
  - Populate: `POST /api/populate/read/product`, `POST /api/populate/create/product`
  - REST Compatibility: `GET /api/products/categories`, `GET /api/products`, `POST /api/products`, `PUT /api/products/<id>`

## 10. Dependencies on Other Modules
- `auth_users`: Required for role-based mutation access control.

## 11. Known Bug Recipes Relevant to This Module
- [Soft-Delete Index Trap on Active Rows](../engine_core/known_bug_recipes/soft_delete_index_trap.md)

## 12. Related Skills
- [Axinix Core Integration & Service Declaration](../engine_core/skills/axinix_core_integration.md)

## 13. Last Verified Date
- 2026-11-06 (Initial Axinix Django Core specification).
