# Rule: Frontend Page-Routing Integrity (`src/pages`)

## Purpose
Governs the placement of files in the Frontend codebase to ensure zero route pollution and maintain 100% integrity of the routing structure.

---

## The Golden Rule: Pure Page-Only `src/pages`
**`frontend/src/pages/` MUST contain ONLY top-level page route components that map 1:1 to browser URLs.**

Non-page components, modals, drawers, cards, and utilities must NEVER be placed in `src/pages/`.
- All reusable UI components live in `src/components/`.
- All context providers live in `src/context/`.
- All API callers live in `src/services/`.
