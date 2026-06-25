---
name: gh-conv-to-issue
description: Turn an implementation discussion into a fully specified GitHub issue, obtain approval, create the issue, and create a dedicated worktree.
---

# GH Issue

When invoked:

## Analyze Existing Context

Review the current conversation and any referenced files.

Extract:

- Goals
- Requirements
- Constraints
- Decisions already made
- Rejected alternatives

Do not ask the user to repeat information already available.

## Resolve Remaining Ambiguities

If implementation details remain unclear, interview the user.

Focus on:

- Architecture
- Data flow
- State management
- Edge cases
- Security requirements
- Performance constraints
- Integration points

Continue until all material ambiguities are resolved.

The final specification must contain no unresolved questions.

## Draft Specification

Create a specification containing:

### Summary / Goal

### Background & Context

### Requirements

### Technical Approach

### Edge Cases & Failure Modes

### Security & Performance Considerations

### Integration Points

### Out of Scope

### Manual Verification Steps

Verification steps must be:

- Observable
- Deterministic
- Unambiguous

## Approval Loop

Present:

1. Proposed issue title
2. Full specification

Ask for approval.

If the user requests changes:

- Gather missing information
- Update the specification
- Present it again

Do not create the issue until explicit approval is received.

## Create GitHub Issue

After approval:

```bash
gh issue create \
  --title "$TITLE" \
  --body "$SPEC"
```

If issue creation fails:

- Explain the failure
- Preserve the generated specification
- Stop

Do not create a worktree.

## Create Worktree

After successful issue creation:

1. Extract the issue number.
2. Create branch name:

   issue-<number>

3. Create worktree:

```bash
git worktree add ../issue-<number> -b issue-<number>
```

Report:

- Issue URL
- Branch name
- Worktree path

## Edit an Existing Issue

When asked to edit an issue, write the issue's final, intended state.

- Use `gh issue edit <number> --title ... --body ...`.
- The body is the complete, current specification — not a changelog of the conversation.
- Do not append "we discussed X then changed to Y" history; replace stale content with what the issue should now say.
