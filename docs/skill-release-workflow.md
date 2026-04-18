# Skill Release Workflow

Use this workflow when a skill in this repository is ready for a human-facing release note or a versioned release checkpoint.

## Goals

- Keep release artifacts discoverable without polluting runtime skill routing.
- Separate runtime instructions, reusable workflows, and human-facing release communication.
- Make each release auditable through validation, benchmark evidence, and synchronized repo docs.

## Placement Rules

Use the narrowest durable home for each release-related artifact:

- `skills/<skill-name>/SKILL.md`: runtime trigger, scope boundary, and section routing.
- `skills/<skill-name>/references/`: runtime tactical guidance the skill may rely on while executing.
- `skills/<skill-name>/releases/`: versioned human-facing release notes such as `v1.md`, `v1.1.md`, or `2026-04.md`.
- `docs/`: cross-skill workflows, reusable release checklists, or repo-wide maintenance guidance.
- `tmp/`: scratch notes, drafts, prepared workspaces, and temporary comparisons only.

Do not keep a published release note in `tmp/`.

Do not place human-facing release notes in `references/`, because that folder is for runtime guidance rather than publication history.

## Release Content

A release note should read like a release announcement, not like a chat transcript or task diary.

Prefer this structure:

1. What was released.
2. What problems it is intended to solve.
3. What capabilities or workflows are included.
4. What evidence supports the release.
5. What limits or caveats still remain.

Keep benchmark detail honest, but summarize the result instead of reproducing the whole task history.

## Release Closeout

Before treating a release note as published:

1. Confirm the final release file is under `skills/<skill-name>/releases/`.
2. Remove or migrate any duplicate draft that still lives in `tmp/`.
3. Update `README.md` if the release note should be discoverable from the repository entry surface.
4. Update `ARCHITECTURE.md` if the release changes the expected package layout or document ownership.
5. Update `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` when the release changes the current contract, workflow surface, or verified state.
6. Update `AGENTS.md` only if the release uncovered a durable repeat-prevention rule for this repository.

## Validation

Release closeout should run the smallest checks that support the claim:

- `git diff --check`
- any skill validator relevant to the edited skill
- syntax or compile checks for changed runner scripts
- direct inspection of the final release note path and linked doc entry points

If benchmark numbers are cited, say whether they come from fresh runs or re-grading existing artifacts.

If token or size metrics are cited, keep metric names precise and do not blur `timing.json.total_tokens` with response length.

## Naming

Use names that stay legible when more releases accumulate:

- `v1.md`, `v1.1.md`, `v2.md` for semantic release checkpoints
- `2026-04.md` for date-based release logs

Choose one convention per skill and keep it consistent.

## Anti-Patterns

Avoid these release mistakes:

- storing the final release note only in `tmp/`
- mixing runtime instructions and release prose in `references/`
- linking to a release note from `README.md` without actually moving the file into the skill package
- quoting aggregate benchmark numbers without saying what metric they represent
- treating re-graded historical artifacts as proof that new skill text was freshly executed
