# Update Workflow

Use this file when you already know the change belongs in `AGENTS.md` and need a disciplined way to add, move, trim, or delete rules.

## Quick Navigation

- Start with `High-Value Triggers` to decide whether the issue deserves a durable rule.
- Use `Memory-Derived Global Updates` when the user wants to mine rollout memory for global rules.
- Use `Lossless Compression` when the file is too verbose but the rules still matter.
- Use `Minimal Maintenance Loop` for the shortest safe path.
- Use `Repository Update SOP` when performing a real edit.
- Use `Rule Wording Standard` before finalizing text.

## High-Value Triggers

These are strong reasons to update an `AGENTS.md` file:

- the same mistake happened a second time,
- review feedback repeated a known point,
- the agent had to search too many files to find one stable fact,
- build or test commands have a non-obvious order,
- one command works only from a certain directory or with a hidden prerequisite,
- a new sensitive area or secret boundary appeared,
- a subtree gained enough local behavior to justify its own file,
- an existing rule became stale, wrong, or redundant.

These are weak reasons:

- a one-off annoyance during a single task,
- a preference that does not change outcomes,
- a detail that is unstable or likely to expire soon,
- a rule that belongs more naturally in another document.

## Evidence Before Editing

Do not turn a hunch into a durable rule without checking the trigger.

Collect the smallest concrete evidence that the change is justified:

- the repeated review comment or repeated user correction,
- the command or path that proved non-obvious,
- the duplicate, stale, or conflicting rule text already present,
- the document that should own the guidance if `AGENTS.md` is not the right place.
- the current repository surface that supersedes an old rule, such as `package.json`, maintained docs, or the real directory layout.

The user's requested destination is not evidence on its own. A request to "add it to `AGENTS.md`" or "make it permanent" still needs independent proof that the issue is durable enough for an agent rule.

The same applies to convenience requests. A request to "keep this in one file so future agents only read one file" does not by itself justify moving onboarding or architecture ownership into `AGENTS.md`.

If you cannot point to a concrete trigger, default to observation or another document update instead of adding a new `AGENTS.md` rule.

One weak note is observation, not durable guidance. A single vague complaint can justify tracking the issue in task notes, but it should not become a permanent `AGENTS.md` rule by default.

When you reject a permanent rule from weak evidence, make the reporting pattern explicit:

- say that the current evidence is not durable or strong enough yet for a permanent `AGENTS.md` rule, and that there is still not enough evidence for that promotion,
- say where the observation now lives,
- say what repeat pattern or concrete path/command boundary would justify promotion later.

## Memory-Derived Global Updates

Use this section when the user wants to strengthen a global or user-level `AGENTS.md` from memory, rollout summaries, or other accumulated cross-repository evidence.

### What qualifies

Good candidates:

- the same failure mode appears across multiple repositories or sessions,
- the same user correction repeats in unrelated contexts,
- the issue is stable at the global layer, such as safety, evidence handling, validation honesty, skill use, or tool preference,
- the wording can stay portable without local paths, repo commands, or temporary environment workarounds.

Bad candidates:

- one repository's command surface,
- a machine-specific path or interpreter location,
- one benchmark runner's artifact contract,
- version-specific tool behavior that is likely to drift soon,
- any detail that belongs in a repo `AGENTS.md`, runbook, or troubleshooting doc.

### How to use memory well

1. Read enough of the relevant memory surface to distinguish repeated patterns from isolated incidents. If the user explicitly asks for a full memory review, do not rely on sparse keyword hits alone.
2. Treat memory as evidence for repetition and durability, not as current repository truth.
3. Extract candidate rules in plain language first.
4. Reject any candidate that is still repo-specific, time-specific, or better owned by a lower layer.
5. Add only the smallest global rule that captures the repeated pattern.

### Reporting expectations

- Say that the rule was derived from repeated memory evidence, not from one local file.
- Say why the rule belongs in the global layer rather than a repo or subdirectory file.
- If you reject a candidate, say that the evidence did not generalize cleanly enough yet.

## Lossless Compression

Use this section when the file is directionally correct but too long, repetitive, or slow to scan.

### Goal

Shorter is not the real goal. The goal is to reduce context cost without weakening execution constraints.

### Safe compression moves

- merge adjacent lines that express the same trigger or boundary,
- replace several parallel examples with one trigger-based rule,
- remove placeholder definitions when later lines already define the same document more precisely,
- collapse repeated wording into one sentence when the scope and severity stay clear.

### Unsafe compression moves

- deleting a dangerous-command boundary because it feels obvious,
- merging two rules that apply to different scopes,
- dropping validation caveats that distinguish full verification from limited checks,
- shortening wording until the actor, scope, or condition becomes ambiguous,
- deleting a routing rule just because another document mentions a neighboring concept.

### Compression procedure

1. Mark which lines are true duplicates, which are complements, and which only look similar.
2. Compress only the duplicates or near-duplicates first.
3. Re-read the shortened text and check whether any command boundary, scope limit, or reporting requirement disappeared.
4. Prefer a trigger-based combined rule only when it preserves the same operational meaning.
5. Keep the fastest-scan constraints early and easy to spot.

