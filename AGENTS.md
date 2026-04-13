# Skills Repo Notes

This repository mainly maintains reusable skills and their routed references.
Keep rules short, repo-specific, and focused on preventing repeat mistakes.

## Skill Authoring

- Keep `SKILL.md` concise. Put trigger logic, scope boundaries, routing, and maintenance rules in the entrypoint; move tactical depth into `references/`.
- Treat progressive disclosure as the default pattern. If the entrypoint starts carrying playbooks, push that detail down into routed reference files.
- When a long reference file becomes a primary execution surface, add `Quick Navigation` / `快速导航` near the top.
- When a skill exists in English and Chinese variants, keep structure aligned while preserving Chinese-native wording and conventions instead of literal translation.

## Related Skills

- For installed external skills, write `skill name + repository source`; do not write absolute filesystem paths, user-profile paths, interpreter paths, or machine-local validation commands.
- If a related skill is installed, the model should discover it by skill name. If it is unavailable in the current environment, the model must say that explicitly to the user.
- Normal task routing must be updated in both places: the entrypoint `SKILL.md` and the routed `references/` file that actually handles the scenario.
- Maintenance-only helpers must stay separate from runtime task routing. Keep tools like `Skill Reviewer` and `Skill Improver` in maintenance notes only, never in normal task-routing sections.
- When a related skill can be missing, document an explicit fallback map by skill instead of a vague “use fallback” sentence.

## References And Sources

- If upstream material is imported only as local source context, keep the vendored repository out of git by default and record the source in a lightweight reference note.
- Source notes should record the upstream repository link and the exact files actually used, not a generic “inspired by” claim.
- Adapt external material into repo-owned guidance. Do not mirror upstream wording or expose upstream runtime dependencies unless the user explicitly wants that.

## Repo Hygiene

- Do not expose machine-specific paths or environment-specific commands in skills, references, README files, or examples.
- For multi-turn skill work, keep `SPEC.md`, `IMPLEMENTATION_PLAN.md`, and `TASK_STATUS.md` synchronized with structural changes.
- After structural or routing edits, run at least `git diff --check` before claiming the update is clean.
- Update this file when a repeated mistake suggests a durable repo rule, especially for skill routing, reference organization, source handling, or environment leakage.
