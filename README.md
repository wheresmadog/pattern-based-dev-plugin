# my-git-plugin

A Claude Code plugin bundling three GitHub workflow skills:

| Skill | Invocation | Purpose |
|-------|-----------|---------|
| **gh-conv-to-issue** | `/gh-conv-to-issue` | Turn an implementation discussion into a fully specified GitHub issue, obtain approval, create the issue, and create a dedicated worktree. |
| **gh-issue-to-plan** | `/gh-issue-to-plan <issue>` | Fetch a GitHub issue via the `gh` CLI, explore the local codebase, design a plan, and execute the changes. Accepts an issue number (`42`) or full URL. |
| **cc-module-md** | `/cc-module-md` | Generate a structured `CLAUDE.md` for the current module — responsibilities, architecture, integration points, and a developer mental model. |

**Prerequisite:** All skills that interact with GitHub shell out to the GitHub CLI (`gh`). Verify it is installed and authenticated before use:

```bash
gh auth status
```

## Install (local)

Register this plugin's marketplace and install:

```bash
/plugin marketplace add /home/ygkim/my-git-plugin
/plugin install my-git-plugin@my-git-plugin
```

Open `/plugin` to confirm `my-git-plugin` is enabled.

## Install (public GitHub repo)

Once published to GitHub, anyone can install it directly:

```bash
/plugin marketplace add https://github.com/<owner>/my-git-plugin
/plugin install my-git-plugin@my-git-plugin
```

## Structure

```
my-git-plugin/
├── .claude-plugin/
│   ├── plugin.json          # plugin manifest (name, version, author)
│   └── marketplace.json     # local marketplace catalog
├── skills/
│   ├── gh-conv-to-issue/SKILL.md  # spec → approve → create issue → worktree
│   ├── gh-issue-to-plan/SKILL.md  # fetch issue → explore → plan → implement
│   └── cc-module-md/SKILL.md      # generate CLAUDE.md for current module
└── CLAUDE.md                # developer guide for this plugin
```

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` with a YAML front-matter block:
   ```yaml
   ---
   name: my-skill
   description: One-line description shown in /skills list.
   ---
   ```
2. Write the skill body — plain markdown instructions Claude executes when the skill is invoked.
3. No changes to `plugin.json` or `marketplace.json` are required; skills are auto-discovered from the `skills/` directory.
