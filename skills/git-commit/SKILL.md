---
name: git-commit
description: "Draft an automated semver bump and formatted commit message from staged changes"
disable-model-invocation: true
---

You are an automated Git workflow helper running the `/commit` skill. Follow this process step-by-step:

### Step 1: Analyze Staged Changes
Run a terminal tool to execute:
! git diff --staged

If there are no staged changes, stop immediately and alert the user to stage their files first.

Also capture the exact list of staged paths — you will need it later to re-stage after pre-commit reformatting:
! git diff --staged --name-only

### Step 2: Determine SemVer Bump
Check if `pyproject.toml` exists in the repository root.
- If it **does not** exist, skip this step.
- If it **does** exist, read the current version string. Analyze the nature of the staged changes from Step 1 to determine the appropriate Semantic Versioning bump (`patch`, `minor`, or `major`). If the changes do not warrant a bump, mark it as "no bump".

If a bump is warranted, edit `pyproject.toml` to the new version and stage it:
! git add pyproject.toml

### Step 3: Sync `uv.lock`
Only if Step 2 produced a version bump **and** a `uv.lock` file exists in the repository root.

The project version is recorded in `uv.lock`, so a bump leaves the lock out of sync. Regenerate and stage it:
! uv lock
! git add uv.lock

- `uv lock` only rewrites the version metadata here, so it is fast and must not pull new dependency versions. If it reports unexpected dependency changes, stop and report them instead of staging.
- If `uv` is not installed, report that `uv.lock` could not be synced and let the user decide; do not proceed silently.

### Step 4: Draft the Commit Message
Draft a commit message based *strictly* on the staged changes using this exact template format:

```text
<title>

Changes:
- `<path/to/file>`: <description>
- `<path/to/file>`: <description>
```

- The `<title>` must be a concise Conventional-Commit-style summary (e.g. `feat(index): ...`, `fix(db): ...`).
- List one bullet per meaningfully changed file. Group trivial files (e.g. `uv.lock`) into a single bullet.

### Step 5: Commit, Handling Pre-commit Reformatting
This repo runs `ruff-check --fix` and `ruff-format` via pre-commit. Those hooks **auto-fix files in place and abort the commit** when they change anything (see `.pre-commit-config.yaml`). Handle that:

1. Run the commit with your drafted message.
2. If the commit **succeeds**, you are done — report the new commit hash.
3. If the commit **fails because a hook modified files** ("files were modified by this hook"):
   - Re-stage only the paths that were already part of this commit (the list from Step 1, plus `pyproject.toml`/`uv.lock` if you staged them):
     ! git add <those-paths>
   - Run the commit again with the same message.
   - If it fails a **second** time, stop and show the user the hook output — do not loop. A repeated failure usually means a lint error the hooks cannot auto-fix, which needs a human.
4. Never use `--no-verify` to bypass the hooks.

After a successful commit, report the commit hash and a one-line summary.
