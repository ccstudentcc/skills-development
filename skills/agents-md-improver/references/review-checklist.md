# Review Checklist

Run this checklist before finishing an `AGENTS.md` improvement task.

## Placement

- Did you identify which `AGENTS.md` files are inherited and which file is the local edit target?
- Did you confirm that the change belongs in `AGENTS.md` rather than `README.md`, `ARCHITECTURE.md`, or task docs?
- Did you choose the narrowest layer that fully explains the behavior?
- If you created a subdirectory file, does it add genuinely local value?
- If onboarding or architecture prose was present, did you move it to `README.md` or `ARCHITECTURE.md` instead of polishing it in place?
- If you removed misplaced onboarding or architecture prose from `AGENTS.md`, did the destination file still contain the needed content after the move instead of relying on routing text alone?

## Rule Quality

- Is each added rule stable beyond the current task?
- Is each rule specific enough to check?
- Does each rule change execution outcomes instead of restating taste or common sense?
- Does the wording mention a concrete command, path, trigger, scope, or boundary when needed?
- If the edit came from memory review, did you confirm the pattern was repeated and global rather than repo-specific or stale?
- If the edit compressed wording, did the shorter text preserve the same operational meaning and scope?

## Redundancy and Conflict

- Did you remove or relocate duplicated rules instead of copying them across layers?
- Does the local file avoid contradicting higher-priority safety rules?
- If a local command conflicts with inherited safety, did you move it out of agent instructions instead of preserving it for convenience?
- Did you trim stale or noisy instructions that no longer earn their context cost?
- If a stale command was present, did you replace it using current repository evidence rather than keeping both old and new commands around?
- If you merged several lines into one, did you avoid deleting a distinct trigger, scope boundary, or validation caveat by accident?

## Signal-to-Noise

- Does the file stay focused on agent-execution facts rather than human onboarding or long explanation?
- If someone asked for one-file convenience, did you still keep onboarding in `README.md` and architecture in `ARCHITECTURE.md`?
- Did you avoid temporary ports, URLs, migration notes, and one-off workarounds?
- Is the entrypoint concise enough that the key constraints are easy to find quickly?
- If the file was bloated, did you shorten it by merging repetition rather than by dropping high-risk rules?

## Verification and Reporting

- Did you verify that the trigger was real and durable rather than a one-off annoyance?
- Did you run the smallest relevant verification step for any command or path-specific claim?
- If something was not verified, did you say exactly what was skipped?
- Did your final report explain what changed, why that layer was chosen, and what was intentionally left in other docs?
- If memory was used, did your report distinguish repeated memory evidence from current repo truth?
- If you rejected a new rule because the evidence was too weak, did the final report say explicitly that the current evidence is not durable or strong enough yet instead of only implying it?
- If you rejected a new rule because the evidence was too weak, did the final report also say where the observation was recorded instead?
- If you rejected a new rule because the evidence was too weak, did you note what repeat or concretization would justify promoting it later?
