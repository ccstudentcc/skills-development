# Architecture

## Repository Layout

- `references/` contains authoring inputs or source notes that may be richer than the final skill.
- `skills/<skill-name>/` contains a self-contained skill package with `SKILL.md`, `agents/`, and any bundled `references/`, `scripts/`, or `assets/`.
- Root task-tracking files record the current implementation contract for larger work.

## Design Principles

- Keep each skill portable inside its own folder.
- Prefer progressive disclosure: brief `SKILL.md`, detailed guidance in skill-local `references/`.
- Avoid adding scripts or assets unless the skill needs deterministic tooling or output resources.
