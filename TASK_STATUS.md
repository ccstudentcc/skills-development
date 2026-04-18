# Task Status

## Current Phase

Closeout and documentation governance for `agents-md-improver`.

## Current Truth

- `skills/agents-md-improver/` exists with a concise entrypoint, routed references, eval fixtures, `agents/openai.yaml`, and a safe-first benchmark runner.
- `agents-md-improver` is being extended to cover two additional maintenance workflows: deriving durable global rules from repeated memory evidence, and losslessly compressing verbose `AGENTS.md` files.
- `docs/skill-evaluation-workflow.md` generalizes the skill benchmark workflow for future skills.
- `docs/task-control-docs.md` defines the expected structure for `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md`.
- Root `AGENTS.md` now has concise guardrails for skill evaluation and task-control docs.
- `skills/agents-md-improver/AGENTS.md` scopes fixture, runner, copied-skill-context, and grader rules to the `agents-md-improver` subtree.

## Latest Benchmark Facts

- Fresh targeted run `tmp/agents-md-improver-workspace/iteration-eval11-retest-2`: `with_skill 3/3`, `without_skill 0/3`.
- Re-graded existing `tmp/agents-md-improver-workspace/iteration-auto-informative-6`: `with_skill 21/21`, `without_skill 9/21`, secondary delta `+0.57`.
- The targeted run validates current skill text for `eval-11`; the full informative result is a re-grade of existing artifacts, not a fresh full rerun.

## Open Items

- If the next goal is a final full benchmark claim, run a fresh informative production-like iteration rather than relying only on re-graded historical artifacts.
- If adding more skills, reuse `docs/skill-evaluation-workflow.md` and adapt only skill-specific runner details.
- If task-control docs start growing again, rewrite them to the structure in `docs/task-control-docs.md` instead of appending more history.

## Caveats

- Nested benchmark `with_skill` still uses explicit copied skill context rather than native nested skill discovery.
- Prepared run directories can contain stale skill copies; fresh iterations are required for validating skill text edits.
- `executor_status.json` is not sufficient evidence by itself; inspect `final_response.md` and `outputs/` before trusting aggregate summaries.
- Grader matcher fixes may accept semantically equivalent evidence but must not weaken expectations.
- The new memory-derived-rule and lossless-compression capabilities are not benchmarked yet in a fresh dedicated run.

## Last Verification

- Re-read `skills/agents-md-improver/SKILL.md`, `references/update-workflow.md`, and `references/review-checklist.md` after the memory-derived-rule and lossless-compression extension.
- Re-optimized the live repo `AGENTS.md` layers: root `AGENTS.md` is now 40 lines and `skills/agents-md-improver/AGENTS.md` is 23 lines.
- `git diff --check` passed after the skill extension and AGENTS-layer optimization.
- `quick_validate.py` passed for `skills/agents-md-improver`.
- `py_compile` passed for `skills/agents-md-improver/scripts/run_benchmark.py`.
- `TASK_STATUS.md`, `SPEC.md`, and `IMPLEMENTATION_PLAN.md` remain compact handoff/contract documents instead of append-only logs.
