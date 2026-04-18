# Skills Development

This repository is a small workspace for building and validating reusable Codex skills.

## Contents

- `docs/` stores reusable workflow guidance for building, evaluating, and maintaining skills.
- `references/` stores source material used during skill authoring.
- `skills/` stores finished skill folders that are intended to be portable.
- `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` track substantial tasks in progress.

## Skills

- `skills/science-research-writing/` helps draft and revise English scientific manuscript prose.
- `skills/science-research-writing-zh/` helps draft and revise Chinese scientific manuscript prose.
- `skills/agents-md-improver/` helps decide whether and how to improve global, repository, or subdirectory `AGENTS.md` files. Human-facing release notes live at `skills/agents-md-improver/releases/v1.md`.

## Workflows

- `docs/skill-evaluation-workflow.md` records the reusable skill benchmark workflow, including baseline choice, executor lanes, artifact contracts, grading rules, and result interpretation.
- `docs/skill-release-workflow.md` records how human-facing skill release notes are placed, closed out, validated, and synchronized with repo docs.
- `docs/task-control-docs.md` records the expected structure for `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md`.

## Validation

If your Codex installation includes the system `skill-creator` skill, run its `quick_validate.py` validator against each skill folder with your local Python setup. This repository does not vendor the validator, so the exact command depends on your own environment.

```powershell
python path\to\quick_validate.py skills\science-research-writing
python path\to\quick_validate.py skills\science-research-writing-zh
python path\to\quick_validate.py skills\agents-md-improver
```
