---
name: gh-issue-create
description: "Turn an implementation discussion into a GitHub issue (with approval), create a worktree, cd into it, enter plan mode, and plan+implement the issue — end to end. Also accepts an existing issue number/URL to skip creation."
disable-model-invocation: true
---

You are an advanced software engineer executing the `/gh-issue-create` skill. This skill runs one deterministic, end-to-end sequence: create (or accept) a GitHub issue, set up an isolated worktree, and drive the implementation from plan mode. Follow the phases in order.

Inspect `$ARGUMENTS`:

- **If `$ARGUMENTS` contains an issue number (e.g. `42`) or a full issue URL** — skip Phase A entirely. Set `N` to that issue number and go straight to Phase B, step 5.
- **Otherwise** — run Phase A to create a new issue from the conversation.

---

## Phase A — Create the issue (normal mode; do NOT enter plan mode here)

Plan mode blocks the `gh issue create` and `git worktree add` steps below, so stay in normal mode for all of Phase A. Plan mode is entered later, in Phase B.

### A1. Analyze Existing Context

Review the current conversation and any referenced files. Extract:

- Goals
- Requirements
- Constraints
- Decisions already made
- Rejected alternatives

Do not ask the user to repeat information already available.

### A2. Resolve Remaining Ambiguities

If implementation details remain unclear, interview the user. Focus on:

- Architecture
- Data flow
- State management
- Edge cases
- Security requirements
- Performance constraints
- Integration points

Continue until all material ambiguities are resolved. The final specification must contain no unresolved questions.

### A3. Draft Specification

Fill in the template at `templates/issue.md` to produce the specification. Follow the guidance embedded in each section.

### A4. Approval Loop (mandatory)

Present:

1. Proposed issue title
2. Full specification

Ask for approval.

If the user requests changes:

- Gather missing information
- Update the specification
- Present it again

**Do not create the issue until explicit approval is received.**

### A5. Create GitHub Issue

After approval:

```bash
gh issue create \
  --title "$TITLE" \
  --body "$SPEC"
```

Extract the issue number from the output and store it as `N`.

If issue creation fails:

- Explain the failure
- Preserve the generated specification
- **Stop. Do not create a worktree and do not proceed to Phase B.**

---

## Phase B — Worktree, session setup, and implementation

### B5. Create the worktree

```bash
git worktree add ../issue-<N> -b issue-<N>
```

If invoked with an existing issue whose branch/worktree already exists, reuse it instead of failing.

Report the issue URL, branch name, and worktree path.

### B6. Enter the worktree (changes the session working directory)

Call the `EnterWorktree` tool with `path: "../issue-<N>"`. This switches the session's working directory into the worktree.

- If `EnterWorktree` rejects the sibling path, do **not** silently fall back. Report the error to the user and ask whether to instead create the worktree under `.claude/worktrees/` via `EnterWorktree` with `name: "issue-<N>"` (this changes the path convention).

### B7. Suggest renaming the session

There is no programmatic way to rename the current session (hooks can only set a title at session start, and no rename tool is exposed). Tell the user to run this themselves to name the session after the issue:

```
/rename issue-<N>
```

### B8. Enter plan mode

Call the `EnterPlanMode` tool. Do not explore, plan, or edit until plan mode is active and the user approves the transition.

### B9. Fetch and analyze the issue

```bash
gh issue view <N> --json number,title,body,labels,comments,state
```

Extract:

1. The exact problem statement or feature request.
2. The clear acceptance criteria / definition of done.
3. Any explicitly mentioned files, modules, functions, or rigid constraints.

### B10. Targeted codebase exploration

Search the local codebase (Grep, Glob, Read) for the symbols, files, and modules referenced in the issue. Read the target code until you understand:

- The current implementation and what specifically must change.
- The active architectural patterns, styling conventions, and testing setup you must follow.
- The precise code entry points.

Stop exploring as soon as you have enough context to assemble a concrete plan.

### B11. Plan, approve, execute

Draft a step-by-step implementation plan naming exactly which files change or are created. Call `ExitPlanMode` to get approval. Once approved, work through the steps in order, verifying each (tests or manual checks) before advancing.

---

## Editing an existing issue

When asked to edit an issue (rather than run the full flow), write the issue's final, intended state:

- Use `gh issue edit <number> --title ... --body ...`.
- The body is the complete, current specification — not a changelog of the conversation.
- Do not append "we discussed X then changed to Y" history; replace stale content with what the issue should now say.
