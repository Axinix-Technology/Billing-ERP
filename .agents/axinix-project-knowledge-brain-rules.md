# Project Knowledge Brain & Engineering Knowledge Rules

**Document type:** Mandatory AI-agent standard\
**Applies to:** Every Axinix project, every AI coding agent, and every
human contributor maintaining project knowledge\
**Location in agent-rules repository:**
`knowledge-management/project-knowledge-brain.md`\
**Version:** 1.0\
**Status:** Proposed standard

------------------------------------------------------------------------

## 1. Purpose

Every project must maintain one structured, searchable **Knowledge
Brain** inside the project root.

The Knowledge Brain is the agent's project map. It must help an agent
quickly understand:

-   What modules exist and what each module does.
-   Where important screens, routes, APIs, services, models, jobs and
    shared components are implemented.
-   How data and control flow through the application.
-   Which other modules may be affected when a module changes.
-   Which known bug patterns and regression checks must be considered.
-   Which reusable implementation procedures and engineering skills are
    available.

The Knowledge Brain is not a duplicate of the source code, a general
project diary, or a collection of bug-fix reports. Source code remains
the implementation source of truth. The Knowledge Brain is a concise,
navigable map that points agents to the correct implementation and
explains the relationships that are not obvious from reading one file.

**Mandatory principle:** An agent must read the Knowledge Brain index
and the relevant module knowledge before making a non-trivial change. If
the Knowledge Brain is missing or materially stale, the agent must
initialize or update it before relying on it.

------------------------------------------------------------------------

## 2. Mandatory rules

### Rule 1 --- Maintain an alphabetically ordered index

-   `knowledge_brain/index.md` must list modules in alphabetical order
    by their canonical module name.
-   Keep module names consistent with the project's actual domain and
    navigation terminology.
-   Each entry must link to that module's `module_brain.md`.
-   Add new modules in the correct alphabetical position; do not append
    them at the bottom.
-   Remove or mark retired modules when the application no longer
    contains them.
-   The index must include a short description and module status where
    useful (active, deprecated, internal, or planned).
-   Do not create duplicate entries for the same module under different
    spellings. Record aliases in the module document if needed.

### Rule 2 --- Knowledge Brain documents describe modules, not individual bug fixes

-   Do not create a standalone Knowledge Brain document for each bug
    fix.
-   Module knowledge must describe the module's purpose, behavior, main
    workflows, important rules and implementation locations.
-   A bug fix may require updating the affected module's behavior
    summary, dependency map, method index or data flow.
-   Store reusable, confirmed bug patterns in the Known Bug Recipes
    section/file described below---not as a new module knowledge
    document for every incident.
-   Temporary investigation notes, ticket discussions and one-off
    debugging transcripts do not belong in the Knowledge Brain.

### Rule 3 --- Convert confirmed recurring bugs into Known Bug Recipes

When a bug is fixed and the cause or prevention pattern is sufficiently
understood:

1.  Decide whether it is reusable beyond the specific incident.
2.  If reusable, create or update a concise Known Bug Recipe under the
    engine-core knowledge area.
3.  Record the symptom, likely cause/pattern, affected surfaces,
    prevention rule, verification steps and relevant code references.
4.  Do not include customer secrets, personal data, credentials or
    sensitive production data.
5.  Link the recipe from the relevant module knowledge and/or the
    module's cross-module map where it is relevant.

**Mandatory proactive regression check:** Before implementing or
modifying a page, screen, API, shared component or workflow, the agent
must search the Known Bug Recipes for relevant patterns. It must assess
whether each relevant recipe applies and perform the appropriate
verification. The agent should fix a clearly confirmed, in-scope
recurrence when safe to do so, even if the user did not explicitly
mention that defect. It must not make unrelated or risky changes
silently; report scope expansion and obtain approval where required.

A Known Bug Recipe is a reusable engineering lesson, not a list of every
historical ticket.

### Rule 4 --- Map dependencies and impact paths

Every module must document dependencies and important relationships
across the application.

At minimum, map relevant paths such as:

`Screen / UI → state or controller → service → API / endpoint → backend handler → model / database → response → UI`

Also map reverse impact relationships: if a shared API, model,
component, permission, event, or service changes, which screens and
modules may need verification?

For each important dependency, record:

-   Source module and destination module.
-   Source screen/component/function and target API/service/data entity.
-   Relationship or reason for the dependency.
-   Whether it is direct, indirect, shared, or conditional.
-   Required verification or regression checks when the dependency
    changes.

