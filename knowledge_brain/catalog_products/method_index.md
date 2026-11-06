# Method & Symbol Index: Catalog & Products

| Symbol | Type | File Path | Lines | Responsibility | Related Symbols |
|---|---|---|---|---|---|
| `Category` | Django Model | `backend/products/models.py` | Verify by symbol search | Category model storing name, icon, and status | `Product` |
| `Product` | Django Model | `backend/products/models.py` | Verify by symbol search | Product catalog item storing price, availability, and category link | `Category` |
| `CategoryService` | Domain Service | `backend/products/services.py` | Verify by symbol search | Domain service for categories with Populate pipeline hooks | `BaseService` |
| `ProductService` | Domain Service | `backend/products/services.py` | Verify by symbol search | Domain service enforcing price validation and active status scoping | `BaseService` |
| `POSPage` | React Page Component | `frontend/src/pages/POSPage.jsx` | 1-250 | Main POS ordering interface with category tabs and item grid | `POSItemCard`, `CartDrawer` |
| `MenuManagePage` | React Page Component | `frontend/src/pages/MenuManagePage.jsx` | 1-280 | Admin management screen for creating, updating, and toggling items | `api.createProduct` |
| `POSItemCard` | React Component | `frontend/src/components/POSItemCard.jsx` | 1-90 | Individual product card displaying name, price, and add-to-cart action | `POSPage` |
