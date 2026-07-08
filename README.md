# claude-dev-skills

## Features

| Skill | Invocation | Purpose |
|-------|-----------|---------|
| **gh-issue-create** | `/gh-issue-create` | Turn an implementation discussion into a fully specified GitHub issue, obtain approval, create the issue, and create a dedicated worktree. |
| **gh-issue-implement** | `/gh-issue-implement <issue>` | Fetch a GitHub issue via the `gh` CLI, explore the local codebase, design a plan, and execute the changes. Accepts an issue number (`42`) or full URL. |
| **update-claude-md** | `/update-claude-md` | Generate a structured `CLAUDE.md` for the current module — responsibilities, architecture, integration points, and a developer mental model. |
| **commit-draft** | `/commit-draft` | Analyze staged changes, bump semver in `pyproject.toml`/`uv.lock` when present, draft a Conventional-Commit message, and commit — retrying once after pre-commit hook reformatting. |

## Prerequisite

`gh-issue-create` and `gh-issue-implement` shell out to the GitHub CLI (`gh`). Verify it is installed and authenticated before use:

```bash
gh auth status
```

## Install

### Claude Code

Once published to GitHub, anyone can install it directly:

```bash
/plugin marketplace add https://github.com/wheresmadog/claude-dev-skills
/plugin install claude-dev-skills@claude-dev-skills
```

### Cursor

Clone (or symlink, for local development) the repo directly into Cursor's local plugins directory — this repo's layout already has `.cursor-plugin/plugin.json` at its root, matching what Cursor expects:

```bash
git clone https://github.com/wheresmadog/claude-dev-skills ~/.cursor/plugins/local/claude-dev-skills
```

```bash
ln -s /path/to/claude-dev-skills ~/.cursor/plugins/local/claude-dev-skills
```

Then restart Cursor, or run **Developer: Reload Window**.

## Platform notes

### Claude Code

Fully supported, including the automatic plan-mode gate and pre-fetched context that `gh-issue-implement`, `update-claude-md`, and `commit-draft` rely on.

### Cursor

Runs all four skills too, but without those hooks — skills just gather their own context and skip the automatic plan-mode step, the same graceful fallback that happens when `jq` is missing.

See `CLAUDE.md` for the plugin's internal structure and how to add or modify a skill.