Do not invent relationships. Verify them in the codebase, routes, API
definitions, imports, tests or runtime behavior. Mark uncertain
relationships as **unverified** and investigate before treating them as
facts.

### Rule 5 --- Maintain a searchable method and symbol index

The Knowledge Brain must point agents to important implementation
symbols.

For important functions, methods, classes, components, routes,
serializers, models, hooks, jobs and event handlers, record:

-   Exact symbol name.
-   File path relative to the repository root.
-   Purpose and responsibility.
-   Start and end line numbers, when they can be verified.
-   Important callers, callees or related symbols where useful.

**Line-number reliability requirement:** Line numbers are navigation
hints, not permanent identifiers. They can change after edits. Agents
must search for the exact symbol and verify its current location before
editing. After modifying a file, refresh the affected line references.
Never rely on an old line range without checking it against the current
source.

Prefer stable symbol names and repository-relative paths alongside line
ranges. Do not index every trivial function; prioritize important entry
points, business logic, shared utilities and cross-module dependencies.

### Rule 6 --- Update knowledge after every development change

At the end of every new feature, enhancement, refactor, bug fix or
meaningful configuration change, the agent must:

1.  Identify which module knowledge is affected.
2.  Update the module summary if behavior or responsibility changed.
3.  Update the data flow if request, state, event or data movement
    changed.
4.  Update the cross-module map if dependencies or impact paths changed.
5.  Update the method index if important symbols or locations changed.
6.  Update the root index if a module was added, renamed, split, merged,
    deprecated or removed.
7.  Update or add a Known Bug Recipe if a reusable bug pattern was
    confirmed.
8.  Run the Knowledge Brain consistency checks described in this
    document.

A task is not complete until the relevant Knowledge Brain updates are
complete, or the agent explicitly reports why no update was necessary.

### Rule 7 --- Use the mandatory module folder structure

The project root must contain the following structure:

``` text
<project-root>/
└── knowledge_brain/
    ├── index.md
    ├── engine_core/
    │   ├── known_bug_recipes/
    │   │   └── index.md
    │   └── skills/
    │       ├── index.md
    │       └── <skill_name>.md
    └── <module_name>/
        ├── cross_module_map.md
        ├── data_flow.md
        ├── method_index.md
        └── module_brain.md
```

-   Use one folder per real application module or bounded domain.
-   Use lowercase `snake_case` for folder names.
-   Each module folder must contain all four required files.
-   If a file has no applicable content yet, create it with a clear
    `Not applicable` or `Not yet mapped` explanation and an owner/next
    action. Do not omit the file.
-   `engine_core` is reserved for project-wide engineering knowledge,
    reusable skills and Known Bug Recipes. It is not a dumping ground
    for unrelated module documentation.
-   If the project has a large number of modules, add sub-indexes only
    when they improve navigation. The root index remains the canonical
    alphabetical entry point.

### Rule 8 --- Turn reusable procedures into Skills

When an agent discovers a reliable, repeatable and useful way to
implement, investigate, test, secure, debug, deploy or operate
something, it must consider capturing the procedure as a Skill.

Store project-specific and Axinix-approved skills under:

`knowledge_brain/engine_core/skills/<skill_name>.md`

Examples include:

-   UI implementation and accessibility.
-   API endpoint implementation.
-   Database migration safety.
-   Authentication and authorization.
-   Secure file upload.
-   Regression test design.
-   Performance investigation.
-   Deployment and rollback.
-   Logging and observability.
-   Framework- or provider-specific procedures.

A Skill must contain a clear use case, prerequisites, step-by-step
procedure, constraints, verification steps, failure modes and
references. It must distinguish mandatory security requirements from
optional implementation preferences.

Do not create a Skill for a one-off workaround, an unverified trick, or
a procedure that is unsafe or contrary to current project standards.

The Skills index must be alphabetically ordered and link to each Skill.
Where appropriate, include the Skill's technology/framework scope and
version assumptions.

**Industry skills:** Skills sourced from external standards or industry
practice may be included only after checking their relevance, currency,
licensing/attribution requirements and compatibility with Axinix
security and engineering standards. Do not blindly copy external
instructions.

------------------------------------------------------------------------

## 3. Required content for each module file

### 3.1 `module_brain.md` --- Module overview and behavior

This is the primary document an agent reads to understand the module.

Required sections:

