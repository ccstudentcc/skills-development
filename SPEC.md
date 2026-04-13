# Science Research Writing Skill Specification

## Goal

Create two reusable writing skills based on the source material in `references/`:

- `science-research-writing` for English scientific manuscript prose
- `science-research-writing-zh` for Chinese scientific manuscript prose

## Scope

- Rewrite `references/Science Research Writing.md` into clear, fully English reference material.
- Preserve the user-added Chinese reference material at `references/Science Research Writing-zh.md`.
- Create portable skill folders under `skills/science-research-writing/` and `skills/science-research-writing-zh/`.
- Keep the English skill fully in English.
- Keep the Chinese skill aligned with Chinese scientific writing conventions and Chinese user phrasing.
- Initialize this workspace as a git repository, publish it to a public remote repository, and push the resulting branch.

## Constraints

- Keep the skill focused on scientific manuscript drafting and revision rather than generic English writing.
- Prefer progressive disclosure: keep `SKILL.md` concise and move detailed guidance into `references/`.
- Avoid scripts or assets unless they add clear value.
- Do not include secrets, credentials, or environment-specific assumptions.

## Acceptance Criteria

- `references/Science Research Writing.md` contains no Chinese text.
- `skills/science-research-writing/SKILL.md` has valid frontmatter with only `name` and `description`.
- `skills/science-research-writing-zh/SKILL.md` has valid frontmatter with only `name` and `description`.
- The skill folder includes any referenced files and no orphaned resources.
- `agents/openai.yaml` exists and matches the skill.
- Validation passes for both skills with the available skill validator.
- A self-review based on the named reviewer methodology finds no unresolved critical or major issues.
- The repository is initialized with git, pushed to a public remote, and the final status is clean or intentionally documented.
