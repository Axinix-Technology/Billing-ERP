# Axinix Core Integration & Service Declaration

## Purpose
Establishes the step-by-step procedure for integrating the `django-populate-core` (`populate_core`) platform into Django projects, registering data models, and declaring domain services with lifecycle hooks.

## When to use
Whenever adding or updating Django backend models, business logic services, or exposing API resources under the unified `/api/populate/` pipeline.

## Scope and assumptions
- Django 5.0+ or 6.0+
- `django-populate-core` installed via pip
- REST Framework installed and configured

## Prerequisites
- Active Python virtual environment (`.venv`)
- `D:\Axinix Projects\Axinix-Core` available locally or via git repository

## Procedure
1. **Package Installation**:
   ```bash
   pip install "git+ssh://git@github.com/Axinix-Technology/Axinix-Core.git#egg=django-populate-core"
   # Or locally during development:
   pip install -e "D:\Axinix Projects\Axinix-Core"
   ```
2. **Settings Configuration**:
   Add `'populate_core'` to `INSTALLED_APPS` and define `POPULATE_CONFIG`:
   ```python
   INSTALLED_APPS = [..., 'rest_framework', 'rest_framework.authtoken', 'populate_core']
   POPULATE_CONFIG = {
       'ROLE_MODEL': 'users.Role',
       'SUPERADMIN_ROLE_FLAG': 'is_superadmin',
       'MAX_PREFETCH_DEPTH': 3,
       'CHILD_PAGINATION_CEILING': 50,
   }
   ```
3. **Mount URLs**:
   ```python
   path('api/populate/', include(('populate_core.urls', 'populate'), namespace='populate'))
   ```
4. **Model & Service Registration**:
   Decorate models with `@register_model("<name>")` and services with `@register_service("<name>")` subclassing `BaseService`.
5. **App Ready Hook**:
   Import `services` inside `apps.py` `ready()` method to ensure registry discovery on startup.

## Security and safety constraints
- Never bypass the 10-stage pipeline by inventing redundant views/routers for standard CRUD.
- Enforce ABAC capability checks in `check_permission` and filter querysets with `get_policy_scope`.

## Verification
- Test query via `POST /api/populate/read/<model_name>`.
- Verify JSON response follows standard `{ success: true, data: [...], count: N }`.

## Common failure modes
- Failing to import `services.py` inside `apps.py` `ready()` results in `Model not registered` errors.

