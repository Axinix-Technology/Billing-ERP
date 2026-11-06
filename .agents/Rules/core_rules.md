---
trigger: always_on
---

# Core Rules & System Directives

These rules are non-negotiable and apply to every agent action in this workspace.

## 1. No Hard Patches
- Do not apply surface-level patches, quick hacks, or temporary bypasses.
- Identify and resolve the root cause cleanly and permanently.

## 2. Living Knowledge Brain with Alphabetical Indexing
- Every update, component, concept, or fix must be documented in `knowledge_brain/`.
- Maintain strict alphabetical order in `knowledge_brain/INDEX.md` for fast scanning and retrieval.

## 3. Knowledge Brain Pre-Verification
- Before implementing any requirement or fix, inspect `knowledge_brain/INDEX.md` and corresponding entries.
- Verify existing patterns, lessons learned, and system specifications.

## 4. Generic Cognitive Architecture (No Code-Based Orchestration)
- Do not build hardcoded procedural orchestration pipelines or rigid code paths.
- Design solutions that empower generic, autonomous reasoning and flexible declarative schemas.

## 5. Mandatory Implementation & Audit Plan
- Do not write or modify functional code without an implementation plan and verification/audit plan.
- Ensure all changes are code-proofed and validated.

## 6. Human-Understandable Language
- Keep all explanations, documentation, and comments crystal clear, descriptive, and human-readable.

## 7. Strict Prohibition on Redundant Routers & Controllers (Populate-Helper + Service First)
- **`populate` is NOT limited to standard CRUD**: Through domain services (`services.py`), the populate pipeline can execute **ANY** complex business logic, validations, state transitions, calculations, multi-collection workflows, third-party integrations, and side effects via lifecycle hooks (`before_create`, `after_create`, `before_update`, `after_update`, `before_read`, `after_read`, `before_delete`, `after_delete`, custom queries/aggregations).
- **Core Architectural Rationale & Inherited Benefits**:
  - Using this pipeline allows every feature and entity to inherit **predefined access policies** (RBAC, field-level allow/forbidden checks), **automatic data sanitization**, **safe aggregation controls**, and **validation security** (correlation IDs, error sanitization, pagination) seamlessly without rewriting them for every endpoint.
- Having custom or complex business logic is **NEVER** a valid reason to create a dedicated controller or router. Custom business logic belongs in the domain service (`services.py`), executed seamlessly within the `/api/populate/` request lifecycle.
- Controllers and routers must **ONLY** be created when a capability **cannot** physically be handled via populate (e.g., binary stream piping/downloads like PDF generation or backup archives, stateful session handshakes in Auth, or external webhook signature verification) or would cause a verified, critical **performance bottleneck**.
- If anything can be handled via `models/` + `populate` + `services.py`, creating a new router or controller is **STRICTLY PROHIBITED**.

