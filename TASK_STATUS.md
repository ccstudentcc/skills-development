# Task Status

## Current Phase

Stage 4: Review and Tighten

## Completed

- Read the repository instructions from `AGENTS.md`.
- Read the requested skill guidance: `skill-improver`, `skill-reviewer`, and `llm-prompt-optimizer`.
- Started a new refinement session with the existing task-tracking files already in place.
- Reviewed the current English and Chinese science research writing skills plus their routed reference files.
- Confirmed that the entrypoint `SKILL.md` files are concise, but the routed `references/` files were too compressed to carry enough practical guidance for model execution.
- Rewrote the English routed reference files with task triage, section-specific playbooks, sentence-level control tactics, and a stronger final review gate.
- Rewrote the Chinese routed reference files with parallel structure plus Chinese-specific handling for subject ownership, chart guidance, certainty calibration, and de-colloquialization.
- Updated both `SKILL.md` files so their routing guidance points to the richer reference content.
- Synced `SPEC.md` and `IMPLEMENTATION_PLAN.md` with the new requirement that routed references remain materially more concrete than the entrypoint.
- Cloned `https://github.com/quanghuy0497/Writing-in-the-Sciences` into `references/Writing-in-the-Sciences/`.
- Read the repository root `README.md` plus the eight unit `README.md` files only; no PDFs were used as source material.
- Identified the most reusable additions for these skills: clutter cutting, stronger verb choices, punctuation and paragraph flow, manuscript assembly order, table/figure storytelling, response-to-reviewers discipline, review article structure, and lay-summary guidance.
- Added new routed workflow-extension references for both skills to cover manuscript assembly order, display-driven storytelling, review-article structure, lay summaries, and reviewer-response discipline.
- Expanded both `SKILL.md` entrypoints so they route into the new workflow-extension references while staying concise.
- Folded the most reusable Unit 1-3 guidance into the existing style and checklist references, especially clutter cutting, stronger verb choices, punctuation-for-emphasis, citation placement, and cross-surface consistency checks.
- Localized the new Chinese guidance to Chinese academic and public-facing writing conventions instead of mirroring English wording.
- Added `.gitignore` coverage for `references/Writing-in-the-Sciences/` so the vendored upstream repository stays local-only.
- Added `references/Writing-in-the-Sciences-reference.md` to record the upstream repository URL and the exact `README.md` files used as source material.
- Added related-skill routing to both skill entrypoints so adjacent tasks now route to `doc-coauthoring`, `canvas-design`, `citation-management`, and the appropriate humanizer skill.
- Added matching related-skill routing to both workflow-extension references, including an explicit instruction to tell the user when a routed skill is unavailable in the current environment.
- Added quick-navigation sections to the large routed reference files so long reference material is faster to traverse during execution.
- Clarified graceful degradation: when a related skill is unavailable, the model should tell the user and continue with the closest in-skill fallback.
- Added explicit per-skill fallback maps for missing related skills so degraded execution stays bounded and does not overclaim unavailable capabilities.
- Added lightweight maintenance rules in both entrypoints to preserve progressive disclosure and keep related-skill names aligned with the real environment.
- Added maintenance-only related-skill guidance for future skill improvement, citing repository sources instead of absolute paths and stating that missing skills must be disclosed explicitly to the user.
- Updated the four main related-skill routes to cite repository sources instead of plain names alone, while keeping discovery by skill name and explicit missing-skill disclosure rules.
- Verified that `git diff --check` is clean after the edits.
- Verified that all relative markdown links under both skill folders resolve successfully.

## In Progress

- Verifying the new related-skill routing pass and preparing the next commit.

## Pending

- Re-run markdown and diff checks after the latest related-skill edits.
- Re-run markdown and diff checks after the quick-navigation and fallback wording pass.
- Re-run markdown and diff checks after the explicit fallback-map and maintenance-rule pass.
- Re-run markdown and diff checks after the maintenance-only reviewer/improver note.
- Wait for a commit request before staging or committing.

## Notes

- The current refinement remains documentation-only.
- The intended design remains progressive disclosure: concise entrypoint, concrete action-oriented reference files.
- The imported course repository is treated as a local reference corpus, not as a runtime dependency for the finished skills.
