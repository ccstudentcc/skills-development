---
name: science-research-writing
description: Draft, revise, and diagnose English scientific manuscript prose for abstracts, introductions, methods, results, discussions, conclusions, titles, and paragraph-level rewrites. Use when Codex needs to turn notes or rough text into journal-style research writing, align a section with its expected rhetorical moves, or improve sentence-level choices such as tense, voice, hedging, cohesion, causality, and terminology consistency.
---

# Science Research Writing

## Overview

Use this skill to produce research prose that is easy to follow, structurally appropriate for the target section, and faithful to the available evidence. Make the reader's path explicit instead of relying on the reader to infer function, relevance, or certainty.

## Use This Skill When

- Draft a manuscript section from notes, figures, or bullet points.
- Revise rough scientific prose into clearer journal-style English.
- Diagnose why a paragraph feels weak, confusing, overclaimed, or structurally mismatched.
- Tighten an abstract, title, or conclusion so the contribution is easier to understand.

## Do Not Use This Skill For

- Citation lookup, BibTeX repair, or literature search.
- Journal template formatting, reference-style conversion, or submission portal tasks.
- Domain-specific scientific judgments that require missing background knowledge or new evidence.

## Workflow

1. Identify the job: draft, revise, or diagnose.
2. Identify the target section and read the matching guidance in [references/manuscript-map.md](references/manuscript-map.md).
3. Read [references/style-controls.md](references/style-controls.md) when the task involves tense, voice, hedging, cohesion, causality, articles, or terminology.
4. Build the paragraph plan in sentence functions before writing. Decide what each sentence must do for the reader, not just what information it contains.
5. Draft or revise from general to specific. Orient the reader early, present evidence clearly, and add interpretation or limitation when the reader would otherwise have to guess.
6. Calibrate certainty. Match tense, modality, and causal wording to the strength of the evidence.
7. Run [references/revision-checklist.md](references/revision-checklist.md) before handing text back.

## Section Routing

- Use [references/manuscript-map.md](references/manuscript-map.md) for section-level move patterns, paragraph roles, and section-specific failure modes.
- Use [references/style-controls.md](references/style-controls.md) for sentence-level control over clarity, ownership, certainty, and precision.
- Use [references/revision-checklist.md](references/revision-checklist.md) for final review across structure, sentence logic, grammar, and evidence discipline.

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

## Example Requests

- `Use $science-research-writing to rewrite this abstract so the gap, method, and main finding are explicit.`
- `Use $science-research-writing to revise this Discussion paragraph without strengthening the claim.`
- `Use $science-research-writing to turn these bullet points into an Introduction paragraph for a biomedical journal.`
- `Use $science-research-writing to diagnose why this Results paragraph is hard to follow and then rewrite it.`
