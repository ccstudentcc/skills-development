# Workflow Extensions

Use this file when the task is not only about one paragraph or one section, but about how to assemble, revise, package, or adapt a research writing deliverable.

## Quick Navigation

- Start with `Routing Guide` when the deliverable type is still unclear.
- Jump to `Manuscript Assembly Order` or `Drafting Workflow` for whole-paper build sequencing.
- Jump to `Tables, Figures, and Storytelling` for display-driven writing.
- Jump to `Response to Reviewers`, `Review Article Extension`, or `Lay Summary Extension` for adjacent scholarly formats.

## Routing Guide

| If the user asks for | Start here |
| --- | --- |
| Turn notes into a full manuscript section efficiently | `Manuscript Assembly Order` and `Drafting Workflow` |
| Improve tables, figures, legends, or Results coupling | `Tables, Figures, and Storytelling` |
| Revise after peer review or draft a response letter | `Response to Reviewers` |
| Draft a review article rather than an original manuscript | `Review Article Extension` |
| Convert technical content into a lay summary | `Lay Summary Extension` |

## Related Skill Routing

When the task crosses from prose repair into a neighboring workflow, route intentionally instead of stretching this skill too far.

- Use `doc-coauthoring` from the `anthropics/skills` repository when the user needs a full staged collaboration loop for a long document or multi-section paper.
- Use `canvas-design` from the `anthropics/skills` repository when the deliverable is a concept figure, framework diagram, graphical summary, or other polished static visual.
- Use `citation-management` from the `K-Dense-AI/claude-scientific-writer` repository when references must be found, verified, normalized, or exported in BibTeX or another structured format.
- Use `humanizer` from the `blader/humanizer` repository when the argument and structure are already stable and the remaining job is a final naturalness pass.
- Do not add absolute paths here: if these routed skills are installed, the model can discover them by skill name; if one is unavailable, tell the user plainly and continue with the closest in-skill fallback.

## Missing-Skill Fallback Map

Use these fallbacks only when the routed skill is unavailable in the current environment.

- `doc-coauthoring` unavailable: keep the work inside this skill, but explicitly split the job into clarify, section-plan, draft, and revision passes instead of pretending a staged collaboration skill is active.
- `canvas-design` unavailable: do not promise a finished graphic artifact. Produce a figure brief with panel intent, visual hierarchy, caption draft, and layout notes that another visual workflow can execute later.
- `citation-management` unavailable: only reorganize, normalize, or sanity-check citation information already supplied by the user. Do not invent metadata, DOIs, BibTeX fields, or missing references.
- `humanizer` unavailable: run an internal final pass using `style-controls.md` plus `revision-checklist.md`, focusing on rhythm, repetition, over-regular phrasing, and sentence variety.

## Manuscript Assembly Order

When the manuscript is still being built, do not draft sections in arbitrary order.

Use this sequence unless the user has a strong reason to deviate:

1. Polish the tables and figures first.
2. Draft the Results from those displays.
3. Draft the Methods.
4. Draft the Introduction once the study story is clear.
5. Draft the Discussion after the Results logic is stable.
6. Draft the Abstract and Title last.

Why this order helps:

- tables and figures define the story backbone,
- Results become easier when each display already has a point,
- the Introduction is easier to frame once the real contribution is visible,
- the Abstract becomes simpler after the full logic is already fixed.

## Drafting Workflow

Keep the writing process separated into three jobs.

### 1. Pre-writing

Do this before drafting polished prose:

- collect and sort source material,
- identify the take-home message,
- build a road map at paragraph level,
- group related ideas before writing sentences.

When starting from notes, create a scratch outline with:

- section goal,
- paragraph goals,
- must-keep evidence,
- sentence jobs,
- points that still need caveats.

### 2. First Draft

The first draft is for logic, not elegance.

- get the ideas down in complete sentences,
- prioritize organization over local polish,
- leave sentence-level beautification for revision,
- keep moving once the paragraph logic is clear.

### 3. Revision

Revision is where most quality gains happen.

Run this sequence:

1. Read the passage aloud.
2. Mark the main verb in each sentence and check whether it is vivid, active, and not buried.
3. Cut clutter, especially dead openings, empty intensifiers, and nominalized verbs.
4. Tag each paragraph with its main point and reorder if the flow is weak.
5. Re-check numerical, reference, and cross-section consistency.

## Tables, Figures, and Storytelling

Treat tables and figures as the foundation of the manuscript story, not as attachments.

### Core Rules

- Each table or figure should make one clear point.
- A table or figure should stand alone with a usable title or legend.
- Do not present the same data in both a table and a figure unless the user explicitly needs both.
- Results prose should summarize the point of the display, not read it line by line.

### Tables

Use tables when the reader needs precise values or many variables.

Check:

- does the title state the point, not just the topic,
- are units visible,
- are abbreviations defined inside the table,
- are decimal places and alignment professional and consistent,
- can footnotes carry technical detail instead of bloating the body text.

### Figures

Use figures when the point is trend, contrast, pattern, or process.

Check:

- does the graph tell a quick visual story,
- can the groups be distinguished easily,
- are axes, symbols, and legends readable,
- would a table communicate the data more honestly if the graphic is too dense,
- does the figure legend let the reader understand the display without hunting elsewhere.

### Results Coupling

When writing prose around a display:

1. state the take-home message first,
2. cite the display,
3. mention only the key values needed for emphasis,
4. leave exhaustive values in the table or figure,
5. mention negative or control findings when they matter.

## Response to Reviewers

Use this when the user needs a revision memo, cover letter, or point-by-point reply.

### Tone

- be specific,
- be respectful,
- do not sound defensive,
- fix the real issue even when the reviewer named it imperfectly.

### Response Pattern

For each reviewer point:

1. restate the concern briefly,
2. say what was changed,
3. identify where the change now appears,
4. if disagreeing, explain the reason clearly and politely.

### Common Failure Modes

- replying emotionally instead of analytically,
- answering the comment without fixing the nearby writing problem that triggered it,
- giving vague statements such as `we clarified this` without naming the change,
- ignoring comments when submitting to a different journal.

## Review Article Extension

Use this only when the user explicitly wants a review article rather than an original research manuscript.

### Core Shift

The goal changes from reporting one study to synthesizing a body of literature around a narrow, well-defined thesis.

### Workflow

1. Define a focused theme, not just a broad topic area.
2. Organize the literature by question, method, mechanism, controversy, or chronology.
3. Separate what is known, what remains contested, and what remains unknown.
4. End with gaps, recommendations, or future directions that follow from the synthesis.

### Failure Modes

- topic too broad to be coherent,
- source dumping without synthesis,
- section list driven by paper order rather than argument structure.

## Lay Summary Extension

Use this only when the user explicitly wants writing for a broad audience.

### Core Shift

Move the take-home message to the front, reduce jargon, and strip away details that do not change what a non-specialist reader needs to understand.

### Working Rules

- start with why the reader should care,
- use plain language before specialist terminology,
- explain risk with absolute values or whole-number framing when possible,
- keep only the details that support the main public-facing point,
- turn the research into a short story rather than a miniature paper.

### Failure Modes

- opening with technical background instead of the news,
- keeping scientist-speak that general readers cannot decode,
- reporting relative risk without giving understandable context,
- preserving so much method detail that the main message disappears.
