# Science Research Writing Skill Specification

## Goal

Create a reusable English-language skill named `science-research-writing` based on the material in `references/Science Research Writing.md`.

## Scope

- Rewrite `references/Science Research Writing.md` into clear, fully English reference material.
- Create a portable skill folder under `skills/science-research-writing/`.
- Keep the skill itself fully in English, including `SKILL.md`, any bundled references, and agent metadata.
- Initialize this workspace as a git repository, publish it to a public remote repository, and push the resulting branch.

## Constraints

- Keep the skill focused on scientific manuscript drafting and revision rather than generic English writing.
- Prefer progressive disclosure: keep `SKILL.md` concise and move detailed guidance into `references/`.
- Avoid scripts or assets unless they add clear value.
- Do not include secrets, credentials, or environment-specific assumptions.

## Acceptance Criteria

- `references/Science Research Writing.md` contains no Chinese text.
- `skills/science-research-writing/SKILL.md` has valid frontmatter with only `name` and `description`.
- The skill folder includes any referenced files and no orphaned resources.
- `agents/openai.yaml` exists and matches the skill.
- Validation passes with the available skill validator.
- A self-review based on the named reviewer methodology finds no unresolved critical or major issues.
- The repository is initialized with git, pushed to a public remote, and the final status is clean or intentionally documented.
