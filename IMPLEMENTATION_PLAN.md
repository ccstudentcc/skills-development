# Implementation Plan

## Stage 1: Inspect and Frame

- Review repository constraints, skill creation guidance, and reviewer criteria.
- Capture scope, acceptance criteria, and validation plan in the task tracking files.

## Stage 2: Prepare Source Material

- Rewrite `references/Science Research Writing.md` into English.
- Preserve the original structure where it still helps downstream skill design.

## Stage 3: Initialize and Author the Skill

- Create `skills/science-research-writing/` with `skill-creator` scaffolding.
- Replace scaffold content with a concise workflow-oriented `SKILL.md`.
- Add only the reference files that the skill actually needs.
- Add `agents/openai.yaml` metadata.

## Stage 4: Review and Tighten

- Run the available validator against the skill folder.
- Review the generated skill against the four reviewer dimensions.
- Fix any critical or major issues, then re-check.

## Stage 5: Publish

- Initialize git locally.
- Create or connect a public remote repository.
- Commit the finished workspace and push the default branch.

## Verification

- File inspection for English-only source and skill contents.
- Validator output from `quick_validate.py`.
- Git evidence for repository initialization, commit, remote, and push.
