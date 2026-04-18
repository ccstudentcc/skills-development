# Implementation Plan

## Status Summary

- Stage 1 through Stage 7 are implemented.
- The current focus is closeout hygiene: keep reusable workflow lessons in `docs/`, keep root `AGENTS.md` concise, and keep task-control docs maintainable.
- No commit has been made in this handoff.

## Stages

### Stage 1: Inspect And Frame

- Read repository instructions and task-control docs.
- Read `research/agents-md_best-practices.md` and supporting source notes.
- Define the deliverable as a reusable `agents-md-improver` skill plus minimal repo-doc sync.

Status: complete.

### Stage 2: Design Skill Shape

- Define the runtime boundary around `AGENTS.md` improvement.
- Split guidance into `SKILL.md` plus routed references for layer selection, update workflow, templates, and review.

Status: complete.

### Stage 3: Author Skill

- Create `skills/agents-md-improver/`.
- Add `SKILL.md`, routed references, `agents/openai.yaml`, eval fixtures, and the benchmark runner.

Status: complete.

### Stage 4: Sync Repository Docs

- Update `README.md` and `ARCHITECTURE.md` for skill and workflow discoverability.
- Keep root task-control docs aligned with the current work.

Status: complete.

### Stage 5: Validate Skill Structure

- Inspect skill files and references.
- Run `git diff --check`.
- Run the local `skill-creator` validator when available.

Status: complete for the current files.

### Stage 6: Automate Benchmarking

- Add a safe-first runner with `prepare`, `safe-run`, `grade-benchmark`, and `status` modes.
- Support eval-selection metadata, bounded parallel execution, deterministic grading, and best-effort review generation.
- Keep benchmark interpretation honest about explicit skill-context loading and executor limitations.

Status: implemented and validated on targeted and informative runs.

### Stage 7: Generalize Workflow Lessons

- Add `docs/skill-evaluation-workflow.md` for future skill benchmarks.
- Add `docs/task-control-docs.md` for maintainable `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md`.
- Add concise root and subdirectory `AGENTS.md` guardrails.

Status: implemented.

### Stage 8: Extend Skill For Memory-Derived Rules And Lossless Compression

- Update `skills/agents-md-improver/SKILL.md` so the skill explicitly supports deriving durable global rules from repeated memory evidence.
- Add routed guidance for lossless `AGENTS.md` compression, including safe vs unsafe compression moves.
- Extend the review checklist so compressed outputs and memory-derived rule proposals are audited explicitly.
- Sync `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` to the new skill scope.

Status: implemented.

### Stage 9: Publish Release Surface And Generalize Release Workflow

- Rewrite the human-facing `agents-md-improver` release note into release-announcement tone.
- Keep published release notes in `skills/<skill>/releases/` and remove duplicate drafts from `tmp/`.
- Add a reusable `docs/skill-release-workflow.md` so future skills follow the same closeout path.
- Sync `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, and task docs to the release workflow.

Status: implemented.

## Validation

- `git diff --check`.
- `quick_validate.py` for `skills/agents-md-improver` when available.
- Python syntax check for `skills/agents-md-improver/scripts/run_benchmark.py`.
- File inspection for root `AGENTS.md`, `skills/agents-md-improver/AGENTS.md`, `docs/skill-evaluation-workflow.md`, and `docs/task-control-docs.md`.
- File inspection for `docs/skill-release-workflow.md` and `skills/agents-md-improver/releases/v1.md`.
- File inspection for `skills/agents-md-improver/SKILL.md`, `skills/agents-md-improver/references/update-workflow.md`, and `skills/agents-md-improver/references/review-checklist.md`.

## Risks

- Existing prepared benchmark run directories contain copied skill context; use fresh iterations or refresh copied context before validating skill text changes.
- Re-grading old artifacts can fix recognition errors but does not prove new skill text was executed.
- Production-like baselines may become strong when repo evidence is obvious; improve eval design rather than hiding normal read-only evidence.
