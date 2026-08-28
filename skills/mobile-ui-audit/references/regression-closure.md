# Mobile UI regression closure

Use this reference for a user-reported regression, repeated failed fix, or a symptom whose root may be outside the visual layer.

## Preserve exact evidence

Record platform, build/SHA, production route, account state, locale, font scale, and observable state. A screenshot proves the
symptom, not the cause. If the original artifact is unavailable, reproduce the current production path or label the root cause
unknown; do not add speculative hardening.

## Close the correct owner

| Evidence | Preferred owner |
|---|---|
| Same invariant across unrelated surfaces | Theme/token |
| Same semantic duty in repeated places | Shared component |
| Immersive or task-specific composition | Named page exception |
| Selection, keyboard, picker, share, permission, system gesture | OS/platform standard |
| Missing field, auth, API, route, payment, privacy, business state | Non-visual handoff |

Derive consumers from production registries and call sites, not a handwritten test list. For a global fix, cover representative
unrelated consumers and applicable states. For an exception, test the exception and inherited global rules separately.

## Eliminate false green

When the defect survives while tests pass, inspect whether the test:

- checks an allowed token/component rather than the correct semantic role;
- uses another incorrect surface as its expected reference;
- never enters the real production caller or state branch;
- trusts a shared primitive whose internal geometry or semantics are defective;
- proves only “one row,” “no exception,” or “uses AppTypography” without reachability or role relationships.

Replace it with a production-path relationship, state, hierarchy, or geometry assertion that fails on the exact symptom before the
fix.

For edge-sensitive toolbars, assert the full first/last target bounds inside the production viewport. If scrolling is intentional,
prove positive extent, final-target reachability, and a continuation affordance whose visibility follows current scroll state.

For essential values such as balances, prices, quotas, or earnings, “no overflow” is insufficient: ellipsis can hide valid data.
Use reflow or a justified readable scale-down, then assert that a long localized value is not truncated.

## Close narrowly

- `CONFIRMED_AND_FIXED`: reproduced root cause, red assertion, production path fixed.
- `EXISTING_PLATFORM_BEHAVIOR`: standard behavior already exists; preserve evidence, do not duplicate UI.
- `NOT_REPRODUCED_CURRENT_BUILD`: current path works and original artifact is unavailable; no speculative change.
- `BLOCKED_EXTERNAL_AUTHORITY`: evidence points outside UI; hand off without changing behavior.

Always separate Development, Integration, Device, and Release evidence.
