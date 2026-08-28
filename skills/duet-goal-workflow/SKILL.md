---
name: duet-goal-workflow
description: Create, start, execute, recover, or close a solo Goal under the duet/Herdr workflow. Use when the user mentions duet, Herdr, Goal lifecycle, Goal pickup, worktree ownership, completion evidence, or asks to turn a bounded outcome into a Goal. Do not invoke merely because an ordinary coding task happens to have multiple steps.
---

# Duet Goal Workflow

Own one bounded result from context receipt to honest delivery without making the target repository depend on duet.

## Start from target authority

1. Read the target repository's current instructions and named sources completely.
2. Treat direct user instructions and project rules as authority over this skill.
3. Confirm cwd, branch, base, worktree, write scope, current changes, and external-action permissions.
4. If the project already defines Goal fields or lifecycle states, use them instead of imposing duet vocabulary.

Do not add a duet link or generic process copy to a shared repository unless the repository owner explicitly chooses duet as a
project dependency. Personal workflow belongs in this skill; product and engineering truth belongs in the target repository.

## Write a small Goal

Capture only what must remain stable:

- observable outcome and beneficiary;
- scope and non-goals;
- acceptance criteria that can fail;
- product, data, permission, and compatibility constraints;
- required context, base, owner, branch, worktree, and stop conditions.

Implementation steps, command transcripts, guesses, and tutorials are work notes, not contract. Do not manufacture a Goal for a
one-step answer, read-only lookup, or trivial reversible edit unless the user or project requires it.

## Execute as one owner

The same Goal owner implements, validates, self-checks, and records the completion evidence. Maintain enough state for cold pickup:
current HEAD, completed work, key choices, observed failures, verification results, risks, and next action.

Continue through local, reversible implementation questions. Stop the affected scope when the outcome, user-visible behavior,
shared contract, data, security, permissions, money, another owner's work, or external mutation authority would change.

Read [references/verification.md](references/verification.md) when designing tests, diagnosing a false-green result, or closing a
Goal with layered evidence.

## Keep runtime and delivery separate

Herdr `working/blocked/idle/done/unknown` describes whether the agent can interact. It does not prove Goal completion. Record the
native session for recovery; use Goal artifacts and Git for delivery truth.

An existing or idle agent is not an available resource. Do not send tasks, follow-ups, or review requests to another agent unless
the Goal already records owner preauthorization or the owner explicitly assigns the target seat.

## Finish honestly

Record:

- result and what is now possible;
- commits or artifacts;
- verification commands and exact results;
- unverified Integration, Device, Release, or external-state work;
- remaining risks and next step.

Self-review is the default. Risk can justify stronger evidence or a request to the owner, but does not authorize an independent
reviewer. Merge, push, deployment, release, deletion, messaging, or cross-repository writes still require the target project's and
user's current authorization.
