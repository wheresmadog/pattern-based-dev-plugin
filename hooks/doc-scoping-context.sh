#!/usr/bin/env bash
# SessionStart hook. Fires once per session (startup/resume/clear) and injects
# two documentation-scoping principles as additionalContext.
set -uo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "doc-scoping-context hook: jq not found, skipping" >&2
  exit 1
fi

context=$(cat <<'EOF'
Documentation scoping principles:
- Docs are audience-scoped. README.md speaks to users of the project; CLAUDE.md speaks to developers working on it. Anything relevant only to development — internals, rationale, implementation notes — belongs in the nearest CLAUDE.md, never in README.md.
- Keep docs current with code. When a change touches a file or directory, update the CLAUDE.md and README.md that cover that scope in the same pass, so documentation never drifts out of sync with implementation.
EOF
)

jq -n --arg ctx "$context" '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
