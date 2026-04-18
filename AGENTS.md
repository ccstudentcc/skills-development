# Skills Repo Notes

This repository maintains reusable skills, routed references, and reusable workflow docs.
Keep rules short, repo-specific, and focused on preventing repeat mistakes.

## Skill Packages

- Keep `SKILL.md` concise; put trigger logic, scope boundaries, and routing in the entrypoint, then push tactical depth into `references/`.
- Treat progressive disclosure as the default pattern. If a reference becomes a primary execution surface, add `Quick Navigation` / `快速导航`.
- When routing changes, update both the entrypoint `SKILL.md` and the routed `references/` file that handles the scenario.
- When a skill exists in English and Chinese variants, keep structure aligned while preserving Chinese-native wording instead of literal translation.

## Runtime Boundaries

- Keep maintenance-only helpers out of runtime task routing. Tools like `Skill Reviewer` and `Skill Improver` belong in maintenance notes, not normal task sections.
- For installed external skills, write `skill name + repository source`; do not write absolute filesystem paths, interpreter paths, or machine-local validation commands.
- If a related skill may be unavailable, document an explicit fallback map by skill instead of a vague fallback sentence.
- Treat `skills/*/evals/files/**/AGENTS.md` as fixture inputs, not live repository guidance.

## Evaluation

- Use `docs/skill-evaluation-workflow.md` for reusable benchmark procedure; keep only short repeat-prevention guardrails here.
- Distinguish executor-health, production-like comparative, diagnostic, and low-discrimination runs before interpreting results.
- For real skill-lift checks, compare absolute `with_skill` and baseline pass rates first; treat delta as secondary context.
- After editing a skill, use a fresh prepared iteration or refresh copied skill context before claiming automatic benchmark evidence.
- Inspect `final_response.md` and `outputs/` before trusting `executor_status.json`, aggregate summaries, or re-grades; matcher fixes may widen equivalent evidence but must not weaken the expectation.

## Task Docs

- Use `docs/task-control-docs.md` for `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` structure and rewrite stale sections instead of appending timelines.
- Move reusable procedures into `docs/`; keep task docs free of machine-local paths unless they are necessary evidence.

## Sources And Hygiene

- Keep vendored upstream repositories out of git by default when they are only source context; record the upstream link and exact files used in a lightweight reference note.
- Adapt external material into repo-owned guidance. Do not mirror upstream wording or expose upstream runtime dependencies unless the user explicitly wants that.
- Do not expose machine-specific paths or environment-specific commands in skills, references, README files, or examples.
- When a new top-level content layer or durable doc set is added, sync `README.md`, `ARCHITECTURE.md`, and task docs in the same pass if navigation or ownership changed.
- For multi-turn skill work, keep `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` synchronized with structural changes.
- After structural or routing edits, run at least `git diff --check` before claiming the update is clean.
