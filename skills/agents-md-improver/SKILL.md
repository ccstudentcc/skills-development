---
name: agents-md-improver
description: Improve, trim, or restructure AGENTS.md files at the correct layer. Use this skill whenever the user wants to add rules to a global instruction file, clean up a repository AGENTS.md, introduce or remove a subdirectory AGENTS.md, decide whether a repeated mistake belongs in AGENTS.md at all, or move guidance between AGENTS.md, README.md, ARCHITECTURE.md, and task-tracking docs.
---

# AGENTS.md Improver

## Overview

Use this skill to keep `AGENTS.md` files small, high-signal, and scoped to the right layer. The goal is not to write more instructions. The goal is to place the smallest durable rule in the lowest layer that actually needs it, and to avoid putting README, architecture notes, or temporary task state into agent instruction files.

## Use This Skill When

- Add, revise, trim, or reorganize a global / user-level instruction file.
- Improve a repository-root `AGENTS.md`.
- Introduce, review, or remove a subdirectory-scoped `AGENTS.md`.
- Decide whether a repeated mistake deserves a durable rule.
- Distill durable global rules from a full memory or rollout-history review without promoting repo-specific noise.
- Compress a bloated `AGENTS.md` without reducing execution quality, by merging redundant wording and preserving the real constraints.
- Decide whether a fact belongs in `AGENTS.md` versus `README.md`, `ARCHITECTURE.md`, or task-tracking docs.
- Turn messy instruction notes into concise, verifiable rules and routing guidance.

## Do Not Use This Skill For

- General project documentation that is mainly for human onboarding.
- Long architecture explanations or design rationale.
- One-off task plans, migration checklists, or temporary execution notes.
- Legal, policy, or compliance questions that require new external authority rather than repository-local guidance cleanup.

## Workflow

1. Inventory the active instruction chain before editing: read the nearest relevant `AGENTS.md` files from the local scope outward, then read adjacent docs that may own neighboring guidance.
2. Use [references/layer-selection.md](references/layer-selection.md) to decide whether the change belongs in `AGENTS.md` at all, and if so, which layer should own it.
3. Use [references/layer-selection.md](references/layer-selection.md) to separate inherited rules, local rules, and guidance that belongs in another document.
4. Use [references/update-workflow.md](references/update-workflow.md) to confirm the trigger with concrete evidence, choose minimal wording, decide whether to add, move, trim, or delete a rule, and compress wording when the current file is verbose or repetitive.
5. Use [references/templates.md](references/templates.md) only as a shape guide. Adapt to the existing repository instead of pasting templates blindly.
6. Run [references/review-checklist.md](references/review-checklist.md) before finalizing the edit.
7. Report what changed, why that layer was chosen, what was intentionally left elsewhere, and what verification was completed.

## Section Routing

- Use [references/layer-selection.md](references/layer-selection.md) for global vs repository vs subdirectory routing, document-boundary decisions, and rule-admission tests.
- Use [references/update-workflow.md](references/update-workflow.md) for update triggers, stale-rule cleanup, wording standards, and the minimum maintenance loop.
- Use [references/templates.md](references/templates.md) for reusable section shapes across global, repository, and local `AGENTS.md` files.
- Use [references/review-checklist.md](references/review-checklist.md) for the final audit on redundancy, specificity, stability, and verification.

## Output Requirements

- State which layer owns the change and why the neighboring layers were not chosen.
- When multiple `AGENTS.md` files are in scope, distinguish inherited guidance from the local delta.
- If a local file conflicts with an inherited safety boundary, preserve the inherited safety rule and remove or rewrite the conflicting local instruction.
- Treat the user's requested destination or durability as a proposal to evaluate, not as proof that `AGENTS.md` is the right target.
- Do not keep a local command in `AGENTS.md` just because it is relevant to that subtree if an inherited safety rule forbids the agent from running it.
- Preserve the target repository's existing language unless the user explicitly asks to normalize it.
- Prefer moving or deleting misplaced rules over copying them into multiple layers.
- When no `AGENTS.md` update is warranted, say so clearly and route the user to the correct document.
- When rejecting a requested `AGENTS.md` change, say explicitly in the target repository's language that the current evidence is not durable or strong enough yet, that there is still not enough evidence for a permanent `AGENTS.md` rule, and where the observation was kept instead.
- When routing a weak signal to task tracking or another non-durable surface, record it as an observation and say what repeat or concretization would justify promoting it later.
- Do not collapse onboarding or architecture back into `AGENTS.md` just because the requester wants future agents to read one file; keep execution rules and human/background docs split.
- When removing misplaced onboarding or architecture from `AGENTS.md`, make the move complete: keep or restore the needed content in `README.md` or `ARCHITECTURE.md` instead of leaving only a routing stub behind.
- When adding a rule, keep it specific, stable, and checkable.
- When deriving global rules from memory or rollout summaries, use the full relevant memory surface when needed, treat memory as evidence for repeated patterns rather than current repo truth, and reject repo-specific or stale details that do not generalize.
- When compressing an `AGENTS.md`, preserve execution semantics while merging redundant lines, deleting low-signal repetition, and keeping the fastest-scan constraints easy to find.
- When cleaning up a stale rule, cite the current repository evidence that replaced it, such as the live script surface, current docs, or the actual path layout.
- When a rule depends on a command, path, or dangerous boundary, include the concrete condition instead of a vague reminder.

## Common Transformations

- Convert a repeated failure into one concise, verifiable rule.
- Split a bloated root `AGENTS.md` into root guidance plus a local subdirectory file.
- Remove a local rule that tries to override a higher-priority safety boundary.
- Move human-onboarding prose from `AGENTS.md` into `README.md`.
- Move design explanation from `AGENTS.md` into `ARCHITECTURE.md`.
- If those destination docs are too thin after the move, restore the needed onboarding or architecture content there instead of only deleting from `AGENTS.md`.
- Delete stale or duplicate rules that no longer improve execution.
- Collapse clusters of near-duplicate rules into a shorter trigger-based rule when the shorter wording preserves the same operational boundary.
- Merge or delete repeated wording when an `AGENTS.md` has become verbose, but do not compress away scope boundaries, dangerous-command rules, or validation caveats.
- Decline to add a permanent rule when the only evidence is a single weak note or one-off complaint.
- Reword generic reminders into concrete commands, paths, scope limits, or validation steps.

## Example Requests

- `Use $agents-md-improver to trim this root AGENTS.md and move local exceptions into subdirectory files.`
- `Use $agents-md-improver to decide whether this repeated review comment belongs in AGENTS.md or README.md.`
- `Use $agents-md-improver to add a minimal repository rule for the test order in this monorepo.`
- `Use $agents-md-improver to review whether this global instruction file is carrying repo-specific noise.`
- `Use $agents-md-improver to draft a subdirectory AGENTS.md for packages/payments without duplicating the root file.`
- `Use $agents-md-improver to review the full memory and decide what durable rules belong in my global AGENTS.md.`
- `Use $agents-md-improver to compress this AGENTS.md without losing any real constraints.`

## Maintenance Notes

- Keep this entrypoint concise. New tactical depth belongs in `references/` unless the routing itself changes.
- Distill future research into actionable guidance; do not paste source registers, literature reviews, or long evidence narratives into the runtime skill.
- If a maintenance change alters routing, update both this entrypoint and the referenced file that handles the scenario.
