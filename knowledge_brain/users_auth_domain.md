# Users & Authentication Domain Model

## Overview
Provides identity management, role-based authorization, and token-based authentication.

## Models
- **`Role`**:
  - `name` (CharField, unique: 'admin', 'cashier')
  - `is_superadmin` (BooleanField, default False)
- **`User` (AbstractUser)**:
  - `role` (ForeignKey to `Role`, nullable)
  - `name` (CharField)
  - `is_superadmin` (BooleanField, default False)
  - `created_at` (DateTimeField, auto_now_add=True)
