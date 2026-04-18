# Task Control Documents

Use this structure for substantial or multi-session work in this repository. These files are coordination surfaces, not append-only transcripts.

## File Roles

### `SPEC.md`

Purpose: define the target contract.

Keep:

- goal and non-goals,
- scope boundaries,
- constraints that affect implementation choices,
- acceptance criteria that can be verified.

Avoid:

- chronological progress logs,
- command output,
- old benchmark history,
- implementation details that belong in the plan.

### `IMPLEMENTATION_PLAN.md`

Purpose: describe how the work is or was sequenced.

Keep:

- stages and milestones,
- current status per stage,
- validation strategy,
- dependencies or risks that change execution order.

Avoid:

- detailed run-by-run results,
- stale completed-task prose,
- duplicate acceptance criteria from `SPEC.md`,
- machine-specific commands unless the repo itself requires them.

### `TASK_STATUS.md`

Purpose: give the next session a fast, accurate handoff.

Keep:

- current phase,
- current verified state,
- latest benchmark or validation facts,
- open blockers and next actions,
- important caveats.

Avoid:

- long chronological transcripts,
- repeated old results after a newer result supersedes them,
- stale Pending items that have already been completed,
- full command logs or raw grader output.

## Maintenance Rules

- Rewrite sections when the truth changes; do not only append new bullets.
- Keep historical detail only when it changes future decisions.
- Move long reusable procedures into `docs/`.
- When a task produces a reusable release or maintenance workflow, move that workflow into `docs/` and keep only the live contract in task docs.
- Keep task docs portable: no user-profile paths, machine-local interpreter paths, or temporary workspace internals unless they are the evidence being discussed.
- Prefer one concise "Current Truth" section over many dated fragments.
- At session boundary, update `TASK_STATUS.md` with what is true now and what should happen next.

## Suggested Shape

`SPEC.md`:

```md
# <Task> Specification

## Goal
## Scope
## Constraints
## Acceptance Criteria
```

`IMPLEMENTATION_PLAN.md`:

```md
# Implementation Plan

## Status Summary
## Stages
## Validation
## Risks
```

`TASK_STATUS.md`:

```md
# Task Status

## Current Phase
## Current Truth
## Latest Results
## Open Items
## Caveats
## Last Verification
```
