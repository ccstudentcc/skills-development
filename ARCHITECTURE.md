# Architecture

## Repository Layout

- `docs/` contains repo-owned workflow guidance that applies across multiple skills.
- `references/` contains authoring inputs or source notes that may be richer than the final skill.
- `skills/<skill-name>/` contains a self-contained skill package with `SKILL.md`, `agents/`, and any bundled `references/`, `scripts/`, `releases/`, or `assets/`.
- Root task-tracking files record the current implementation contract for larger work.
- Parallel skills may target different task families, such as writing workflows or agent-instruction governance, while sharing the same repository-level structure.

## Design Principles

- Keep each skill portable inside its own folder.
- Prefer progressive disclosure: brief `SKILL.md`, detailed guidance in skill-local `references/`.
- Keep human-facing release history in skill-local `releases/`, not in runtime `references/` or repo `tmp/`.
- Avoid adding scripts or assets unless the skill needs deterministic tooling or output resources.
- Put cross-skill maintenance workflows in `docs/`; put skill-specific runtime instructions inside the relevant skill folder.
- Keep root task-control documents as small coordination surfaces; move reusable procedures and long histories into `docs/` or benchmark artifacts.
