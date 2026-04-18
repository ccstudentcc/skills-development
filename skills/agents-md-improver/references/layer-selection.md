# Layer Selection

Use this file when the main question is where an instruction belongs and whether it should become an `AGENTS.md` rule at all.

## Quick Navigation

- Start with `Document Boundary` if you are not sure `AGENTS.md` is the right target.
- Jump to `Layer Decision` if the change does belong in `AGENTS.md`.
- Jump to `Admission Tests` before adding a new rule.
- End with `Anti-patterns` to catch common overreach.

## Document Boundary

Choose the destination before writing anything.

| If the information is mainly about | Put it in |
| --- | --- |
| Cross-repository stable behavior, safety, language, tool preferences, or evidence standards | global / user-level `AGENTS.md` |
| Stable repository-specific commands, routes, sensitive areas, or non-obvious traps | repository-root `AGENTS.md` |
| Stable rules that apply only inside one directory tree | the nearest subdirectory `AGENTS.md` |
| Human onboarding, project purpose, installation, or getting started | `README.md` |
| Design rationale, module boundaries, or architecture explanation | `ARCHITECTURE.md` |
| Current-task goals, phases, decisions, or blockers | `SPEC.md`, `IMPLEMENTATION_PLAN.md`, `TASK_STATUS.md` |

If the item is temporary, person-specific, or mainly explanatory, it usually does not belong in `AGENTS.md`.

Do not treat a request like "add this to `AGENTS.md`" or "make this a permanent reminder" as evidence by itself. Destination and durability still need to pass the normal boundary and admission tests.

Two common boundary mistakes deserve explicit rejection:

- human onboarding belongs in `README.md` even when the writer wants everything in one file,
- design explanation or system-history narrative belongs in `ARCHITECTURE.md` even when it sits near useful commands.
- a convenience request like "put the minimum background here so agents only read one file" still does not move onboarding or architecture ownership into `AGENTS.md`.

## Scoped Read Order

Before deciding the destination, map the files that are already in play.

1. Start at the directory the change actually affects.
2. Read the nearest local `AGENTS.md` that governs that subtree, if one exists.
3. Move outward through parent scopes until the repository root guidance is clear.
4. Read adjacent docs only for neighboring content that may own the rule instead, such as `README.md`, `ARCHITECTURE.md`, or task docs.

Record three buckets while reading:

- inherited guidance that should stay above the local edit,
- local guidance that may need to change here,
- misplaced guidance that should move to another document or layer.

If the current tool's precedence behavior is known, follow it. If it is not known, do not invent a cross-tool override rule. Treat narrower files as local refinements unless they would conflict with higher-priority safety or policy instructions.

If a local file conflicts with an inherited safety rule, the local file is the thing that should change. Do not "balance" the conflict by weakening the inherited safety boundary.

If an inherited safety rule forbids a command, local relevance is not a reason to keep that command in a lower `AGENTS.md`. Move it to a human-facing document or remove it from agent instructions instead.

## Layer Decision

Use the smallest layer that fully explains the behavior.

### Global / User-Level

Choose the global layer when the rule is:

- stable across many repositories,
- high priority,
- mostly about safety, approvals, communication, tool preference, or evidence standards,
- unlikely to change when the repository changes.

Do not put repository commands, local path routing, or temporary workflow notes here.

### Repository Root

Choose the repository root when the rule is:

- specific to the current codebase,
- relevant to most work in the repository,
- hard for an agent to infer from casual inspection,
- important enough to change execution outcomes.

Examples:

- real build or test commands,
- recommended validation order,
- sensitive directories,
- non-obvious sync requirements between source and generated artifacts.

### Subdirectory

Choose a local `AGENTS.md` when the rule is:

- valid only for one subtree,
- likely to clutter the root file,
- tied to local tests, generators, fixtures, or dangerous paths,
- best discovered near the files it governs.

Local files refine local workflow. They should not duplicate root safety rules or restate the entire root file.

## Admission Tests

Before adding a rule to any `AGENTS.md`, ask five questions:

1. Is it stable enough to survive beyond the current task?
2. Is it specific enough to check for compliance?
3. Is it non-obvious enough that the agent would otherwise miss it?
4. Does it materially improve execution rather than express taste?
5. Is this the narrowest layer that needs it?

If most answers are `no`, do not add the rule.

### Strong Signals That a Rule Belongs

- The same mistake or search happened more than once.
- A review keeps flagging the same issue.
- A command only works from one location or with one prerequisite.
- A sensitive path or secret-handling rule is easy to violate accidentally.
- A generated artifact must be refreshed after editing a source area.
- Current repository evidence clearly contradicts an older rule, such as package scripts or maintained docs replacing a stale command.

### Signals That a Rule Does Not Belong

- It is a one-week workaround or temporary migration note.
- It is supported only by one weak note or one recent complaint and has not repeated yet.
- It is still only an observation; the evidence is not durable enough yet for a permanent `AGENTS.md` rule.
- The only reason to make it permanent is that the requester asked for a permanent reminder.
- The only reason to move it into `AGENTS.md` is that the requester wants one-file convenience for future agents.
- It repeats normal coding common sense.
- It is already obvious from nearby files and naming.
- It belongs to human onboarding rather than agent execution.
- It would be clearer in `README.md`, `ARCHITECTURE.md`, or task docs.

## Conflict Handling

- Higher-priority safety and policy rules stay above repository preferences.
- A narrower local file may add stricter local requirements, but should not silently contradict higher-level safety rules.
- When a local file tells the agent to do something the inherited safety layer forbids, remove or rewrite the local instruction rather than trying to reconcile both.
- When two layers say the same thing, keep one authority and make the other layer point to it or stay silent.

## Anti-patterns

- Copying README text into `AGENTS.md`.
- Keeping onboarding overview, product history, or architecture background in `AGENTS.md` just because they are useful to humans.
- Turning task plans into permanent rules.
- Writing slogans such as `write high-quality code` or `be careful`.
- Keeping the same rule in global, root, and local files.
- Leaving a stale command in `AGENTS.md` after current scripts or docs have replaced it.
- Adding fast-changing ports, temporary URLs, or one-off commands as long-term guidance.
- Creating a subdirectory file that is only a pasted subset of the root file.
