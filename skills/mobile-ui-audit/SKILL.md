---
name: mobile-ui-audit
description: Audit, diagnose, compare, plan, or polish native mobile UI/UX across iOS, Android, and HarmonyOS using production-consumer evidence, global-versus-exception ownership, platform-standard controls, accessibility, state coverage, and Device evidence. Use for page reviews, visual regressions, interaction details, screenshot comparisons, or UI experience closure. Do not use for backend, business contracts, analytics, payments, or release-only work.
---

# Mobile UI Audit

Improve observable mobile UI quality without changing business ownership or inventing a parallel design system.

## Establish authority

Read the target repository's current instructions, visual/design-system rules, task contract, validation strategy, and device/build
instructions relevant to the request. The user's current screenshot or reproduction is evidence; repository product contracts and
production behavior remain authority. Generic design guidance and external product comparisons are advisory.

For Byteme Mobile, read [references/byteme-mobile.md](references/byteme-mobile.md) after locating the repository root.

A review-only request is read-only. Planning belongs in the project's canonical truth location; implementation belongs in the
owner-assigned worktree and branch after the project's pickup checks pass.

## Keep the assignment visual

UI scope may change layout, typography, surfaces, icons, accessibility semantics, touch geometry, animation, loading/empty/error
presentation, or interaction feedback. It does not authorize changes to APIs, business state, request counts, route outcomes,
authentication, payment/privacy gates, analytics, deployment, or release configuration.

If a visual fix requires one of those changes, report the exact boundary and stop that slice for owner direction.

## Choose the smallest owner

Classify the symptom before coding:

1. theme/token for a visual invariant shared by unrelated surfaces;
2. shared semantic component for one repeated UI duty;
3. page exception for genuinely task-specific composition;
4. OS/platform-owned UI for selection, keyboard, permissions, share, picker, and system gestures;
5. non-visual authority for data, API/auth, routing, payment, privacy, or business behavior.

Do not treat a shared primitive as a trusted endpoint. If it owns the reported invariant, inspect and guard its internal geometry,
semantics, and states as well as representative production callers.

## Audit in evidence order

1. Reproduce or inspect the production route and state; separate observation from inference.
2. Trace entry, page role, shell, primitive, state branch, and production consumer set.
3. Cover applicable default, loading, empty, error, unauthenticated/refused, success, disabled, destructive, and interrupted states.
4. Check keyboard, Safe Area, back behavior, scroll ownership, system text scaling, accessibility, and touch reachability.
5. Check perceived performance: stable geometry, image reservation, repeated taps, animation interruption, and long-list behavior.
6. Compare mature products, older native versions, web, or mini-program only after understanding the mobile path. Prefer the
   reference that best fits the current mobile user outcome; do not copy Web density by default.

For exhaustive or Device work, read [references/audit-matrix.md](references/audit-matrix.md). For a regression or repeated failed
fix, read [references/regression-closure.md](references/regression-closure.md).

## Decide global versus exception

Prefer a global token or primitive when the same semantic duty occurs on at least three unrelated production surfaces and the
shared layer can stay free of business state, routing, request, payment, or privacy ownership.

Use a named exception for immersive, viewer-like, branded, OS-owned, or task-specific composition. An exception still inherits the
project's typography, semantic colors, Safe Area, system scaling, accessibility, touch, and state-feedback rules unless authority
explicitly says otherwise.

Do not create a universal component with many behavior flags. A small visual responsibility plus explicit composition is usually
more robust.

## Research simply

Start with platform guidance and a few mature products that share the interaction, not a giant style catalog. Record the observed
pattern, why it transfers, and where it does not. Prefer one conservative recommendation over many trend options. External tools or
downloaded UI datasets are optional inputs; this skill must remain useful without them.

## Report and verify

For each material finding, report the surface, symptom, evidence, confidence (`confirmed`, `probable`, `unknown`), short-term fix,
long-term global rule or exception, behavior risk, and required Device evidence. Group repeated symptoms under one root cause.

Use project wrappers and gates. Add a red-capable assertion at the production seam, run focused tests and affected analysis, and
record Development, Integration, Device, and Release separately. Widget evidence cannot close real keyboard, Safe Area, system menu,
physical touch, assistive technology, or platform rendering.

Stop before introducing a new page-shell family, UI dependency, platform channel, dark mode, payment/privacy behavior, or changed
navigation outcome without owner direction.
