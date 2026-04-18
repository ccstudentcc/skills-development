# AGENTS.md Research Sources

Date: 2026-04-17

## Notes

- Tier 1 = papers / research papers
- Tier 2 = official docs / official engineering blogs
- Tier 3 = strong GitHub repository cases / open practice standards
- Directness:
  - direct: directly discusses instruction files such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or repository custom instructions
  - indirect: does not discuss `AGENTS.md` directly, but supports adjacent principles used in this research

## Source Register

| Tier | Source | URL | Directness | How used in this research |
| --- | --- | --- | --- | --- |
| 1 | Eric Wallace et al., *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions* (2024) | https://arxiv.org/abs/2404.13208 | indirect | Supports instruction precedence, trusted vs untrusted input separation, and conflict handling |
| 1 | John Yang et al., *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* (2024) | https://arxiv.org/abs/2405.15793 | indirect | Supports explicit command surfaces, agent-friendly interfaces, and repository-level validation guidance |
| 1 | John Yang et al., *SWE-agent* NeurIPS 2024 proceedings page | https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html | indirect | Confirms published venue and abstract details for the SWE-agent argument |
| 1 | Chunqiu Steven Xia et al., *Agentless: Demystifying LLM-based Software Engineering Agents* (2024) | https://arxiv.org/abs/2407.01489 | indirect | Supports the argument for simpler, interpretable workflows over excessive agent complexity |
| 1 | Chunqiu Steven Xia et al., *Demystifying LLM-Based Software Engineering Agents* (FSE 2025) | https://doi.org/10.1145/3715754 | indirect | Confirms the published form of Agentless and supports the simplicity baseline argument |
| 2 | Anthropic, *How Claude remembers your project* | https://docs.anthropic.com/en/docs/claude-code/memory | direct | Used for hierarchy, recursive loading, imports, and rule admission triggers |
| 2 | Anthropic, *Best Practices for Claude Code* | https://docs.anthropic.com/en/docs/claude-code/best-practices | direct | Used for brevity, specificity, verification-first writing, and what to exclude from shared instruction files |
| 2 | Anthropic, *Security* | https://docs.anthropic.com/en/docs/claude-code/security | direct | Used for permission boundaries, untrusted content handling, and least-privilege recommendations |
| 2 | GitHub Docs, *Adding repository custom instructions for GitHub Copilot* | https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot | direct | Used for repository-wide vs path-specific instructions and nearest-AGENTS precedence in Copilot |
| 2 | GitHub Docs, *Adding personal custom instructions for GitHub Copilot* | https://docs.github.com/en/copilot/how-tos/custom-instructions/adding-personal-custom-instructions-for-github-copilot | direct | Used for priority and merge behavior across personal, repository, and organization instructions |
| 2 | OpenAI Developers, *Codex* | https://developers.openai.com/codex | direct | Used to confirm that `AGENTS.md` is treated as a first-class Codex configuration area |
| 2 | OpenAI Developers, *Rules* | https://developers.openai.com/codex/rules | indirect | Used for restrictive-rule precedence, least privilege, and approval governance patterns |
| 2 | OpenAI Engineering, *Harness engineering: leveraging Codex in an agent-first world* | https://openai.com/index/harness-engineering/ | direct | Used for golden-principles encoding, ongoing cleanup, and the idea that agent reliability comes from environment and feedback design |
| 2 | Anthropic, *Enterprise deployment overview* | https://docs.anthropic.com/en/docs/claude-code/third-party-integrations | direct | Used for organization-level investment in documentation, repository memory, and centrally managed integration patterns |
| 3 | OpenAI Codex repository `AGENTS.md` | https://raw.githubusercontent.com/openai/codex/main/AGENTS.md | direct | Primary case study for a dense, validation-heavy repository `AGENTS.md` |
| 3 | Google Gemini CLI repository `GEMINI.md` | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/GEMINI.md | direct | Case study for repository overview + command + validation + documentation guidance |
| 3 | Google GitHub Action `run-gemini-cli` | https://github.com/google-github-actions/run-gemini-cli | direct | Evidence that repo-level context files are part of official automation workflows |
| 3 | AGENTS.md open format website | https://agents.md/ | direct | Used for README-vs-AGENTS positioning and nested AGENTS guidance in the broader ecosystem |
| 3 | `agentsmd/agents.md` repository | https://github.com/agentsmd/agents.md | direct | Case study for the open-format framing and minimal example structure |

## Source Quality Assessment

### Strongest direct sources

- Anthropic Claude Code docs
- GitHub Copilot docs
- OpenAI Codex docs and engineering writing
- OpenAI Codex repository `AGENTS.md`
- Google Gemini official repositories

### Strongest indirect sources

- Instruction hierarchy paper
- SWE-agent paper
- Agentless paper

## Evidence Gaps Logged During Research

1. No dedicated peer-reviewed paper was found that specifies `AGENTS.md` authoring or update governance directly.
2. Most direct operational guidance comes from vendor docs, not neutral standards bodies.
3. Cross-tool precedence behavior is similar in spirit but not identical in implementation, so portability claims should stay conservative.
