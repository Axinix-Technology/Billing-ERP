---
trigger: always_on
---

# UI Formatting Rule: Commercial Data Presentation, Form Layouts & Navigation Integrity

## Rule 1: Zero Values Must Be Rendered as Dash ("—" or "-")
In all data tables, reports, product registries, billing summaries, and KPI metrics:
1. **Never Display Raw "0" or "0.00"**:
   - Zero quantities, zero discount, zero tax, and zero amounts must be displayed as an em-dash (`—`) or hyphen (`-`).
2. **Implementation**:
   - Pass quantities and currency amounts through formatters:
     - `formatQty(val)`: Returns `num.toLocaleString()` or `"—"` if `num === 0 || !num`.
     - `formatCurrency(val)`: Returns `₹...` or `"—"` if `num === 0 || !num`.

## Rule 2: Minimalist Single-Line Metric Summary Bar
1. Avoid tall, multi-card KPI grids that consume vertical screen real estate.
2. Render summaries in a sleek, horizontal, single-line metrics bar to keep tables and data immediately visible above the fold.

## Rule 3: Form Layout Scannability — Single-Row Table Layout (No Chaotic Grids)
1. When a form requires more than a few fields that a human can easily track in a single glance, it MUST be structured as a clean, scan-friendly table layout where **each row has the label in the first column and the input element in the second column**.
2. Avoid multi-column card grids for complex forms; multi-column grids cause visual hunting and jagged horizontal/vertical tracking.
3. Multi-column grids are permitted **only** when a form has 2–3 simple fields that the user can immediately notice and process in one glance.

## Rule 4: Mandatory Field Required Sign (`*`)
1. Every compulsory field must visually feature an unmistakable, prominent red asterisk (`*`) or required tag next to the label (e.g. `<span className="text-red-500 font-bold ml-1">*</span>`).
2. Users must never be left guessing which fields are mandatory.

## Rule 5: Zero Modals/Popups for URL-Based Documents & Entry Forms
1. Never use popup modals or floating overlays for bill receipts, invoice views, customer order summaries, or multi-field creation/edit workflows.
2. Every invoice, bill receipt, and edit workflow MUST be a dedicated separate page with an explicit, bookmarkable URL (e.g. `/orders/invoice?id=123`).
3. Dedicated pages allow bookmarking, team sharing, direct browser reloading, and clean printing.

## Rule 6: Shareable & Traceable URLs (`backTo`, `from`, `redirect`, `search`)
1. All sub-pages, edit forms, and receipt views must consume and propagate navigation parameters:
   - `backTo`: Return path (e.g. `?backTo=/orders` or `?backTo=/pos`).
   - `from`: Originating workflow context (e.g. `from=pos`).
   - `redirect`: Login / auth return target.
   - `search` / filters: Active search queries and category filters stored in URL parameters.
2. The team and operators can copy and share any URL to reproduce the exact state or investigate an issue immediately.

## Rule 7: Zero Developer Instructions & Technical Jargon for Non-Technical Users
1. Never show developer notes, technical setup instructions, database column names, or raw errors (`500 Internal Server Error`, `KeyError`, `NaN`, `undefined`, stack traces) on operator-facing UI.
2. All messages, tooltips, validation alerts, and empty states must use clear, courteous, human-understandable commercial language.
