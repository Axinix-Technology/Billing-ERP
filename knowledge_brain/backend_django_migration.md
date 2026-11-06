# Backend: Django Migration & App Layout

## Overview
Migration of the legacy Node.js Express backend (`tea-shop-backend`) to Django 6+ utilizing `django-populate-core`.

## App Layout
- `config/`: Project settings, ASGI/WSGI, root URL routing.
- `users/`: User model (`AUTH_USER_MODEL`), Roles, JWT/Token authentication, profile endpoints.
- `products/`: `Category` and `Product` models and domain services registered with `populate_core`.
- `billing/`: `Order` and `OrderItem` models, bill number generation, transaction management, and billing domain services.
- `reports/`: Analytics aggregation, dashboard KPIs, and PDF export streaming.
- `core/`: Custom middleware (Audit logging, Request ID tracking).
