---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

**Continuous execution:** Do not pause between tasks. Execute all tasks without stopping. Only stop for: BLOCKED status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete.

## Model Selection

Use the least powerful model that can handle each role. Mechanical implementation tasks (1-2 files, clear specs) use a fast/cheap model. Integration tasks use standard model. Architecture/design/review tasks use most capable model.

## Handling Implementer Status

**DONE:** Proceed to spec compliance review.
**DONE_WITH_CONCERNS:** Read concerns, address if about correctness/scope, note observations and proceed.
**NEEDS_CONTEXT:** Provide missing context and re-dispatch.
**BLOCKED:** Assess: context problem → provide context; needs more reasoning → more capable model; too large → break into smaller pieces; plan wrong → escalate.

## Red Flags
Never: start on main/master, skip reviews, proceed with unfixed issues, dispatch parallel implementation subagents, skip re-review loops, accept "close enough" on spec compliance.
