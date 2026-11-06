---
trigger: always_on
---

# Agent Rule: Strict Prohibition of Hardcoded Fallbacks in Form State & Post Payloads

## Core Mandate: Zero Mockup Fallbacks in Creation Forms & Mutation Payloads

In all form inputs, create pages, billing checkout forms, product edit pages, and API mutation payloads across the entire ERP:

### 1. Form State Must Initialize with Clean, Empty Primitives
- String fields must strictly initialize to `""` (empty string).
- Optional numerical values must initialize to `""`, `0`, or `null`.
- Array / relational collections must initialize to `[]`.
- Never pre-fill fields with hardcoded sample strings, mockup text, or fake dummy copy.

### 2. Submission Integrity & Database Truth Principle
- Submitted post/put payloads must reflect 100% genuine operator intent or validated database defaults.
- Because this platform is built strictly for commercial business use, mutation payloads (`POST`, `PUT`, `PATCH`) must NEVER inject artificial fallback values, fake strings, or silent defaults.
- If an optional field is left unpopulated by the user, it must be sent as `null` or `""` and handled authoritatively by the backend domain service.

### 3. Explicit, Actionable Error Messages for Non-Technical Users
- Validation errors must never be suppressed, obscured, or rendered as cryptic technical codes or silent failures.
- Every error must explicitly state what field failed, why it failed, and what the operator must do to fix it, in clear human-understandable terms.
