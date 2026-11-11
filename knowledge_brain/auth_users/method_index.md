# Method & Symbol Index: Authentication & Users

| Symbol | Type | File Path | Lines | Responsibility | Related Symbols |
|---|---|---|---|---|---|
| `Role` | Django Model | `backend/users/models.py` | 7-20 | System role definition with `is_superadmin` boolean flag | `User` |
| `User` | Django Model | `backend/users/models.py` | 24-47 | Custom user model with display name, role link, and `is_superadmin` property | `Role` |
| `DualTokenAndBearerAuthentication` | DRF Auth Class | `backend/users/authentication.py` | 10-58 | Authenticates Bearer JWT tokens and DRF Token headers | `LoginView` |
| `RoleService` | Domain Service | `backend/users/services.py` | 9-18 | Populate service deferring role access authorization to `PolicyEngine` | `BaseService` |
| `UserService` | Domain Service | `backend/users/services.py` | 21-44 | Populate service deferring user ABAC checks to `PolicyEngine` and hashing passwords | `BaseService` |
| `LoginView` | APIView | `backend/users/views.py` | 25-83 | Authenticates user credentials and issues signed JWT token | `serialize_user` |
| `ProfileView` | APIView | `backend/users/views.py` | 86-99 | Returns authenticated user profile (`/api/auth/me`) | `serialize_user` |
| `LogoutView` | APIView | `backend/users/views.py` | 102-109 | Revokes DRF token on logout (`/api/auth/logout`) | `LoginView` |
| `Command` | Management Command | `backend/users/management/commands/seed_db.py` | 12-156 | Seeds initial roles, default accounts, categories, products, `Capability`, and `AccessPolicy` | `Role`, `User`, `AccessPolicy`, `Capability` |
| `AuthContext` | React Context | `frontend/src/context/AuthContext.jsx` | 1-50 | Manages frontend auth state and token lifecycle | `LoginPage` |
| `LoginPage` | React Page Component | `frontend/src/pages/LoginPage.jsx` | 1-150 | UI form for user login with credentials inputs | `AuthContext` |
