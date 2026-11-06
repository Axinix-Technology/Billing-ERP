# Known Limitations, Architecture Exceptions & Bug Recipes

This document outlines structural limitations, operational exceptions, and preventative bug recipes for developers and AI agents working with the Populate Engine, Django ORM, and MySQL/SQLite backend in Billing-ERP.

---

## 1. Recipe 01 — Database Lock Contention on High-Frequency Order Transactions

### The Threat
- **Mechanism:** Using `select_for_update()` inside `transaction.atomic()` locks target database rows until the transaction terminates.
- **Production Failure:** If service hooks (`before_*` or `after_*`) perform third-party HTTP requests, slow calculations, or external I/O while holding a row lock, concurrent checkout requests queue up, leading to Deadlock detected and Lock wait timeout exceeded.

### Non-Negotiable Directive
1. **Never perform network I/O or heavy computations inside the transaction lock window.**
2. Execute all validations and pre-computations **before** acquiring the lock.
3. Keep database lock holding duration strictly under **10 milliseconds**.

---

## 2. Recipe 02 — The "Soft-Delete Index Trap" (`status = 1`)

### The Threat
- **Mechanism:** Read queries scope to `WHERE status = 1`.
- **Production Failure:** `status` is a low-cardinality field. In production tables where 95%+ of rows are active, MySQL's query optimizer evaluates a single-column index on `status` as ineffective and drops back to a full table scan.

### Non-Negotiable Directive
1. **Never rely on a standalone `db_index=True` on `status`.**
2. Every high-volume master and transaction table must define compound/composite indexes:
   ```python
   class Meta:
       indexes = [
           models.Index(fields=["status", "created_at"]),
           models.Index(fields=["category_id", "status"]),
       ]
   ```

---

## 3. Recipe 03 — Memory Spikes from Nested `prefetch_related`

### The Threat
- Deep populate requests traverse reverse foreign keys (`orders -> items -> product -> category`).
- Deep queries stitch thousands of model instances in Python process memory, triggering container OOM crashes.

### Non-Negotiable Directive
1. **Hard Ceiling on Populate Depth:** No populate instruction may exceed **3 nested levels**.
2. **Bounded Children Limit:** Nested populated child relations must enforce a default pagination ceiling (maximum **50 records** per parent node).

---

## 4. Recipe 04 — Pipeline Execution CPU Overhead & Dynamic Caching

### The Threat
- Processing pipeline stages dynamically on every request can introduce pure CPU overhead per request.

### Non-Negotiable Directive
1. **Cache Parsed DSL Plans:** For repeated queries, cache the parsed query plan and field projection tokens in an in-process LRU cache.
2. Bypass redundant parsing on cache hit.
