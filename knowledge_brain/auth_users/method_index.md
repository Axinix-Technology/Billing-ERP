# Method & Symbol Index: Authentication & Users

| Symbol | Type | File Path | Lines | Responsibility | Related Symbols |
|---|---|---|---|---|---|
| `User` | Django Model | `backend/users/models.py` | Verify by symbol search | Custom user model with name, role foreign key, and superadmin flag | `Role` |
| `Role` | Django Model | `backend/users/models.py` | Verify by symbol search | System role definition with `is_superadmin` flag | `User` |
| `UserService` | Domain Service | `backend/users/services.py` | Verify by symbol search | Registered service handling user permissions and policies | `BaseService` |
| `LoginView` | APIView | `backend/users/views.py` | Verify by symbol search | Authenticates user credentials and issues JWT token | `api.login` |
| `ProfileView` | APIView | `backend/users/views.py` | Verify by symbol search | Returns authenticated user profile (`/api/auth/me`) | `api.getMe` |
| `AuthContext` | React Context | `frontend/src/context/AuthContext.jsx` | 1-50 | Manages frontend auth state and token lifecycle | `LoginPage` |
| `LoginPage` | React Page Component | `frontend/src/pages/LoginPage.jsx` | 1-150 | UI form for user login with credentials inputs | `AuthContext` |
