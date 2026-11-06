---
trigger: always_on
---

# Axinix Agent Standard — Commercial Engineering Rules

These rules are mandatory for AI agents and developers working on Axinix projects. They define the organization's baseline expectations for commercial software, architecture, data integrity, user experience, diagnostics and project-specific engineering practices.

Apply these rules alongside the project's `knowledge_brain/` and its verified architecture. The actual source code, tests and configuration remain the implementation truth; documentation must be checked against them.

## 1. Commercial software and genuine user input

Axinix applications are built for real commercial use.

- Never populate business forms with fabricated example data such as a person's name, mobile number, email address, address, customer record or transaction value.
- Keep business input fields empty until the user supplies a value.
- Use instructional placeholders that explain what belongs in the field, such as `Enter customer name`, `Enter mobile number` or `Enter email address`.
- Do not use realistic-looking sample values such as `John Hendry` as input placeholders or prefilled values.
- Development and automated tests may use clearly identified fixtures or synthetic test data where required. Such data must never leak into production workflows or be presented as genuine customer/business data.
- Never use dummy IDs, fake records, silent mockups or fabricated values to make a workflow appear complete.

A placeholder is an instruction about the expected input, not an example of a completed record.

## 2. Navigation and page-versus-modal decisions

Navigation must be predictable, shareable and easy to test, support and revisit.

- Give each primary user intention its own URL-addressable page or route.
- Use separate pages for primary create, edit, detail, receipt, invoice, report-breakdown and other substantial workflows.
- Use a modal for a supporting action that is subordinate to the current workflow and does not represent the user's primary intention.
- Example: creating a customer from inside billing may use a modal because the primary task is creating a bill.
- A full product-creation workflow, invoice view or detailed report should have its own page rather than being hidden inside a modal.
- Do not choose a modal merely to avoid implementing a proper route.
- Ensure browser navigation, refresh, bookmarking and direct linking behave consistently for URL-based workflows.

The decision is based on the user's primary intention: primary workflows belong on pages; supporting actions may use modals.

## 3. List pages, search and filtering

A list page is a page where users browse and verify records.

- Except for simple configuration/master lists where the controls provide no practical value, list pages must provide:
  - Date-range selection when records are time-based.
  - Search.
  - Relevant filters.
- Do not add controls mechanically. Choose filters that help users find, compare or verify records.
- Preserve active search, date range and filter state when users navigate away and return.
- Make active filters clear to users, including when they affect exported or printed results.

## 4. Export and print requirements

Every business list must provide appropriate export options.

- Provide print and Excel export for tabular business lists unless a documented technical or product constraint makes one inapplicable.
- Exported data must respect the active search, date range and filters.
- Printed reports must visibly show:
  - The time and date when the print was generated.
  - The selected date range, where applicable.
  - Active filters.
  - Active search criteria, where applicable.
- Present this context clearly enough that a reader can understand exactly which records the printout contains.
- Do not silently export all records when the user has selected a narrower result set.

This is an operational safeguard: users must be able to explain why a record does or does not appear in a printed or exported report.

## 5. Axinix Core is the mandatory Django API platform

Every Django project created for Axinix must use **Axinix Core** as its API platform. This is an organizational requirement, not an optional project preference.

Install the package using the organization's repository:

```bash
pip install "git+ssh://git@github.com/Axinix-Technology/Axinix-Core.git#egg=django-populate-core"
```

Engineering requirements:

- Read the Axinix Core repository's README to understand its installation, conventions and required backend structure.
- Follow the backend structure and API patterns defined by Axinix Core.
- Do not independently introduce a competing API platform or bypass Axinix Core for convenience.
- Before adding or changing API behavior, inspect the installed version and the project's actual Axinix Core integration. Do not assume a capability exists without verifying it.
- If a requirement appears impossible to implement through the established platform, investigate the platform's supported extension points before proposing a separate implementation.

## 6. Populate, domain services and API architecture

Use the Axinix Core Populate request lifecycle and domain services as the default path for application API behavior.

