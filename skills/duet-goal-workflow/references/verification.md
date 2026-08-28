# Verification discipline

Read this reference when a Goal needs implementation evidence, a regression test, or a completion verdict.

## Prove the action happened

Before interpreting output, verify that the intended command, code path, mock, mutation, or external action actually ran. Inspect
the exit status, affected target, and a positive signal. Empty output can mean “nothing happened,” not success; a write helper can
silently miss its anchor; a mock can be configured but never consumed.

## Build a red-capable signal

Prefer the smallest deterministic check that reaches the production seam and fails on the reported outcome. Confirm at least one
new assertion can turn red before trusting it green. Exact relationships, states, bounds, status codes, and side effects are better
than vague predicates such as “no exception” or “not successful.”

Passing tests are diagnostic evidence only after confirming that their expected values do not preserve the defect. When the user
still sees the bug, inspect the assertion, test host, shared primitive, production caller set, and state branches before adding
speculative hardening.

## Validate boundaries, not every typed call

Validate untrusted inputs at the owning boundary: user input, wire/API, persisted data readback, environment/config, queue or tool
payload, and process edges. Do not scatter duplicate validation across already-typed internal calls. Missing required configuration
must fail visibly or degrade explicitly; silent skipping is not a valid fallback.

For a capability seam, verify Definition, Provider, and Consumer. A type and a reader without a production provider is still an
unwired feature.

## Layer the verdict

Keep Development, Integration, Device, Release, and external state separate. Automated tests do not prove physical-device behavior,
real provider credentials, store review, deployment, push, or a message sent. Report the narrowest result the evidence supports and
name every required layer that remains `NOT_RUN`, failed, or externally blocked.
