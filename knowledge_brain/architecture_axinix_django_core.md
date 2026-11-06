# Architecture: Axinix Django Core & Populate Engine

## Overview
Axinix Django Core (`django-populate-core` / `populate_core`) is a 10-stage unified execution kernel for Django enterprise applications.

## Key Principles
1. **Single Entry Point (`/api/populate/`)**: Handles all standard CRUD, filtering, relation prefetching, pagination, and aggregations without repetitive Django views or DRF viewsets.
2. **Domain Services (`services.py`)**: All business logic, validations, state transitions, and lifecycle hooks (`before_create`, `after_create`, `check_permission`, etc.) are declared cleanly in domain services registered with `@register_service("<model>")`.
3. **Fail-Closed ABAC Security**: Fine-grained capability checks and field-level permissions.
4. **Audit Logging**: Automatic persistence of user actions, IP addresses, request IDs, and payload changes to the database audit log.
