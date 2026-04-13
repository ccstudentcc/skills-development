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

Use the validator shipped with the system `skill-creator` skill:

```powershell
& 'C:\Users\chenpeng\miniconda3\python.exe' `
  'C:\Users\chenpeng\.codex\skills\.system\skill-creator\scripts\quick_validate.py' `
  'skills\science-research-writing'

& 'C:\Users\chenpeng\miniconda3\python.exe' `
  'C:\Users\chenpeng\.codex\skills\.system\skill-creator\scripts\quick_validate.py' `
  'skills\science-research-writing-zh'
```
