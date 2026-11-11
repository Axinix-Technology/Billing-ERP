# End-to-End Data Flow: Authentication & Users

## 1. Primary Flow: User Login & Session Establishment

- **Trigger:** Operator clicks "Sign In" button on login form.
- **Starting Screen:** `frontend/src/pages/LoginPage.jsx`
- **Frontend Logic:**
  - `LoginPage.jsx` calls `login(username, password)` from `AuthContext.jsx`.
  - Dispatches HTTP POST to `/api/auth/login` via `frontend/src/services/api.js`.
- **API Request:**
  - `POST /api/auth/login`
  - Payload: `{ "username": "admin", "password": "..." }`
- **Backend View / Handler:**
  - `backend/users/views.py:LoginView`
  - Authenticates user via Django `authenticate(username=..., password=...)`.
  - Generates JWT access token containing `{ id, username, role, is_superadmin }`.
- **Database Entities Involved:**
  - `users_user` table (lookup by username/email).
  - `users_role` table (lookup role permissions and flags).
- **Response Shape:**
  - Status `200 OK`:
    ```json
    {
      "success": true,
      "token": "<jwt_string>",
      "user": {
        "id": 1,
        "username": "admin",
        "name": "Administrator",
        "role": "admin"
      }
    }
    ```
- **State Update & Resulting Screen:**
  - `AuthContext.jsx` writes token to `localStorage.setItem('teashop_token', token)`.
  - Sets active `user` state.
  - Operator is redirected to POS billing screen (`/pos` or URL `redirect` param).
- **Error Behavior:**
  - Missing fields: `400 Bad Request` with message "Username and password are required".
  - Invalid credentials: `401 Unauthorized` with message "Invalid username or password".
  - Password inputs are never echoed back.

