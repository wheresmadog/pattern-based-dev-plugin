# claude-dev-skills

A Claude Code plugin that ships four workflow skills. Skills are plain markdown files — no compilation. `commit-draft` has a companion hook script, and `gh-issue-implement`/`update-claude-md` have a pair of hook scripts that force plan mode — all three require `jq`.

## Skills

### gh-issue-create (`/gh-issue-create`)
Turns a free-form implementation discussion into a formal GitHub issue.

**Workflow:** interview user → draft spec (goal, requirements, approach, edge cases, verification steps) → approval loop → `gh issue create` → `git worktree add`.

Key invariants:
- Never creates an issue without explicit user approval.
- Never creates a worktree if issue creation fails.
- When editing an existing issue, writes the complete final state — no changelog prose.

### gh-issue-implement (`/gh-issue-implement <issue>`)
Fetches a GitHub issue and implements it.

**Workflow:** `gh issue view` → extract acceptance criteria → targeted codebase exploration → step-by-step plan → execute + verify each step.

Accepts a bare number (`42`) or a full URL as `$ARGUMENTS`.

Key invariants:
- A plugin `UserPromptExpansion` hook (`hooks/hooks.json` → `hooks/plan-mode-prompt.sh`) instructs the model to call `EnterPlanMode` before this skill's own explore/plan/execute steps run, since the skill otherwise designs and executes in one pass.

### update-claude-md (`/update-claude-md`)
Generates a structured `CLAUDE.md` for the current module.

Sections: Module Purpose, Feature Overview, Module Boundaries, Internal Architecture, Integration Points, Domain Model, Change Guide, Directory Guide, Mental Model.

Focus: architectural understanding for onboarding engineers, not a file inventory.

Key invariants:
- Same `UserPromptExpansion` hook as `gh-issue-implement` forces plan mode when invoked via `/update-claude-md`. Unlike `gh-issue-implement`, this skill has no `disable-model-invocation` flag, so the model can also invoke it directly via the `Skill` tool mid-conversation — a `PreToolUse` hook (`hooks/plan-mode-guard.sh`) denies that call until plan mode is active, since `UserPromptExpansion` never fires for a `Skill` tool call.

### commit-draft (`/commit-draft`)
Analyzes staged changes and drafts a commit, handling versioning and pre-commit reformatting.

**Workflow:** `git diff --staged` → bump semver in `pyproject.toml` if warranted (skipped if the file doesn't exist) → sync `uv.lock` if a bump happened and the lockfile exists → draft a Conventional-Commit-style message with a `Changes:` bullet list → commit.

Key invariants:
- Never uses `--no-verify` to bypass pre-commit hooks.
- If a hook reformats files, re-stages the original paths and retries the commit exactly once — a second failure is reported to the user, not looped on.
- Skips the semver/`uv.lock` steps entirely when `pyproject.toml`/`uv.lock` are absent from the repo root.
- A plugin `UserPromptExpansion` hook (`hooks/hooks.json` → `hooks/commit-draft-context.sh`) runs the staged-diff/`pyproject.toml`/`uv.lock` lookups *before* the skill's prompt reaches the model, injecting the results as `additionalContext` — the skill never spends a tool call gathering that state itself.

## Plugin structure

```
.claude-plugin/plugin.json       # name, version, author, keywords
.claude-plugin/marketplace.json  # local marketplace catalog (source: "./")
.cursor-plugin/plugin.json       # Cursor plugin manifest (name, version, author)
skills/gh-issue-create/SKILL.md  # one file per skill, auto-discovered
skills/gh-issue-implement/SKILL.md
skills/update-claude-md/SKILL.md
skills/commit-draft/SKILL.md
hooks/hooks.json                 # plugin-level hook registry, auto-discovered
hooks/commit-draft-context.sh      # UserPromptExpansion hook for commit-draft (requires jq)
hooks/plan-mode-prompt.sh          # UserPromptExpansion hook forcing plan mode for gh-issue-implement/update-claude-md
hooks/plan-mode-guard.sh           # PreToolUse hook denying autonomous Skill-tool calls to those skills outside plan mode
```

`hooks/` is intentionally not mirrored under `.cursor-plugin/` — Cursor has no confirmed per-prompt hook equivalent to `UserPromptExpansion`/`PreToolUse` (its confirmed hook surface is a `workspaceOpen` hook, firing once per workspace rather than per-prompt). Under Cursor, `commit-draft`, `gh-issue-implement`, and `update-claude-md` simply run without their hook firing — the same fallback path each skill already exercises when `jq` is missing (see Constraints below).

Manifest format references: [Claude Code plugins](https://code.claude.com/docs/en/plugins) for `.claude-plugin/plugin.json`, [Cursor plugins](https://cursor.com/docs/plugins) (field reference: [cursor.com/docs/reference/plugins](https://cursor.com/docs/reference/plugins)) for `.cursor-plugin/plugin.json`.

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

- Skills that interact with GitHub (`gh-issue-create`, `gh-issue-implement`) require `gh` CLI authenticated (`gh auth status`). `commit-draft` is plain git and has no `gh` dependency.
- `disable-model-invocation: true` in gh-issue-implement's and commit-draft's front-matter means they run as a direct instruction set, not a sub-model call — keep the instructions self-contained and deterministic.
- `.claude/settings.local.json` contains a local `ANTHROPIC_BASE_URL` override — do not commit this file to a public repo.
- `hooks/commit-draft-context.sh` requires `jq`; it degrades to a no-op (exit 1, stderr note) if `jq` is missing, and the `commit-draft` skill falls back to gathering context itself in that case.
- `hooks/plan-mode-prompt.sh` and `hooks/plan-mode-guard.sh` also require `jq`; each degrades to a no-op if `jq` is missing, meaning `gh-issue-implement`/`update-claude-md` simply run without the plan-mode gate rather than failing.
