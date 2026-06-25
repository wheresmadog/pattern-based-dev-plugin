---
name: gh-issue-to-plan
description: "Fetch a GitHub issue via CLI, explore the local codebase, design a plan, and execute changes"
disable-model-invocation: true
---

You are an advanced software engineer executing the `/gh-resolve` skill. Use the runtime argument passed in by the user (available via $ARGUMENTS) to complete the workflow below.

### Step 1: Fetch and Analyze the GitHub Issue
Inspect the text passed into `$ARGUMENTS`. It must contain either a raw issue number (e.g., `42`) or a full GitHub issue URL (e.g., `https://github.com/owner/repo/issues/42`).

Execute a terminal tool to retrieve the issue data directly:
! gh issue view "$ARGUMENTS" --json number,title,body,labels,comments,state

Carefully analyze the terminal response and extract:
1. The exact problem statement or feature request.
2. The clear acceptance criteria / definition of done.
3. Any explicitly mentioned files, modules, code blocks, functions, or rigid constraints.

### Step 2: Targeted Codebase Exploration
Search the local codebase using your search and file tools (such as Grep, Glob, or File Reading) to find the symbols, files, and modules referenced in the issue. Read the target code until you clearly understand:
- The state of the current implementation and what specific components must change.
- The active architectural patterns, styling conventions, and testing setups you must follow.
- The precise code entry points.

*Efficiency rule:* Stop exploring the codebase as soon as you have sufficient technical context to assemble a concrete, deterministic engineering plan.

### Step 3: Formulate and Execute the Implementation Plan
Draft a step-by-step engineering plan detailing exactly which files will be modified or created. Present this plan to the user briefly.

Once established, systematically work through your plan steps in sequential order. Run native testing tools or manual checks to verify the integrity of each step before advancing to the next.
