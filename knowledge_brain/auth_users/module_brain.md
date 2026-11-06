# Authentication & Users (`auth_users`)

## 1. Module Name and Status
- **Canonical Name:** `auth_users`
- **Status:** Active / Core Module

## 2. Purpose and Business Responsibility
Manages user authentication, credentials validation, dual token & JWT sessions, cashier/admin roles, and user context resolution across the Billing-ERP system.

## 3. Scope
- User account creation, update, and lookup (`User` model).
- Role management (`Role` model: `admin`, `cashier`) with `is_superadmin` schema boolean flag.
- Login authentication (`/api/auth/login`) and current user profile retrieval (`/api/auth/me`).
- Password hashing and session token verification.

## 4. Explicit Non-Scope
- Product catalog or inventory definitions (handled by `catalog_products`).
- Order placement, cart management, or payments (handled by `orders_billing`).
- Revenue analytics (handled by `reports_analytics`).

## 5. Main Screens and Entry Points
- Frontend Login Page: `frontend/src/pages/LoginPage.jsx`
- Auth Context Provider: `frontend/src/context/AuthContext.jsx`
- Top Navbar User Profile: `frontend/src/components/Navbar.jsx`

## 6. Main User Roles and Permissions
- `admin`: Superadmin role with full privileges to manage products, view reports, manage cashiers, and configure settings (`is_superadmin = True`).
- `cashier`: Operational role with permissions limited to POS checkout and order entry.

## 7. Main Workflows and Business Rules
1. Operator submits username and password on `LoginPage.jsx`.
2. Backend authenticates credentials, returns JWT token and sanitized user profile (`id`, `username`, `name`, `role`).
3. Frontend stores token in `localStorage('teashop_token')` and mounts `AuthContext`.
4. Role checks determine navigation access to `/manage` and `/reports` (`isAdmin = role === 'admin'`).

## 8. Important Validations and Edge Cases
- Passwords must be hashed using strong algorithm (`bcrypt` / PBKDF2).
- Non-superadmin users cannot elevate privileges or modify roles.
- Invalid credentials return explicit, clear error without leaking user existence.

## 9. Important API/Service/Model References
- Model: `backend/users/models.py:User`, `backend/users/models.py:Role`
- Service: `backend/users/services.py:UserService`
- Auth Views: `backend/users/views.py:LoginView`, `backend/users/views.py:ProfileView`

## 10. Dependencies on Other Modules
- Core Populate Kernel (`populate_core`) for ABAC checks and user session context.

## 11. Known Bug Recipes Relevant to This Module
- [Soft-Delete Index Trap on Active Rows](../engine_core/known_bug_recipes/soft_delete_index_trap.md)

## 12. Related Skills
- [Axinix Core Integration & Service Declaration](../engine_core/skills/axinix_core_integration.md)

## 13. Last Verified Date
- 2026-11-06 (Initial Axinix Django Core specification).
