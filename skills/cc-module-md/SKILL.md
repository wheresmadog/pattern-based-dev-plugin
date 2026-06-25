---
name: cc-module-md
description: Create a CLAUDE.md for this module only.
---

# Claude MD

When invoked, create a `CLAUDE.md` for the current module.

Treat this module as a subsystem within a larger application. Focus on the module's responsibilities, features, boundaries, and interactions with the rest of the system.

Do NOT produce a file-by-file inventory unless a file is exceptionally important to understanding the module.

## Structure

Write the document using the following sections:

### Module Purpose

* Why this module exists
* Problems it solves
* Responsibilities it owns
* Responsibilities intentionally owned by other modules

### Feature Overview

For each major feature provided by this module:

* Purpose
* Main workflows
* Key entry points
* Important business rules
* Dependencies on other modules

### Module Boundaries

* What belongs inside this module
* What should not be implemented here
* Upstream dependencies
* Downstream consumers
* Public interfaces exposed to other modules

### Internal Architecture

* Major components and their responsibilities
* Data flow within the module
* Lifecycle of a typical request/job/event
* Important abstractions and patterns

### Integration Points

* APIs consumed
* Events published/subscribed
* Database/storage interactions
* External services used
* Cross-module communication

### Domain Model

* Core concepts and entities
* Relationships between concepts
* Important terminology specific to this module

### Change Guide

When modifying this module:

* Safe areas to extend
* Common implementation patterns
* Areas with hidden complexity
* Frequently broken assumptions
* Important invariants that must be preserved

### Directory Guide

Explain the purpose of major directories and packages in terms of functionality, not individual files.

### Mental Model

Provide a concise explanation of how an engineer should think about this module and its role within the larger system.

## Guidelines

* Optimize for onboarding engineers who need to work on this module.
* Explain responsibilities and feature ownership rather than implementation details.
* Prefer architectural understanding over code listing.
* Summarize recurring patterns instead of documenting every file.
* Include Mermaid diagrams when they help explain workflows, boundaries, or interactions.
