---
name: science-research-writing
description: Draft, revise, and diagnose English scientific writing for manuscript sections, review-style synthesis, lay summaries, and reviewer-facing revisions. Use when Codex needs to turn notes or rough text into journal-style research prose, align a section with its expected rhetorical moves, improve sentence-level choices such as tense, voice, hedging, cohesion, causality, and terminology consistency, or package research writing for adjacent scholarly formats.
---

# Science Research Writing

## Overview

Use this skill to produce research prose that is easy to follow, structurally appropriate for the target section, and faithful to the available evidence. Make the reader's path explicit instead of relying on the reader to infer function, relevance, or certainty.

## Use This Skill When

- Draft a manuscript section from notes, figures, or bullet points.
- Revise rough scientific prose into clearer journal-style English.
- Diagnose why a paragraph feels weak, confusing, overclaimed, or structurally mismatched.
- Tighten an abstract, title, or conclusion so the contribution is easier to understand.
- Organize a review article, point-by-point response, or lay summary that stays close to the underlying science.

## Do Not Use This Skill For

- Citation lookup, BibTeX repair, or literature search.
- Journal template formatting, reference-style conversion, or submission portal tasks.
- Domain-specific scientific judgments that require missing background knowledge or new evidence.
- Pure journalism or marketing copy that is no longer anchored to the source science.

## Related Skills

- When the task expands into staged document collaboration across outlining, section-by-section ideation, drafting, refinement, and reader checks, use `doc-coauthoring` from the `anthropics/skills` repository.
- When the user needs a concept figure, framework diagram, schematic, or other polished single-page visual artifact, use `canvas-design` from the `anthropics/skills` repository.
- When the task requires citation lookup, metadata verification, DOI-to-BibTeX conversion, or bibliography cleanup, use `citation-management` from the `K-Dense-AI/claude-scientific-writer` repository.
- When the scientific structure is already sound but the prose still feels synthetic or machine-regular, use `humanizer` from the `blader/humanizer` repository for the final tone pass.
- Do not add absolute paths here: if these skills are installed, the model can discover them by skill name; if one is unavailable, say that explicitly to the user and continue with the best in-skill fallback.

## Workflow

1. Identify the job: draft, revise, or diagnose.
2. Identify the target section and read the matching playbook in [references/manuscript-map.md](references/manuscript-map.md).
3. Read [references/style-controls.md](references/style-controls.md) when the task involves tense, voice, hedging, cohesion, causality, articles, terminology, or sentence-level diagnosis.
4. Read [references/workflow-extensions.md](references/workflow-extensions.md) when the task involves manuscript assembly order, tables and figures, review articles, response letters, or lay summaries.
5. Build the paragraph plan in sentence functions before writing. Decide what each sentence must do for the reader, not just what information it contains.
6. Draft or revise from general to specific. Orient the reader early, present evidence clearly, and add interpretation or limitation when the reader would otherwise have to guess.
7. Calibrate certainty. Match tense, modality, and causal wording to the strength of the evidence.
8. Run [references/revision-checklist.md](references/revision-checklist.md) before handing text back.

## Section Routing

- Use [references/manuscript-map.md](references/manuscript-map.md) for task triage, section-level move patterns, paragraph roles, and section-specific failure modes.
- Use [references/style-controls.md](references/style-controls.md) for sentence-level control over clarity, ownership, certainty, causality, and rewrite tactics.
- Use [references/workflow-extensions.md](references/workflow-extensions.md) for manuscript assembly order, table/figure storytelling, review articles, lay summaries, and response-to-reviewers discipline.
- Use [references/revision-checklist.md](references/revision-checklist.md) for final review across structure, sentence logic, evidence discipline, and delivery readiness.

## Maintenance Notes

- Keep this entrypoint concise. Put new tactical depth in `references/` unless the routing itself has changed.
- Before adding a new adjacent task here, decide whether it should be routed to another installed skill instead of expanding this one.
- When updating related-skill names or fallback behavior, keep the names aligned with the actual installed skills in the current environment.
- For future maintenance and skill-improvement work only, reviewer-oriented checks may reference `Skill Reviewer` from the `openclaw/skills` repository, and iterative fix loops may reference `Skill Improver` from the `sickn33/antigravity-awesome-skills` repository. Do not add absolute paths here: if those skills are installed, the model can discover them by name; if they are unavailable, say that explicitly to the user. Do not route normal research-writing tasks to these maintenance-only helpers.

## Output Requirements

- Preserve the scientific meaning unless the user explicitly asks to change the claim.
- Preserve numbers, comparisons, and citations unless they are clearly inconsistent with the source text.
- Prefer explicit logic over stylistic variation.
- Repeat the same term for the same concept unless a distinction is intended.
- Avoid unsupported novelty claims, inflated causal claims, and vague pronoun references.

## Common Transformations

- Convert notes into prose by mapping sentence functions first, then drafting the paragraph.
- Convert data-heavy text into readable Results prose by adding commentary around the numbers.
- Convert overclaimed language into evidence-matched language by weakening certainty or causality where needed.
- Convert flat prose into reader-guided prose by making contribution, limitation, or implication explicit.
- Convert display-first study materials into a manuscript section by building the story from tables and figures.
- Convert reviewer criticism into a calm, specific response plus the nearby textual repair it implies.

## Example Requests

- `Use $science-research-writing to rewrite this abstract so the gap, method, and main finding are explicit.`
- `Use $science-research-writing to revise this Discussion paragraph without strengthening the claim.`
- `Use $science-research-writing to turn these bullet points into an Introduction paragraph for a biomedical journal.`
- `Use $science-research-writing to diagnose why this Results paragraph is hard to follow and then rewrite it.`
- `Use $science-research-writing to draft a point-by-point reply to these reviewer comments without sounding defensive.`
- `Use $science-research-writing to turn this paper abstract into a lay summary for non-specialist readers.`
