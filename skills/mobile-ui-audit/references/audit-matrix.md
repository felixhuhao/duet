# Mobile UI audit matrix

Use this reference for an exhaustive review, screenshot comparison, or Device acceptance. Select only states the product actually
has; do not manufacture scope.

## Journey and state closure

Derive two independent sets:

1. production routes, registries, shared primitives, and their consumers;
2. semantic journeys and applicable states.

For each affected journey, check the relevant dimensions:

| Dimension | Examples |
|---|---|
| Data | initial, loading, populated, empty, stale/refreshing |
| Failure | validation, recoverable error, unauthenticated/refused, invalid link, offline/timeout |
| Action | idle, pressed, loading, disabled, selected, expanded, confirmation, success |
| Content | short/long locale text, large number, long name, missing image, multiple lines |
| Geometry | narrow phone, ordinary phone, large phone, keyboard open, supported landscape |
| Text | normal and large system scaling; no fixed-height clipping or hidden essential value |

A page appearing in a token inventory does not prove it uses the correct semantic role in every state.

## Component and interaction checks

- One page-shell authority, one visible back authority, and one vertical scroll owner.
- The component matches its duty: action, inline link, navigation row, single-target card, multi-action surface, input, selector,
  dialog, sheet, menu, viewer, or OS handoff.
- A global primitive has a production-derived consumer inventory; an exception names what differs and what it still inherits.
- OS-owned menus, gestures, keyboard, permissions, share, and pickers remain standard unless an exact platform gap is reproduced.
- Icons have semantics; text fields have durable labels; raw backend status and internal error vocabulary are not exposed.
- Touch targets meet the target project's rule and nearby actions remain distinguishable.
- Loading preserves geometry, prevents duplicate actions, and does not hide unrelated navigation.
- Focus, dismissal, submit, validation placement, keyboard inset, and bottom-action reachability are coherent.
- Back button, system gesture, deep link, modal dismissal, and success return reach the existing intended destination.
- Images reserve an aspect ratio, define fallback, avoid layout jump, and preserve public/authenticated media boundaries.
- Motion communicates state, remains interruptible, and respects platform reduced-motion behavior where supported.

## Platform Device evidence

| Platform | Typical evidence when affected |
|---|---|
| iOS | Safe Area/notch, keyboard, navigation gesture, Dynamic Type, VoiceOver, system share/menu |
| Android | system/predictive back, keyboard, font scale, TalkBack, popup/sheet geometry |
| HarmonyOS | window inset, keyboard, back gesture, system font scaling, menus/sheets, runtime packaging behavior |

Simulator/emulator evidence helps iteration but does not replace physical-device evidence required by the project.

## Screenshot evidence

Capture only stable states needed to prove the issue and result: default/entry, problematic state, expanded or keyboard state,
narrow/large-text state, and one platform-specific state when behavior differs. Label platform, build/SHA, route, account state,
font scale, and emulator versus physical device. Use test data and exclude personal content.
