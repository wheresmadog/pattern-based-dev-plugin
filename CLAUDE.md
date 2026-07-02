# claude-dev-skills

A Claude Code plugin that ships four workflow skills. Skills are plain markdown files — no compilation. One skill (`git-commit`) has a companion hook script that requires `jq`.

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

### git-commit (`/git-commit`)
Analyzes staged changes and drafts a commit, handling versioning and pre-commit reformatting.

**Workflow:** `git diff --staged` → bump semver in `pyproject.toml` if warranted (skipped if the file doesn't exist) → sync `uv.lock` if a bump happened and the lockfile exists → draft a Conventional-Commit-style message with a `Changes:` bullet list → commit.

Key invariants:
- Never uses `--no-verify` to bypass pre-commit hooks.
- If a hook reformats files, re-stages the original paths and retries the commit exactly once — a second failure is reported to the user, not looped on.
- Skips the semver/`uv.lock` steps entirely when `pyproject.toml`/`uv.lock` are absent from the repo root.
- A plugin `UserPromptExpansion` hook (`hooks/hooks.json` → `hooks/git-commit-context.sh`) runs the staged-diff/`pyproject.toml`/`uv.lock` lookups *before* the skill's prompt reaches the model, injecting the results as `additionalContext` — the skill never spends a tool call gathering that state itself.

## Plugin structure

```
.claude-plugin/plugin.json       # name, version, author, keywords
.claude-plugin/marketplace.json  # local marketplace catalog (source: "./")
skills/gh-conv-to-issue/SKILL.md  # one file per skill, auto-discovered
skills/gh-issue-to-plan/SKILL.md
skills/cc-module-md/SKILL.md
skills/git-commit/SKILL.md
hooks/hooks.json                 # plugin-level hook registry, auto-discovered
hooks/git-commit-context.sh      # UserPromptExpansion hook for git-commit (requires jq)
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

## Repository

Public: https://github.com/wheresmadog/claude-dev-skills

## Constraints

- Skills that interact with GitHub (`gh-conv-to-issue`, `gh-issue-to-plan`) require `gh` CLI authenticated (`gh auth status`). `git-commit` is plain git and has no `gh` dependency.
- `disable-model-invocation: true` in gh-issue-to-plan's and git-commit's front-matter means they run as a direct instruction set, not a sub-model call — keep the instructions self-contained and deterministic.
- `.claude/settings.local.json` contains a local `ANTHROPIC_BASE_URL` override — do not commit this file to a public repo.
- `hooks/git-commit-context.sh` requires `jq`; it degrades to a no-op (exit 1, stderr note) if `jq` is missing, and the `git-commit` skill falls back to gathering context itself in that case.
