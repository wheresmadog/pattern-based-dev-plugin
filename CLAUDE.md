# my-git-plugin

A Claude Code plugin that ships three GitHub workflow skills. Skills are plain markdown files — no compilation, no runtime dependencies.

## Skills

### gh-conv-to-issue (`/gh-conv-to-issue`)
Turns a free-form implementation discussion into a formal GitHub issue.

**Workflow:** interview user → draft spec (goal, requirements, approach, edge cases, verification steps) → approval loop → `gh issue create` → `git worktree add`.

Key invariants:
- Never creates an issue without explicit user approval.
- Never creates a worktree if issue creation fails.
- When editing an existing issue, writes the complete final state — no changelog prose.

### gh-issue-to-plan (`/gh-issue-to-plan <issue>`)
Fetches a GitHub issue and implements it.

**Workflow:** `gh issue view` → extract acceptance criteria → targeted codebase exploration → step-by-step plan → execute + verify each step.

Accepts a bare number (`42`) or a full URL as `$ARGUMENTS`.

### cc-module-md (`/cc-module-md`)
Generates a structured `CLAUDE.md` for the current module.

Sections: Module Purpose, Feature Overview, Module Boundaries, Internal Architecture, Integration Points, Domain Model, Change Guide, Directory Guide, Mental Model.

Focus: architectural understanding for onboarding engineers, not a file inventory.

## Plugin structure

```
.claude-plugin/plugin.json       # name, version, author, keywords
.claude-plugin/marketplace.json  # local marketplace catalog (source: "./")
skills/gh-conv-to-issue/SKILL.md  # one file per skill, auto-discovered
skills/gh-issue-to-plan/SKILL.md
skills/cc-module-md/SKILL.md
```

## Adding a skill

1. `mkdir skills/<name> && touch skills/<name>/SKILL.md`
2. Add YAML front-matter:
   ```yaml
   ---
   name: <name>
   description: One line shown in /skills.
   ---
   ```
3. Write the skill body in markdown below the front-matter.
4. No changes to `plugin.json` or `marketplace.json` needed.

## Constraints

- Skills that interact with GitHub require `gh` CLI authenticated (`gh auth status`).
- `disable-model-invocation: true` in gh-issue-to-plan's front-matter means it runs as a direct instruction set, not a sub-model call — keep the instructions self-contained and deterministic.
- `.claude/settings.local.json` contains a local `ANTHROPIC_BASE_URL` override — do not commit this file to a public repo.
