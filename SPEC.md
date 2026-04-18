# AGENTS.md Improver Skill Specification

## Goal

Create and maintain `skills/agents-md-improver/`, a reusable skill that helps Codex improve `AGENTS.md` files at the correct layer:

- global / user-level instruction files,
- repository-root `AGENTS.md`,
- subdirectory-scoped `AGENTS.md`.

The skill should decide whether guidance belongs in `AGENTS.md` at all, choose the narrowest durable layer, and produce minimal, verifiable updates instead of bloated instruction files.

## Scope

- Distill `research/agents-md_best-practices.md` into portable runtime guidance.
- Keep the skill package progressive-disclosure based: concise `SKILL.md`, deeper routed `references/`, optional deterministic `scripts/`.
- Cover document-boundary decisions across `AGENTS.md`, `README.md`, `ARCHITECTURE.md`, and task-control docs.
- Support full-memory or rollout-summary review when the user wants to derive durable global `AGENTS.md` rules from repeated cross-repository patterns.
- Support lossless `AGENTS.md` compression: shorten bloated files by merging redundant wording without weakening execution constraints.
- Provide eval fixtures and a safe-first benchmark runner for `with_skill` versus baseline comparisons.
- Generalize reusable benchmark and task-control lessons into `docs/`.
- Generalize reusable skill-release closeout lessons into `docs/`.
- Keep repository docs synchronized only where they improve discoverability or execution.

## Constraints

- Do not turn `agents-md-improver` into generic documentation governance; keep runtime behavior focused on `AGENTS.md` decisions.
- Do not mirror research prose or upstream wording; adapt source material into repo-owned guidance.
- Keep skill content portable: no machine-local paths, user-profile paths, interpreter paths, or environment-specific commands in skill runtime docs.
- Allow the skill to reject a requested `AGENTS.md` change when evidence is weak, temporary, or belongs in another document.
- Treat memory as evidence for repeated patterns, not as current repository truth.
- Keep compression semantics-safe: do not compress away dangerous-command boundaries, scope limits, or validation caveats.
- Keep benchmark execution safe-first: preparation is default, nested execution is explicit, and unrestricted execution is not the baseline.
- Distinguish executor-health smokes, production-like comparative benchmarks, diagnostic reruns, and low-discrimination coverage.
- Treat absolute `with_skill` and baseline pass rates as primary; use delta as secondary context.
- Keep `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` concise coordination surfaces, following `docs/task-control-docs.md`.

## Acceptance Criteria

- `skills/agents-md-improver/SKILL.md` has valid frontmatter with only `name` and `description`.
- Referenced skill-local files exist and are used through clear routing.
- The skill clearly supports three decisions: whether to update `AGENTS.md`, which layer owns the rule, and how to word the smallest durable rule.
- The skill explicitly covers two additional maintenance workflows: mining repeated durable patterns from memory for global rules, and compressing `AGENTS.md` text without losing operational meaning.
- The skill-local references cover layer selection, update workflow, templates, and final review.
- `skills/agents-md-improver/agents/openai.yaml` exists and matches the skill.
- The benchmark runner can prepare, execute, grade, summarize, and inspect comparative runs without relying on hidden chat context.
- Benchmark artifacts state whether they are executor-health, production-like comparative, diagnostic, or low-discrimination.
- `docs/skill-evaluation-workflow.md` captures reusable benchmark workflow for future skills.
- `docs/skill-release-workflow.md` captures reusable skill release-note placement and closeout workflow.
- `docs/task-control-docs.md` captures reusable task-control document structure.
- Root and subdirectory `AGENTS.md` files contain only stable, short repeat-prevention rules.
- `README.md` and `ARCHITECTURE.md` mention the skill and reusable workflow docs where appropriate.
- `git diff --check` passes after edits.
- The available skill validator passes for `skills/agents-md-improver/`.