- Populate is not to be treated as CRUD-only when the installed engine and project integration support more complex behavior.
- Put business rules, validation, calculations, state transitions, multi-entity operations and supported integrations in the appropriate domain/service layer.
- Use the platform's supported lifecycle hooks, services, policies and query capabilities rather than duplicating those responsibilities in custom routers or controllers.
- Do not create a separate router/controller merely because the business logic is complex.
- Before creating a custom endpoint, verify whether the requirement can be handled by the existing models, Populate configuration and domain services.
- A separate route/controller may be justified when the required capability cannot appropriately be handled through the platform (for example, a protocol-specific streaming response, an authentication handshake or external webhook signature verification), or when measurement demonstrates a critical performance need.
- Any exception must have a clear technical rationale, a defined scope and appropriate review. Do not use an exception to avoid understanding the existing platform.

This rule does not authorize assuming that every project has identical Populate capabilities. Verify the actual installed Axinix Core version, configuration and supported extension points.

## 7. Root-cause fixes and controlled exceptions

The default engineering approach is to fix the underlying cause and implement a reusable, maintainable solution.

- Do not introduce ad hoc hot patches, temporary bypasses or scattered special cases as a substitute for understanding the root cause.
- Do not use direct hardcoded string comparisons for roles, permissions, statuses or other domain concepts when the project has, or should have, a centralized typed constant, enum, policy, configuration or domain abstraction.
- Do not scatter conditional workarounds across screens, APIs or services to compensate for a broken shared behavior.
- Normal conditional logic that expresses a genuine business rule is allowed. This rule is against brittle, duplicated or bypass-style logic, not against `if` statements as a programming construct.
- When existing code contains a brittle pattern that is relevant to the requested change, identify it and explain the risk even if the user did not explicitly ask for an architecture review.
- Do not silently expand a task into a broad refactor. Explain the issue, impact and proposed scope, then obtain approval where the change goes beyond the authorized request.

### Approval-only exception process

A hot patch or direct comparison that would otherwise violate this rule may be used only after explicit user approval.

Before applying it:
1. Explain why the normal reusable/root-cause solution is not being used.
2. State the exact files, behavior and scope affected.
3. Explain the risks and expected lifetime of the exception.
4. Obtain explicit approval from the user.

Record every approved exception in the project's engineering documentation or change record with:
- The approving user's identity/name as provided in the project context.
- Approval date.
- Reason for approval.
- Exact location and behavior covered.
- Whether the exception is temporary or permanent.
- A removal/review condition or target date for temporary exceptions.

Approval for one exception does not authorize similar exceptions elsewhere. Never claim approval that was not actually given.

## 8. Mutation payload integrity and server-generated values

Mutation requests (`POST`, `PUT` and `PATCH`) must represent the values the user is authorized and intended to submit.

- Do not inject fabricated fallback values, dummy IDs, fake strings or silent mock values into mutation payloads.
- Do not silently replace missing or invalid user input with a different value.
- Required user-entered values must be collected and validated explicitly in the UI and validated again by the backend.
- If a required user value is missing, return a clear validation error rather than inventing a value.
- Do not confuse user-provided data with values generated by the server.

### Server-generated values

Some values must be generated by trusted backend logic rather than supplied by the client.

Examples include:
- A unique bill number or document series.
- Internal identifiers.
- Audit timestamps.
- Derived totals or calculated values that must be authoritative.
- Other system-controlled values defined by the business domain.

Generate these values inside the appropriate backend service or trusted server-side layer. Do not add them artificially to the user's POST payload or represent them as values entered by the user.

The frontend should send only fields the user is permitted to provide. The backend must enforce ownership, permissions, validation and server-side generation.

## 9. Required-field clarity and validation messages

- Mark every required field with an asterisk (`*`) in the UI.
- Make required versus optional fields clear; users must not have to guess.
- Ensure the asterisk has an accessible explanation, such as a form-level `* Required` note.
- Validation errors must identify the field and explain what the user needs to correct.
- Use plain, actionable language. Avoid vague messages such as `Invalid data` when a more useful explanation is available.
- Preserve valid user-entered values when validation fails, unless security or data-integrity requirements require clearing a value.

## 10. Form layout and scanability

The primary objective is to let users scan a form quickly, understand where each value belongs and complete it without confusion.

