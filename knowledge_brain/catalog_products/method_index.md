# Method & Symbol Index: Catalog & Products

| Symbol | Type | File Path | Lines | Responsibility | Related Symbols |
|---|---|---|---|---|---|
| `Category` | Django Model | `backend/products/models.py` | 5-17 | Category model storing name, icon, and status (`@register_model("category")`) | `Product` |
| `Product` | Django Model | `backend/products/models.py` | 20-39 | Product catalog item storing price, availability, and category link (`@register_model("product")`) | `Category` |
| `CategoryService` | Domain Service | `backend/products/services.py` | 7-23 | Populate domain service enforcing category permissions and active scoping | `BaseService` |
| `ProductService` | Domain Service | `backend/products/services.py` | 26-73 | Populate domain service enforcing price validation, admin permissions, and active status scoping | `BaseService` |
| `POSPage` | React Page Component | `frontend/src/pages/POSPage.jsx` | 1-250 | Main POS ordering interface with category tabs and item grid | `POSItemCard`, `CartDrawer` |
| `MenuManagePage` | React Page Component | `frontend/src/pages/MenuManagePage.jsx` | 1-280 | Admin management screen for creating, updating, and toggling items | `api.createProduct` |
| `POSItemCard` | React Component | `frontend/src/components/POSItemCard.jsx` | 1-90 | Individual product card displaying name, price, and add-to-cart action | `POSPage` |
