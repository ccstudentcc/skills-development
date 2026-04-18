# agents-md-improver Local Notes

These rules apply to `skills/agents-md-improver/`.

## Eval Fixtures

- Treat `evals/files/**/AGENTS.md` as fixture inputs, not live repository guidance; edit them only when changing the eval scenario itself.
- When an eval expectation changes, update `evals/evals.json`, the fixture files, and the deterministic grader together.

## Benchmark Runner

- Keep `run_benchmark.py` safe-first: `prepare` should not launch nested execution, and `safe-run` should remain explicit.
- Preserve the benchmark lane split: executor-health, production-like comparative, diagnostic, and low-discrimination.
- Keep `with_skill` and baseline runs in fresh isolated directories when validating skill text changes.
- Disable plugins, memories, and unrelated ambient context in nested benchmark runs unless the eval intentionally tests them.
- Default parallel nested execution to a conservative limit such as `max_parallel=2` unless the user asks otherwise.
- If the benchmark targets current skill wording, refresh copied skill context or use a fresh prepared iteration before trusting the run.

## Grading

- Inspect `final_response.md` and `outputs/` before accepting `executor_status.json` or aggregate summaries.
- Loosen matcher phrases only for semantically equivalent evidence; do not change the expectation to match a bad run.
- Record whether a score comes from fresh execution or re-grading existing artifacts.
