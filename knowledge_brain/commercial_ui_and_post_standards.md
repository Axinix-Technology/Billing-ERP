# Commercial Post Data & Non-Technical UI Standards

## 1. Commercial-Grade Post Data Integrity
- Zero fallback / zero mockup placeholders in form state and API mutation payloads.
- All payload data must reflect genuine operator intent or verified database defaults.
- Validation errors must be explicit, detailed, and human-understandable so operators know exactly what failed and how to correct it.

## 2. Form Layout & Scannability
- Forms with more than a few fields must use a single-row table layout (Label in Column 1, Input in Column 2) for rapid vertical eye-scanning.
- Multi-column card grids are prohibited for complex forms; permitted only for forms with 2–3 simple fields.

## 3. Mandatory Field Indicators
- Every required input must visually feature a prominent red asterisk (`*`).

## 4. Modal-Free Workflows for Core Documents
- Bill receipts, invoices, and entry forms must be separate, dedicated pages with explicit, bookmarkable URLs.
- Popups/modals lack persistent URLs and impair verification/debugging.

## 5. Traceable URL Navigation
- Sub-pages and edit screens must carry and preserve URL parameters: `backTo`, `from`, `redirect`, and `search`.

## 6. Zero Developer Instructions on Operator UI
- No developer notes, stack traces, database column names, or raw errors on UI screens.
- All text must use professional, courteous commercial language.