1.  Module name and status.
2.  Purpose and business responsibility.
3.  Scope: what belongs to this module.
4.  Explicit non-scope: what belongs elsewhere.
5.  Main screens, pages or entry points.
6.  Main user roles and permissions.
7.  Main workflows and business rules.
8.  Important validations and edge cases.
9.  Important API/service/model references.
10. Dependencies on other modules.
11. Known Bug Recipes relevant to this module.
12. Related Skills.
13. Last verified date and source revision/commit, if available.

Keep summaries concise and implementation-oriented. Do not paste entire
source files or reproduce large sections of code.

### 3.2 `data_flow.md` --- End-to-end flow

Document the meaningful flows through the module.

For each flow, include:

-   Flow name and triggering action.
-   Starting screen or entry point.
-   State/controller/hook or frontend logic.
-   API request details (method, route and relevant payload shape,
    without secrets).
-   Backend route/view/handler/service path.
-   Database entities or external systems involved.
-   Response and state update.
-   Resulting screen, notification or side effect.
-   Error, retry, permission and validation behavior.
-   Relevant tests.

Show both successful and important failure paths. Use a small Mermaid
diagram where it improves understanding; keep the written explanation so
the flow remains searchable.

### 3.3 `method_index.md` --- Important code locations

Use a table with columns such as:

  Symbol   Type   File path   Lines   Responsibility   Related symbols
  -------- ------ ----------- ------- ---------------- -----------------

Include important entry points and business logic, not every trivial
helper. Verify current line numbers whenever the file changes. If exact
line numbers cannot be established, record `Verify by symbol search`
rather than guessing.

### 3.4 `cross_module_map.md` --- Dependencies and change impact

Include:

-   Modules this module depends on.
-   Modules that depend on this module.
-   Shared components, APIs, models, permissions, events and services.
-   Screen-to-API-to-backend relationships.
-   Change-impact matrix: what must be checked when a dependency
    changes.
-   Known indirect or conditional relationships.
-   Unverified relationships requiring investigation.

Example:

  -------------------------------------------------------------------------
  Changed item      Connected surface Why it is connected Required
                                                          verification
  ----------------- ----------------- ------------------- -----------------
  Shared customer   Sales screen,     Both consume        Search,
  API               order screen      customer details    selection,
                                                          validation and
                                                          save flows

  Permission helper Admin and user    Controls action     Positive and
                    screens           visibility/access   negative role
                                                          tests
  -------------------------------------------------------------------------

------------------------------------------------------------------------

## 4. Root index format

`knowledge_brain/index.md` must be the first navigation point.

Recommended format:

``` markdown
# Project Knowledge Brain

## How to use this Knowledge Brain
Read the relevant module overview, then inspect its data flow,
method index and cross-module map before changing code.

## Modules (alphabetical)

- [Accounts](accounts/module_brain.md) — Accounting and ledger workflows.
- [Customers](customers/module_brain.md) — Customer records and profiles.
- [Inventory](inventory/module_brain.md) — Stock and inventory operations.
- [Sales](sales/module_brain.md) — Sales and billing workflows.

## Project-wide engineering knowledge

- [Known Bug Recipes](engine_core/known_bug_recipes/index.md)
- [Skills](engine_core/skills/index.md)
```

The names above are examples only. Build the real index from the actual
repository. Do not create fictional modules to fill the list.

------------------------------------------------------------------------

## 5. Known Bug Recipe format

Store recipes in `knowledge_brain/engine_core/known_bug_recipes/`. Use
descriptive filenames in lowercase `snake_case` and maintain an
alphabetical `index.md`.

Recommended recipe structure:

``` markdown
# <Bug Pattern Name>

## Symptom
What a user or tester observes.

## Root cause / pattern
The confirmed underlying cause, or the recurring implementation pattern
that can produce the defect.

## Where it can occur
Relevant modules, screens, APIs, shared components or technology areas.

## Prevention rule
What an agent must inspect or do to avoid introducing the issue.

## Verification steps
Concrete steps or automated tests to confirm the behavior is correct.

## Code references
Repository-relative paths and exact symbols. Treat line numbers as
temporary navigation hints and verify them before use.

## Related modules
Links to relevant module Knowledge Brain documents.

## Confidence and status
Confirmed / probable / retired, with the evidence or reason.
```

Only promote a recipe to `Confirmed` when there is evidence. If the root
cause is not known, describe it as a symptom-based regression check and
do not claim a root cause.

