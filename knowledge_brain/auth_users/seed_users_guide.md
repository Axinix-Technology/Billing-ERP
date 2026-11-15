# User Credentials & Seed Setup Guide (`seed_users`)

## Overview
The `seed_users` management command creates, synchronizes, and configures login user accounts specifically tailored for testing the Billing-ERP frontend interface (`LoginPage.jsx`) and API authentication (`/api/auth/login`).

Both `python manage.py seed_users` and its alias `python manage.py seed_user_credentials` can be used interchangeably.

---

## Default Accounts Seeded

| Username | Password | Role | Superadmin | Name | Accessible Views |
|---|---|---|---|---|---|
| `admin` | `admin123` | `admin` | Yes | Store Manager | POS Terminal (`/pos`), Store Management (`/manage`), Reports (`/reports`) |
| `cashier` | `cashier123` | `cashier` | No | Front Cashier | POS Counter (`/pos`) & Order creation |
| `teashop` | `teashop` | `admin` | Yes | Tea Shop Owner | All screens & Admin controls |
| `teashop123` | `teashop123` | `admin` | Yes | Tea Shop Admin | All screens & Admin controls |

---

## Execution Commands

### 1. Standard Seed & Password Sync
Ensures roles exist, sets up ABAC policies, creates the demo accounts, and ensures their passwords match the frontend demo defaults:
```powershell
& "backend\.venv\Scripts\python.exe" manage.py seed_users
```

### 2. Create a Custom User on the Fly
Easily provision custom test users with a specific role and password:
```powershell
# Create a custom cashier
& "backend\.venv\Scripts\python.exe" manage.py seed_users -u rajesh -p pass123 -r cashier -n "Rajesh K"

# Create a custom store manager
& "backend\.venv\Scripts\python.exe" manage.py seed_users -u manager1 -p pass123 -r admin -n "Shift Manager"
```

### 3. Custom Passwords for Default Users
```powershell
& "backend\.venv\Scripts\python.exe" manage.py seed_users --admin-pass MyAdminPass99 --cashier-pass CashierPass99
```

### 4. Preserve Existing Passwords
If accounts have already been customized in the database and you only want to insert missing ones without resetting passwords:
```powershell
& "backend\.venv\Scripts\python.exe" manage.py seed_users --keep-passwords
```

### 5. Display DRF Auth Tokens
```powershell
& "backend\.venv\Scripts\python.exe" manage.py seed_users --show-tokens
```

---

## Frontend Integration
1. Launch the React frontend:
   ```powershell
   cd frontend
   npm run dev
   ```
2. Navigate to `http://localhost:5173/login`.
3. Quick-fill credentials using the demo buttons:
   - **Admin Demo** button auto-fills `admin` / `admin123`.
   - **Cashier Demo** button auto-fills `cashier` / `cashier123`.
4. Click **Sign In to Terminal** to authenticate and route to `/pos`.

