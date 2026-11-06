# Rule: Auto-Verification & Code Philosophy Audit

## Purpose
Governs how the AI agent approaches development and verification for the Billing-ERP backend (Django + `axinix-django-core` / `populate_core`).

## Core Execution Principles
1. **Pre-code check:** Verify system specifications and existing models before making changes.
2. **Platform Extension vs. Domain Feature:** Controllers are generic (`/api/populate/`); domain business rules live strictly in service hooks (`services.py`).
3. **Audit Logging & Verification:** Every endpoint change must be verified against audit logging compliance, schema constraints, and unit/integration tests.