------------------------------------------------------------------------

## 6. Skill document format

Store each Skill at:

`knowledge_brain/engine_core/skills/<skill_name>.md`

Recommended structure:

``` markdown
# <Skill Name>

## Purpose
What repeatable task this Skill helps perform.

## When to use
Applicable scenarios and triggers.

## Scope and assumptions
Framework, language, versions and project conditions.

## Prerequisites
Required context, tools, permissions and inputs.

## Procedure
Ordered, actionable steps.

## Security and safety constraints
Mandatory safeguards, prohibited actions and approval requirements.

## Verification
Tests, checks or evidence required to establish success.

## Common failure modes
Known pitfalls and how to detect them.

## References
Relevant project modules, official documentation and related Skills.

## Maintenance
Owner, version, last verified date and compatibility notes.
```

Skills are reusable procedures; they do not override the Agent Standard,
project security rules, user authorization or approval gates.

------------------------------------------------------------------------

## 7. Agent workflow: initialize the Knowledge Brain

When an agent first encounters a project:

1.  Inspect the repository root, project documentation, framework
    configuration and existing architecture.
2.  Search for an existing `knowledge_brain/` before creating anything.
3.  If it exists, inspect its index and relevant module documents; do
    not overwrite useful knowledge blindly.
4.  Discover actual modules from routes, navigation, feature folders,
    backend apps, API definitions, models, services and tests.
5.  Identify module boundaries based on real responsibilities. Do not
    assume that every folder is a module or that frontend and backend
    folders always represent separate business modules.
6.  Create `knowledge_brain/index.md`,
    `engine_core/known_bug_recipes/index.md` and
    `engine_core/skills/index.md`.
7.  Create the four required files for each identified module.
8.  Map important screens, APIs, backend handlers, data entities, shared
    services and cross-module dependencies.
9.  Index important symbols and verify their file paths and line ranges.
10. Search for existing project bug patterns and reusable procedures in
    the repository and available project documentation. Do not invent
    historical bug recipes or skills.
11. Mark incomplete or unverified areas clearly.
12. Validate links, alphabetical ordering, required files and
    references.
13. Report what was discovered, created, verified and left incomplete.

If the project is too large to map in one pass, initialize the full
index and module skeletons first, then complete modules incrementally.
Clearly mark mapping coverage; never imply the entire project is
documented when only a subset has been inspected.

------------------------------------------------------------------------

## 8. Agent workflow: before changing code

Before implementing a feature, change request, refactor or bug fix:

1.  Read `knowledge_brain/index.md`.
2.  Read the target module's `module_brain.md`.
3.  Read its `data_flow.md`, `method_index.md` and
    `cross_module_map.md`.
4.  Search Known Bug Recipes for relevant symptoms, components, APIs and
    patterns.
5.  Search Skills for applicable implementation or verification
    procedures.
6.  Inspect the actual current source code and verify all paths, symbols
    and line references.
7.  Trace upstream and downstream dependencies to identify affected
    screens, APIs, jobs, permissions and modules.
8.  Define the expected behavior and relevant tests before changing
    code.
9.  If the Knowledge Brain conflicts with source code, treat source code
    as the current implementation truth, investigate the discrepancy and
    update the Knowledge Brain after verification.
10. If a required dependency or behavior is unclear, investigate it or
    explicitly record the uncertainty; do not guess.

------------------------------------------------------------------------

## 9. Agent workflow: after changing code

At the end of every meaningful development task:

1.  Run the relevant tests and verification steps required by the
    project.
2.  Review the actual diff and identify all affected modules and shared
    dependencies.
3.  Update the relevant `module_brain.md` if purpose, behavior,
    workflow, rules or entry points changed.
4.  Update `data_flow.md` if data movement, state transitions, API
    interactions or side effects changed.
5.  Update `method_index.md` for added, removed, renamed or relocated
    important symbols.
6.  Update `cross_module_map.md` for changed dependencies or impact
    paths.
7.  Update the root index for module lifecycle changes.
8.  Add or update a Known Bug Recipe only when a reusable pattern is
    established.
9.  Add or update a Skill only when a reliable procedure is reusable.
10. Refresh line references and validate links.
11. Record the date and source commit/revision where available.
12. Include Knowledge Brain changes in the same pull request as the
    implementation they describe, unless repository policy requires a
    separate coordinated change.
13. In the completion summary, state which Knowledge Brain files were
    updated and which regression recipes were checked.

