# Skill Evaluation Workflow

Use this workflow when creating, improving, or comparing reusable skills. It captures the benchmark lessons from the `agents-md-improver` work and is intended to be portable to other skills in this repository.

## Goals

- Measure whether a skill changes real task outcomes, not only whether the executor can run.
- Compare `with_skill` and baseline runs under conditions that resemble normal repository use.
- Keep evidence inspectable: every claim should point to prompts, outputs, final responses, grading, and summaries.
- Preserve safety: automatic execution should stay isolated and opt-in.

## Evaluation Lanes

Keep these lanes separate in naming, metadata, and interpretation:

- `trigger-description`: checks whether the skill description causes the skill to be selected for appropriate prompts.
- `executor-health`: small smoke checks that prove the runner and sandbox can execute.
- `production-like-comparative`: realistic `with_skill` versus baseline runs where both sides can inspect the prepared repository copy.
- `diagnostic`: narrow reruns for one failure mode, grader fix, or prompt change.
- `low-discrimination`: cases that are useful for coverage but too easy for measuring skill lift.

Do not use an executor-health smoke as evidence that a skill improved outcomes.

Do not confuse description-trigger evaluation with fixture-edit benchmarks. A trigger optimizer can test whether a skill is selected, but it does not prove that the selected skill completes repository tasks correctly.

## Baseline Choice

Choose the baseline before running:

- For a new skill, compare against `without_skill`.
- For improving an existing skill, compare against either the old skill snapshot or `without_skill`, and record which choice was used.
- When the user asks for real usage, allow normal read-only repository inspection for both sides. Do not artificially blind the baseline unless the question is specifically about isolated reasoning without repo evidence.

## Eval Design

Prefer evals that exercise decisions the skill is supposed to improve:

- Include real files and realistic prompts instead of abstract questions.
- Add adversarial phrasing based on observed baseline failures.
- Include negative cases where the right answer is to refuse, route elsewhere, or keep a file unchanged.
- Keep easy smoke cases, but label them as low-discrimination or executor-health.
- Add 2-4 harder evals after each meaningful failure-mode review instead of only tuning the skill against one case.

Good eval assertions are objective and artifact-checkable. They should describe the behavior, not the exact wording, unless wording is the behavior under test.

## Executor Strategy

Use the safest executor that can answer the evaluation question:

- Start with `prepare` when available: copy fixtures, materialize prompts, and stop before nested execution.
- Run nested executors only as an explicit step.
- Prefer isolated workspace-write execution with no approvals for benchmark runs.
- Disable plugins, memories, and unrelated ambient context unless the evaluation is intentionally testing them.
- Allow read-only shell inspection inside the prepared workspace when the task requires repo awareness.
- For throughput, run independent eval directories in parallel with a conservative default such as `max_parallel=2`.

If a skill is copied into each run directory, a source skill edit is not visible to existing prepared runs. Use a fresh prepared iteration or refresh the copied skill context before claiming that a skill-text change was validated.

## Artifact Contract

Each iteration should make the run auditable without relying on chat memory:

- `iteration_metadata.json`: eval IDs, selection strategy, benchmark style, executor policy, parallelism.
- `prompt.md`: exact nested task prompt.
- `outputs/`: files produced or edited by the run.
- `final_response.md`: final user-facing answer from the run.
- `timing.json`: executor timing plus raw `total_tokens` from `codex exec --json` when available.
- `executor_status.json`: executor state, but not the only readiness signal.
- `codex_stdout.jsonl` and `codex_stderr.log`: transcripts and warnings when automatic execution is used.
- `grading.json`: per-expectation `text`, `passed`, and `evidence`.
- `benchmark.json`, `results.json`, and `run-summary.md`: aggregate results and interpretation notes.
- `review.html`: best-effort human review surface when a viewer is available.

Inspect `final_response.md` and `outputs/` before trusting `executor_status.json` or aggregate numbers. A run can be marked executed while its final response is still a progress note or while the claimed edit did not land.

Keep output-size metrics distinct from executor-usage metrics:

- `final_response.md` length is a response-size metric, not a token-usage metric.
- `timing.json.total_tokens` is the executor total-token metric when usage is available.
- Do not label `final_response.md` chars, `outputs/` chars, or transcript length as "tokens".
- If a run has missing usage and `timing.json.total_tokens` is `0`, say so explicitly before averaging or comparing token costs.

## Grading Rules

Keep grading deterministic where practical:

- Programmatically inspect files when assertions are objective.
- Store one `grading.json` per run with the exact viewer-compatible fields: `text`, `passed`, and `evidence`.
- If a matcher is too narrow, fix the matcher to accept semantically equivalent evidence without weakening the expectation.
- Do not change assertions simply to make a run pass.
- Re-grade historical artifacts only when the grader fix is about recognition, not when the underlying expected behavior changed.

When a grader fix changes an aggregate result, say whether the run artifacts are old or freshly rerun with the current skill text.

## Reading Results

Read benchmark results in this order:

1. Absolute `with_skill` pass rate.
2. Absolute baseline pass rate.
3. Per-eval wins, ties, and losses.
4. Delta as secondary context.
5. Time and usage costs, with token metric names stated explicitly.
6. Transcript and output inspection for surprising scores.

Baseline strengthening is not automatically bad. In production-like benchmarks, a strong baseline may mean the repo evidence is obvious. Use harder evals, not artificial blindness, when the goal is realistic skill value.

When reporting efficiency, name the metric precisely instead of saying only "tokens":

- use `executor total tokens` for `timing.json.total_tokens`,
- use `final response length` for `final_response.md` text length,
- use `output chars` only for aggregate edited-file size if that metric is relevant.

If a summary includes both response length and executor token cost, report them separately and explain why they are not interchangeable.

## Iteration Discipline

After a benchmark:

- Compare against the previous relevant iteration, not only the latest aggregate in isolation.
- Identify whether failures are skill weaknesses, runner prompt issues, stale copied skill context, incomplete runs, or grader mismatches.
- Make holistic skill updates when multiple fixes interact; avoid many tiny patches that create global drift.
- Rerun the smallest meaningful subset first, then re-grade or rerun the full informative set when needed.
- Record durable workflow lessons in task docs and, only when they prevent repeat agent mistakes, in `AGENTS.md`.

## Minimum Closeout

Before reporting success:

- Run structural validation for the edited skill when a validator is available.
- Run `git diff --check`.
- Compile or syntax-check any benchmark runner scripts that changed.
- Summarize the exact iteration paths and pass rates.
- If quoting efficiency numbers, state whether they came from `timing.json.total_tokens`, final-response length, or another metric.
- State which results came from fresh reruns and which came from re-grading existing artifacts.
- State remaining caveats, especially non-native skill loading, executor policy, or known low-discrimination evals.
