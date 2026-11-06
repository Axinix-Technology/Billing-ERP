# Soft-Delete Index Trap on Active Rows

## Symptom
Full table scans occur on queries filtering by `status = 1` as the table grows, causing slow API responses.

## Root cause / pattern
`status` is a low-cardinality column (`0` or `1`). When 95%+ of rows are active (`status = 1`), MySQL ignores single-column indexes on `status` and performs a full table scan.

## Where it can occur
`catalog_products`, `orders_billing`, and any model utilizing soft-delete or active status flags.

## Prevention rule
Never rely on a standalone `db_index=True` on `status`. Always create compound indexes pairing `status` with query keys (e.g. `[status, created_at]`, `[category_id, status]`).

## Verification steps
Run `EXPLAIN` on queries filtering by `status` to ensure compound index lookup is used instead of table scans.

## Code references
- `backend/products/models.py`
- `backend/billing/models.py`

## Related modules
- [Catalog & Products](../../catalog_products/module_brain.md)
- [Orders & Billing](../../orders_billing/module_brain.md)

## Confidence and status
Confirmed. Required indexing standard across Axinix platforms.