- Use a structured label-and-input row layout as the default for multi-field business forms.
- Keep each label clearly associated with its corresponding input. A table-like two-column structure is an acceptable default.
- Avoid placing multiple unrelated label/input pairs side by side in dense grids when this makes it difficult to scan across the page or identify which input belongs to which label.
- Do not use a multi-column layout merely to reduce vertical height if it makes the form harder to understand.
- Alternative layouts are allowed when they improve scanability, clarity and efficient use of space without creating ambiguity.
- On smaller screens, adapt the layout while preserving the clear association between each label and its input.
- Provide clear section headings and logical grouping for long forms.
- Do not create unclear forms that force users to guess the next step or the meaning of a field.

## 11. Data-dense, purpose-led UI

Business users need to see and work with information, not navigate decorative containers.

- Prefer clear, data-dense interfaces over excessive whitespace and unnecessarily tall components.
- Avoid unnecessary cards, shadows, borders and background blocks around every component.
- Do not style every label/input pair as a separate colored block.
- Use cards when they serve a clear purpose, such as summarizing dashboard metrics or grouping meaningful dashboard content.
- Do not make ordinary list, detail or data-entry pages look like dashboards made from many decorative cards.
- Use visual emphasis to establish hierarchy and make important information easy to find.
- Reduce unnecessary scrolling without sacrificing readability, spacing, accessibility or clear grouping.
- Do not compress the interface so aggressively that it becomes crowded or difficult to scan.

## 12. Displaying NULL and zero values

For amount and quantity fields in reports and data displays, follow this presentation convention:

- A `NULL` value is displayed as `-`.
- An actual numeric `0` is displayed as blank (`""`).

This is strictly a display rule. Never convert an actual zero to `NULL`, omit it from calculations, or change the stored value merely to achieve the visual presentation.

Apply the convention consistently across relevant tables, summaries, exports and reports. If a particular business context requires users to distinguish an actual zero from a missing value, raise that requirement rather than silently changing the underlying data semantics.

## 13. URL state, traceability and return navigation

Pages should be shareable and should preserve enough context for users, testers and support staff to reproduce a view.

Use URL query parameters or the project's established equivalent to preserve relevant navigation context, including:

- `backTo` — where the user should return.
- `from` — the originating page or workflow.
- `redirect` — an intended next destination, where appropriate.
- `search` — the active search query.
- Active date range, filters, sorting and pagination state where useful.

Requirements:

- A user should be able to copy and share a URL and have the recipient reach the same permitted view and relevant filter/search state.
- Returning from a detail or supporting workflow should restore the user's previous list context where appropriate.
- Browser refresh and direct navigation should preserve URL-backed state.
- Validate and restrict redirect destinations. Never trust arbitrary redirect URLs or introduce open-redirect vulnerabilities.
- Do not put secrets, access tokens, personal data or other sensitive values in query strings.
- Use the application's established routing conventions rather than introducing inconsistent parameter names.

## 14. User-facing language and error handling

The UI is for business users, not developers.

- Never expose developer instructions, implementation notes or internal technical jargon in user-facing screens.
- Never show raw stack traces, exception class names, internal schema names, raw JSON payloads, database errors or internal server details to users.
- Translate technical failures into clear, actionable messages appropriate to the user's task.
- Keep detailed diagnostic information in protected developer/server logs, linked by a correlation/request ID where available.
- Explain what happened and what the user can do next when the application can safely provide that guidance.
- Do not reveal internal implementation details merely because an API returned them.

## 15. Environment-aware diagnostics and logging

Use a consistent diagnostic strategy across development, QA/staging and production.

| Environment | Frontend diagnostics | Backend diagnostics |
|---|---|---|
| Development | Detailed console diagnostics are allowed | Detailed structured logs |
| QA / Staging | Controlled diagnostics useful for testing | Detailed structured logs |
| Production | No debug console output or sensitive diagnostics | Controlled structured server-side logs |

Implementation requirements:

- Do not expose debug output or sensitive API response details in the production UI or browser console.
- Use structured backend logging and appropriate severity levels: `DEBUG`, `INFO`, `WARNING`, `ERROR` and `CRITICAL`.
- Include a request/correlation ID where available so a user-reported issue can be traced across frontend and backend.
- Sanitize credentials, passwords, access tokens, session values, secrets, payment credentials and sensitive personal data before logging.
- Do not log complete request/response bodies indiscriminately. Log only the information necessary for diagnosis and audit, subject to privacy and security requirements.
- Make diagnostic behavior environment-aware through configuration, not scattered hardcoded checks.
- User-facing errors must remain safe and understandable in every environment.

## 16. Implementation planning and verification

Before making functional code changes:

1. Understand the requested outcome and identify the affected workflow.
2. Inspect the relevant Knowledge Brain entries and current implementation.
3. Trace the screen, API, backend service, data model and downstream effects.
4. Identify risks, dependencies and existing patterns that should be reused.
5. Prepare a concise implementation plan and verification plan.
6. Ask for clarification or approval when requirements, permissions or scope are unclear.

After making changes:

1. Review the complete diff.
2. Run relevant automated tests and appropriate manual verification.
3. Verify success, validation failures, permissions and important edge cases.
4. Check that no fabricated values, unauthorized defaults or unintended behavior were introduced.
5. Check the affected screens and responsive layouts.
6. Report what changed, what was tested, what remains unverified and any known limitations.

Do not claim that a change is tested or verified unless the corresponding check was actually performed.

## 17. Knowledge Brain integration

The project Knowledge Brain is governed by the separate Axinix Knowledge Brain standard.

- Before a change, inspect `knowledge_brain/index.md` and the relevant module documents, dependency maps, Known Bug Recipes and Skills.
- Treat source code as the current implementation truth. Investigate and correct stale Knowledge Brain content.
- After meaningful changes, update the relevant module summary, data flow, cross-module map, method index and root index as applicable.
- Do not create standalone Knowledge Brain documents for individual bug fixes. Update the affected module documentation instead.
- Record a reusable, confirmed bug pattern as a Known Bug Recipe.
- Record a reliable, repeatable procedure as a Skill.
- Verify symbol paths and line references after edits; line numbers are hints and must not be trusted without checking.
- Clearly mark unknown, incomplete or unverified information. Never invent architecture, dependencies, historical bugs or procedures.
- Do not store secrets, credentials, customer personal data or sensitive production records in the Knowledge Brain.

Follow the Knowledge Brain standard's initialization, pre-change, post-change and validation workflows. Do not duplicate that entire standard in this file.

## 18. Final agent checklist

Before completing a task, confirm the applicable items:

- [ ] Business forms contain no fabricated prefilled values or realistic fake examples.
- [ ] Placeholders explain what users should enter.
- [ ] Primary workflows have appropriate URL-addressable pages; modals are limited to supporting actions.
- [ ] List pages have useful search, date range and filters, except where those controls are not relevant.
- [ ] Business lists provide appropriate print and Excel exports.
- [ ] Printed output identifies its generation time and active search/filter context.
- [ ] Django projects use Axinix Core as their API platform.
- [ ] API behavior follows the verified Axinix Core and Populate architecture.
- [ ] No unapproved hot patches, brittle direct comparisons or duplicated workarounds were introduced.
- [ ] Mutation payloads contain only authorized user-provided values; server-generated values are created in trusted backend services.
- [ ] Required fields and actionable validation messages are clear.
- [ ] Forms are easy to scan and labels are unambiguously associated with inputs.
- [ ] UI styling emphasizes useful data rather than decorative cards and containers.
- [ ] NULL and actual zero values follow the defined display convention without changing stored data.
- [ ] URLs preserve useful navigation and filter context without exposing sensitive data or permitting unsafe redirects.
- [ ] User-facing screens contain no developer instructions or raw technical errors.
- [ ] Diagnostics follow the environment-specific logging policy and sanitize sensitive data.
- [ ] An implementation and verification plan was followed.
- [ ] Relevant Knowledge Brain entries were reviewed and updated.

---

## Standard maintenance

When changing this standard, preserve its intent and resolve conflicts explicitly rather than silently weakening or expanding a rule. Project-specific constraints may add stricter requirements, but must not contradict this organizational standard without an explicitly approved exception.

**Guiding principle:** Build commercial software that is predictable for users, traceable for support teams, maintainable for engineers and safe to operate.