## Minimal Maintenance Loop

Use this loop unless the task needs something more elaborate:

1. Identify the trigger event.
2. Confirm the trigger with concrete evidence from the repository, task history, or repeated feedback.
3. Decide whether it is durable enough to become a rule.
4. Choose the smallest correct layer.
5. Write the minimum concrete delta.
6. If the file is bloated, compress redundant wording without weakening the real rule set.
7. Check for duplicates or conflicts.
8. Verify the command, path, document boundary, or inherited safety constraint when practical.
9. Keep the rule only if it actually reduces future search or failure.

## Repository Update SOP

1. Record the trigger in plain language.
2. Confirm the trigger with repository evidence, repeated feedback, or an existing conflicting rule.
3. Decide whether the problem is repeated, structural, or just noise.
4. Confirm the correct destination: global, repository root, local `AGENTS.md`, `README.md`, `ARCHITECTURE.md`, or task docs. Treat the requested destination as a hypothesis, not a binding instruction.
5. If `AGENTS.md` is correct, edit only the smallest necessary section.
6. Prefer adding one durable rule over adding a new paragraph of commentary.
7. If the file is bloated, compress or merge redundant wording before adding more lines.
8. If a rule applies only to one subtree, move it downward instead of polluting the root file.
9. Remove or relocate stale and duplicate rules instead of preserving historical clutter.
10. If the issue is a local conflict with inherited safety, preserve the inherited rule and rewrite the local file. Do not keep the forbidden command in local `AGENTS.md` just because it is operationally relevant there.
11. Run the smallest relevant verification step.
12. In the final report, say what changed, why it belongs there, and what was verified.
13. If you rejected an `AGENTS.md` change, say both why the evidence is still too weak and which non-durable surface now holds the observation.
14. If you kept only an observation, record the likely promotion trigger, such as repetition of the same confusion or a later concrete path/command boundary.

## Rule Wording Standard

Good rules are concrete and testable.

### Good

- `After editing schema files under schema/, run pnpm db:generate.`
- `Do not edit generated files under gen/ directly; regenerate them from the source definitions.`
- `Changes under packages/payments/ should start with pnpm test --filter payments before wider validation.`

### Weak

- `Pay attention to database-related files.`
- `Follow project conventions.`
- `Test things before finishing.`

## Add vs Move vs Delete

### Add

Add a rule when the fact is durable, non-obvious, and missing.

### Move

Move a rule when it is still important but lives at the wrong layer.

Examples:

- root-level local test details that belong in a subtree file,
- architecture explanation that belongs in `ARCHITECTURE.md`,
- onboarding prose that belongs in `README.md`.

When moving misplaced content out of `AGENTS.md`, finish the move completely:

- remove the misplaced onboarding or architecture text from `AGENTS.md`,
- add or restore that content in `README.md` or `ARCHITECTURE.md` if the destination file does not already carry the needed information,
- do not stop at a routing note if the destination would otherwise stay incomplete.

### Delete

Delete a rule when it is:

- stale,
- contradicted by current practice,
- duplicated elsewhere,
- too vague to guide action,
- no longer worth the context budget.

### Route Elsewhere

Do not treat every cleanup as an `AGENTS.md` edit.

- Move onboarding, project story, and getting-started prose to `README.md`.
- Move design explanation, module history, and architecture rationale to `ARCHITECTURE.md`.
- Move one-off observations and current-task tracking to task docs.
- If a lower `AGENTS.md` used to contain a forbidden production/deploy command, move that operational note to a human-facing doc if it still matters, but keep the command out of agent instructions.

## Verification Expectations

- If the rule names a command, verify that command or the smallest relevant equivalent when practical.
- If the edit removes or replaces a stale command, verify the replacement against current repo evidence rather than preserving both.
- If the rule names a path or scope boundary, inspect the real path layout.
- If a local file used to conflict with inherited safety, verify that the conflict is gone and that the inherited boundary still stands.
- If the rule claims a generated artifact dependency, verify the source-to-derived relationship.
- If verification is too expensive or not possible in the current turn, say exactly what was not verified.

## Rejection Reporting Pattern

Use a direct shape when weak evidence does not justify a permanent rule:

- `I did not update AGENTS.md because the current evidence is still only a one-off note and is not durable enough yet for a permanent rule.`
- `I did not update AGENTS.md because the current evidence is still only one recent review note and is not strong enough yet. There is still not enough evidence for a permanent AGENTS.md rule.`
- `I recorded the observation in TASK_STATUS.md for now. If the same confusion repeats, or if it becomes a concrete path/command boundary, then promote it.`
- `我没有更新 AGENTS.md，因为当前只有一条单次反馈，证据还不够强，也还没有足够证据升格成永久 AGENTS.md 规则。`
- `我先把观察记录在 TASK_STATUS.md；如果同类问题再次出现，或者进一步明确成具体路径 / 命令 / 范围边界，再考虑提升。`
