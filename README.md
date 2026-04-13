# Skills Development

This repository is a small workspace for building and validating reusable Codex skills.

## Contents

- `references/` stores source material used during skill authoring.
- `skills/` stores finished skill folders that are intended to be portable.
- `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` track substantial tasks in progress.

## Skills

- `skills/science-research-writing/` helps draft and revise English scientific manuscript prose.
- `skills/science-research-writing-zh/` helps draft and revise Chinese scientific manuscript prose.

## Validation

If your Codex installation includes the system `skill-creator` skill, run its `quick_validate.py` validator against each skill folder with your local Python setup. This repository does not vendor the validator, so the exact command depends on your own environment.

```powershell
python path\to\quick_validate.py skills\science-research-writing
python path\to\quick_validate.py skills\science-research-writing-zh
```
