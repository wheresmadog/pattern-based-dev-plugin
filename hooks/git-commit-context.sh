#!/usr/bin/env bash
# UserPromptExpansion hook for the git-commit skill.
# Runs before the skill's prompt reaches the model and injects the staged
# diff / pyproject.toml / uv.lock state as additionalContext, so the model
# never has to spend a tool call gathering it.
set -uo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "git-commit-context hook: jq not found, skipping context injection" >&2
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

staged_diff=$(git diff --staged)
staged_files=$(git diff --staged --name-only)

if [ -f pyproject.toml ]; then
  pyproject_status=$(cat pyproject.toml)
else
  pyproject_status="(pyproject.toml not present)"
fi

if [ -f uv.lock ]; then
  uvlock_status="(uv.lock present)"
else
  uvlock_status="(uv.lock not present)"
fi

context=$(cat <<EOF
Staged diff (git diff --staged):
${staged_diff:-(no staged changes)}

Staged file list (git diff --staged --name-only):
${staged_files:-(no staged changes)}

pyproject.toml:
${pyproject_status}

uv.lock: ${uvlock_status}
EOF
)

jq -n --arg ctx "$context" '{hookSpecificOutput: {hookEventName: "UserPromptExpansion", additionalContext: $ctx}}'
