# Transaction Lock Contention on High-Frequency Order Checkout

## Symptom
Under concurrent checkout requests, API requests hang or fail with database lock wait timeouts or deadlock errors (`Error 1213`).

## Root cause / pattern
Performing network I/O, heavy external requests, or long computations while holding row-level database locks inside `transaction.atomic()` or `select_for_update()`.

## Where it can occur
`orders_billing` module during checkout, payment status updates, or invoice generation.

## Prevention rule
1. Never perform network I/O or heavy non-DB compute inside a database transaction lock window.
2. Execute all validations, price checks, and preparatory steps before acquiring row locks.
3. Keep database lock holding duration strictly under 10 milliseconds.

## Verification steps
Execute concurrent order creation requests and verify transactions complete without lock timeouts.

## Code references
- `backend/billing/services.py`
- `backend/billing/views.py`

## Related modules
- [Orders & Billing](../../orders_billing/module_brain.md)

## Confidence and status
Confirmed. Prevention rule enforced across Axinix platforms.
