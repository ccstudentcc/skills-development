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
- Create `skills/science-research-writing-zh/` with matching structure.
- Package the Chinese scientific writing guidance into Chinese-facing skill content and references.

## Stage 4: Review and Tighten

- Run the available validator against the skill folder.
- Run the available validator against both skill folders.
- Review both skills against the four reviewer dimensions.
- Enrich routed `references/` files when reviewer-style read-through shows that section playbooks or control rules are too shallow to guide the model well.
- Fix any critical or major issues, then re-check.

## Stage 5: Publish

- Initialize git locally.
- Create or connect a public remote repository.
- Commit the finished workspace and push the default branch.

## Verification

- File inspection for the English source notes and both skill folders.
- Validator output from `quick_validate.py` for both skills.
- Reviewer-style read-through of the routed reference files to confirm they remain concise at the entrypoint and concrete in `references/`.
- Git evidence for repository initialization, commit, remote, and push.
