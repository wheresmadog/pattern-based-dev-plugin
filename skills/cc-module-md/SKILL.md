---
name: cc-module-md
description: Create a CLAUDE.md for this module only.
---

# Claude MD

When invoked, create a `CLAUDE.md` for the current module.

Treat this module as a subsystem within a larger application. Focus on the module's responsibilities, features, boundaries, and interactions with the rest of the system.

Do NOT produce a file-by-file inventory unless a file is exceptionally important to understanding the module.

## Structure

Fill in the template at `templates/claude-md.md` to produce the document. Follow the guidance embedded in each section.

## Guidelines

* Optimize for onboarding engineers who need to work on this module.
* Explain responsibilities and feature ownership rather than implementation details.
* Prefer architectural understanding over code listing.
* Summarize recurring patterns instead of documenting every file.
* Include Mermaid diagrams when they help explain workflows, boundaries, or interactions.