If no Knowledge Brain update is necessary, state why (for example, a
comment-only change with no behavior, dependency or symbol impact).

------------------------------------------------------------------------

## 10. Accuracy, maintenance and quality controls

-   **Source-backed facts only:** Every implementation claim must be
    traceable to current code, tests, configuration, API definitions or
    verified behavior.
-   **No guessed line numbers:** Never invent line ranges. Reconfirm
    them after edits.
-   **No stale certainty:** If an item has not been checked, mark it
    unverified or last verified at an earlier revision.
-   **No secret material:** Never store tokens, passwords, private keys,
    session data, customer personal data or production records in
    Knowledge Brain files.
-   **No duplicate source code:** Link to code; do not copy large
    implementation blocks into documentation.
-   **No speculative dependencies:** Mark uncertain relationships
    clearly until verified.
-   **No giant documents:** Keep module files focused. Split a genuinely
    large domain into real submodules with clear ownership and links.
-   **Consistent terminology:** Use the same module, API and symbol
    names used by the application.
-   **Version awareness:** Record framework or API version assumptions
    where they materially affect a procedure.
-   **Review changes:** Knowledge Brain updates are code-adjacent
    changes and must be reviewed for accuracy like implementation
    changes.

### Suggested automated validation

Where practical, provide a script or CI check that verifies:

-   Required directory and file structure exists.
-   Every module folder has all four required files.
-   Root and Skills indexes are alphabetically ordered.
-   Markdown links resolve.
-   No duplicate module entries exist.
-   No placeholder text remains in modules marked complete.
-   Referenced files and symbols exist.
-   Line ranges are within current file bounds (a mismatch should
    trigger review, not automatic rewriting).
-   Secret scanning is run against Knowledge Brain changes.

Automated checks can validate structure and references; they cannot
prove that a module description or dependency map is semantically
complete. Human or agent review remains required.

------------------------------------------------------------------------

## 11. Completion checklist

An agent must use this checklist before declaring a Knowledge Brain
initialization or maintenance task complete.

### Initial project setup

-   [ ] Inspected the repository and existing documentation.
-   [ ] Created or reconciled `knowledge_brain/` at the project root.
-   [ ] Created the root alphabetical `index.md`.
-   [ ] Identified actual modules and documented coverage.
-   [ ] Created all four required files for every identified module.
-   [ ] Mapped important screens, APIs, backend handlers and data
    entities.
-   [ ] Recorded important symbols with verified paths and line hints.
-   [ ] Created Known Bug Recipes and Skills indexes without inventing
    entries.
-   [ ] Marked unknown, incomplete and unverified areas.
-   [ ] Validated links, structure and alphabetical ordering.

### After each development task

-   [ ] Read the relevant module knowledge before changing code.
-   [ ] Checked applicable Known Bug Recipes.
-   [ ] Checked applicable Skills.
-   [ ] Verified source code and dependency impact.
-   [ ] Updated all affected Knowledge Brain files.
-   [ ] Refreshed changed symbol line references.
-   [ ] Validated links and required structure.
-   [ ] Reported documentation updates and remaining gaps.

------------------------------------------------------------------------

## 12. Non-negotiable summary

1.  One project-level Knowledge Brain lives at the repository root.
2.  The root module index is alphabetically ordered.
3.  Knowledge Brain documents describe modules and their behavior---not
    individual bug tickets.
4.  Confirmed reusable bug patterns become Known Bug Recipes.
5.  Relevant Known Bug Recipes are proactively checked when pages, APIs,
    shared components or workflows are created or changed.
6.  Every module has `cross_module_map.md`, `data_flow.md`,
    `method_index.md` and `module_brain.md`.
7.  Important symbols are indexed with repository-relative paths and
    verified line hints.
8.  Every meaningful development change triggers a Knowledge Brain
    review and update.
9.  Reusable, verified procedures become Skills under
    `knowledge_brain/engine_core/skills/`.
10. Source code is the implementation truth; the Knowledge Brain must be
    corrected when it becomes stale.
11. Agents must distinguish verified facts from assumptions and
    incomplete mapping.
12. Knowledge Brain content must never contain secrets or sensitive
    production data.

**The expected outcome:** Any authorized human developer or AI agent can
enter an unfamiliar Axinix project, navigate its Knowledge Brain,
understand the relevant module and its dependencies, make a controlled
change, verify the impact and leave the project knowledge more accurate
than before.