## 8. Adherence to Populate Engine Known Limitations & Bug Recipes
- Every developer and AI agent working on backend models, services, or queries must strictly adhere to the bug recipes in [.agents/Rules/known_limitations_and_recipes.md](file:///d:/Axinix%20Projects/Billing-ERP/.agents/Rules/known_limitations_and_recipes.md):
  1. **Minimal Lock Windows**: Never execute network I/O or heavy non-DB compute inside `transaction.atomic()` or while holding row locks (`select_for_update`). Keep DB locks strictly under 10ms.
  2. **Composite Indexes for Soft-Delete**: Never rely on a single-column index on `status`. Always create compound indexes pairing `status` with query keys (e.g. `INDEX(status, tenant_id, created_at)`) to prevent MySQL full table scans.
  3. **Prefetch Memory Safeguards**: Enforce a hard maximum populate depth of 3 levels and a 50-item child pagination ceiling to prevent `prefetch_related` OOM memory crashes.
  4. **Pipeline Caching**: Cache parsed DSL plans and authorization policies in-memory to eliminate pipeline CPU overhead on hot paths.

## 9. Mandatory API Audit Logging on All Custom & Non-Populate API Routes
- **Core Security & Compliance Policy**: Every API request that enters the system must be traceably and immutably audited in the database with:
  1. `request_id`: Unique correlation ID generated or propagated via HTTP header `X-Request-ID`.
  2. **Who Asked** (`user` / `user_name`): Authenticated user instance or username/email (or `'Anonymous'` / `'System'`).
  3. **From Where Details**: Client IP address (`ip_address` extracted safely via `X-Forwarded-For` or `REMOTE_ADDR`), User Agent (`user_agent`), request path (`path`), and HTTP method (`method`).
- **Populate Core Pipeline (`/api/populate/`)**:
  - Automatically audited by Stage 10 (`FinalizationStage`) of the Populate Engine via `populate_core`.
- **Custom / Non-Populate API Routes**:
  - Processed through `ApiAuditLogMiddleware`, which automatically extracts `X-Request-ID`, records `AuditLog` in MySQL/SQLite, and returns the correlation ID in the response.
  - Credential Sanitization: Never write raw passwords, auth tokens, secrets, or financial credentials to the audit log. Always sanitize payload dictionaries prior to storage.

## 10. Commercial-Grade Post Data Integrity, Human Error Explanations & Non-Technical UI Workflow Design
- **Commercial-Grade Post Data Integrity (Zero Fallback / Zero Fake Copy)**:
  - Because this software is built strictly for commercial business production, mutation payloads (`POST`, `PUT`, `PATCH`) must NEVER inject artificial fallback values, fake strings, dummy IDs, or silent mockups.
  - Payload data must represent 100% genuine operator intent and verified database state.
- **Explicit, Human-Understandable Error Messages**:
  - Validation errors must be explicit, crystal clear, and actionable. Never return vague, generic, or silent errors.
  - The user must immediately understand the exact issue (e.g. "Product price must be a positive number greater than ₹0.00" instead of "Invalid input" or "NaN").
- **Mandatory Field Indicators (`*`) on UI**:
  - Every mandatory field on all forms, create screens, modal dialogs, and edit pages MUST visually feature an unmistakable, distinct required marker (e.g. `<span className="text-red-500 font-bold">*</span>`).
  - Operators must never have to guess whether a field is optional or compulsory.
- **Self-Guiding UI Workflows (Zero Guesswork Transitions)**:
  - Operators must never be stranded or forced to guess how to navigate or complete an action.
  - The UI must actively guide the operator through every workflow with clear, contextual primary action buttons (e.g., "Proceed to Payment", "Generate Invoice & Print"), breadcrumbs, back buttons, and step-by-step progression.
  - Every workflow must terminate in a clear confirmation and an intuitive path to the next logical operational task.
- **Strict Prohibition of Developer Instructions & Technical Jargon on UI**:
  - **Zero Technical Instructions for Non-Technical Users**: Never present developer comments, API instructions, setup commands, internal schema field names, or technical implementation notes anywhere in operator-facing UI.
  - **Zero Raw Debug Output**: Raw stack traces, exception classes (`KeyError`, `IntegrityError`, `Undefined`), internal JSON payloads, or HTTP codes (`500 Server Error`) must NEVER be shown on UI screens.
  - All labels, helper texts, empty state messages, error banners, and success notices must be expressed in professional, courteous, non-technical commercial business language.

## 11. Form UI Formatting: Single-Row Table Layout for Human Scannability
- **Scannable Table Layout for Forms with Multiple Fields**:
  - Whenever a form requires more than a few fields that a human can easily track in a single glance, it MUST be structured as a clean, scan-friendly table layout where **each row contains the label in the first column and the input field in the second column**.
  - This provides instantaneous vertical scannability, clear visual alignment, and predictable eye-tracking for commercial operators.
- **Strict Restriction on Multi-Column Grid Forms**:
  - Never use multi-column card grids for complex forms. Multi-column grids cause visual hunting, jagged vertical alignments, and cognitive overload.
  - Multi-column grids are permitted **only** when a form has very few fields (e.g. 2–3 simple fields like a quick discount box or search filter) that the user can immediately notice and process in one glance.

## 12. Strict Prohibition of Popups/Modals for URL-Based Pages & Entry Workflows
- **Zero Modals for Key Commercial Documents & Workflows**:
  - Never use modal popups, floating modal dialogs, or popup overlays for URL-based records such as bill receipts, invoice views, customer order summaries, product creation forms, or report breakdowns.
  - A modal popup destroys browser back-button history, lacks a persistent URL, cannot be reloaded, and cannot be shared across the team for investigation or verification.
- **Mandatory Dedicated Separate Pages**:
  - Every receipt, invoice, entry form, edit workflow, and detailed report MUST be a dedicated separate page with its own bookmarkable, reproducible URL (e.g. `/orders/invoice?id=...`, `/products/create`, `/orders/create`).
  - Dedicated pages provide full scannability, clear breadcrumbs, full keyboard navigation, and predictable printing.

## 13. Canonical URL Query Strings (`backTo`, `from`, `redirect`, `search`) for Traceability & Team Sharing
- **Self-Documenting, Shareable URLs**:
  - All navigation between list pages, detail views, creation pages, and receipt views MUST carry explicit URL parameters:
    1. `backTo`: Defines the return path when the user clicks 'Back' or completes a workflow (e.g. `/orders/invoice?id=123&backTo=/orders`).
    2. `from`: Indicates the initiating workflow or source module (e.g. `from=pos`, `from=orders`).
    3. `redirect`: Used during authentication or guarded routes to return the operator seamlessly to their target page.
    4. `search`: Captures current table filters, search keywords, and category IDs in the URL query string (e.g. `?search=masala&category=1`).
  - This guarantees that operators and QA/development teams can copy, paste, and share the exact URL to reproduce any screen, search state, or workflow investigation instantly.


