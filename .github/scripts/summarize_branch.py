"""Summarize the current branch vs origin/main into a PR title + body.

Run via:  uv run --with litellm --no-project --python 3.12 \
              python .github/scripts/summarize_branch.py

Output contract (stdout):
  line 1     -> PR title
  lines 2..n -> PR body (markdown)

Exits non-zero on any failure so the workflow falls back to a commit-list body.
"""

import os
import subprocess
import sys

MODEL = "openrouter/anthropic/claude-haiku-4.5"  # cheap, fast — right tier for a short summary
MAX_DIFF_CHARS = 12_000
BASE = "origin/main"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> int:
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("OPENROUTER_API_KEY not set", file=sys.stderr)
        return 1

    commits = _git("log", "--pretty=format:- %s%n%b", f"{BASE}..HEAD")
    diffstat = _git("diff", "--stat", f"{BASE}...HEAD")
    diff = _git("diff", f"{BASE}...HEAD")

    if not commits and not diff:
        print("No changes vs base", file=sys.stderr)
        return 1

    truncated = len(diff) > MAX_DIFF_CHARS
    if truncated:
        diff = diff[:MAX_DIFF_CHARS]

    prompt = f"""You are writing a GitHub pull request description.

From the commit messages, the diffstat, and the (possibly truncated) diff below,
produce a concise PR title and body.

STRICT OUTPUT FORMAT:
- The FIRST line is the PR title: imperative mood, <= 70 chars, no leading "Draft:".
- Every line AFTER the first is the PR body in GitHub-flavored markdown.
- The body should be a 1-2 sentence summary, then a "## Changes" bullet list of the
  notable changes. Only describe changes present in the diff/commits; do not invent any.
- Do not wrap the output in code fences.

=== COMMITS ===
{commits or "(none)"}

=== DIFFSTAT ===
{diffstat or "(none)"}

=== DIFF{" (TRUNCATED)" if truncated else ""} ===
{diff or "(none)"}
"""

    # Local import so a missing dependency surfaces as a clean fallback, not a crash.
    from litellm import completion

    resp = completion(
        model=MODEL,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    content = (resp.choices[0].message.content or "").strip()
    if not content:
        print("Empty LLM response", file=sys.stderr)
        return 1

    if truncated:
        content += "\n\n_Note: the diff was truncated for summarization._"

    print(content)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # any failure -> workflow's bash fallback
        print(f"summarize_branch failed: {exc}", file=sys.stderr)
        sys.exit(1)
