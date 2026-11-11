# End-to-End Data Flow: Catalog & Products

## 1. Flow 1: POS Catalog Hydration & Category Filter

- **Trigger:** Operator opens POS screen or selects a category tab.
- **Starting Screen:** `frontend/src/pages/POSPage.jsx`
- **Frontend Logic:**
  - Calls `api.getCategories()` and `api.getProducts(selectedCategory, searchQuery)`.
- **API Request:**
  - `GET /api/products/categories`
  - `GET /api/products?category_id=1&search=masala`
- **Backend View / Handler:**
  - Route delegates to `backend/products/views.py:get_products` (or `/api/populate/read/product`).
  - Filters by `category_id` and performs case-insensitive substring search on `name` or `description`.
- **Database Entities Involved:**
  - `products_product` table (with `status = 1` and `is_available = True` for POS).
  - `products_category` table.
- **Response Shape:**
  - Status `200 OK`:
    ```json
    {
      "success": true,
      "products": [
        {
          "id": 1,
          "category_id": 1,
          "category_name": "Hot Teas",
          "name": "Masala Chai",
          "price": "20.00",
          "description": "Brewed with ginger, cardamom, and fresh spices",
          "image_url": "https://...",
          "is_available": true
        }
      ]
    }
    ```
- **State Update & Resulting Screen:**
  - `POSPage.jsx` renders product cards grouped by category.
  - Cashier can click an item to add it to `CartDrawer.jsx`.

---

## 2. Flow 2: Product Creation / Update by Admin

- **Trigger:** Admin operator submits the product form on `MenuManagePage.jsx`.
- **Starting Screen:** `frontend/src/pages/MenuManagePage.jsx`
- **Frontend Logic:**
  - Validates required fields (`name`, `category_id`, `price`).
  - Submits payload via `api.createProduct(productData)` or `api.updateProduct(id, productData)`.
- **Backend Service / Lifecycle:**
  - Evaluates `ProductService.before_create(context, data)`.
  - Verifies admin role capability.
  - Sanitizes price to positive float/decimal.
- **Database Mutation:**
  - Inserts or updates row in `products_product`.
- **Response Shape:**
  - `201 Created` / `200 OK`: `{ "success": true, "message": "Product saved successfully" }`.

