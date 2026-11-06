# AI Agent Rule: Mandatory API Request & Mutation Audit Logging

## Core Policy Directive
In accordance with our platform security and compliance policy, **EVERY API request that enters this system MUST be automatically and immutably persisted into the database audit log (`audit_logs` table)**.

### Mandatory Metadata for Every Audit Record
Every record must capture:
1. **`request_id`**: A unique request correlation ID passed via `X-Request-ID` header (or auto-generated UUID if omitted). Must be echoed back in the response headers.
2. **Who Asked (`user` / `user_name`)**: The authenticated `User` foreign key (if authenticated) and `user_name` (username, email, or "Anonymous" / "System").
3. **From Where Details**:
   - `ip_address`: Real client IP address extracted safely from `X-Forwarded-For` or `REMOTE_ADDR`.
   - `user_agent`: Client device/browser User Agent string.
   - `path`: The exact request URI/endpoint path.
   - `method`: HTTP method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
4. **Operation Details**:
   - `action`: `CREATE`, `UPDATE`, `DELETE`, `READ`, `LOGIN`, `LOGOUT`, etc.
   - `module`: Subsystem module (`billing`, `products`, `orders`, `users`, `reports`, etc.).
   - `entity`: Target entity name or endpoint identifier.
   - `entity_id`: Primary key of affected record (if applicable).
   - `status_code`: HTTP response status code (e.g. 200, 201, 400, 403, 500).
   - `description` / `details`: Clear, human-readable summary of the action and result.
   - `changes`: Request payload or execution metadata with sensitive credentials (passwords, tokens, keys) strictly redacted.

---

## Rules for Populate Engine Routes (`/api/populate/`)
- All requests through the Populate Core automatically execute through Stage 10 (`FinalizationStage`).
- Built-in audit logger handles database insertion directly into `AuditLog`.
- Never bypass or suppress Stage 10 finalization.

---

## Rules for Non-Populate / Custom API Routes
When an API route cannot physically be handled by the Populate Engine (such as authentication handshakes or binary PDF streaming):
1. **Middleware Coverage**:
   - The route must be under `/api/` and processed by `ApiAuditLogMiddleware`.
   - The middleware automatically captures `request_id`, client IP, user agent, action, and persists the audit record.
2. **No Direct Secret Storage**:
   - Always sanitize payloads prior to storage.
