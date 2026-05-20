---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Agents

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

## When to Use

Use when: 3+ test files failing with different root causes, multiple subsystems broken independently, each problem can be understood without context from others, no shared state between investigations.

## Agent Construction

Each agent gets precisely crafted context — what they need to succeed, nothing more. They should never inherit your session's context or history. You construct exactly what they need. This preserves your own context for coordination work.

## Agent Status Handling

Handle agent reports:
- **DONE:** Proceed to next
- **DONE_WITH_CONCERNS:** Read concerns, address if critical
- **NEEDS_CONTEXT:** Provide missing context, re-dispatch
- **BLOCKED:** Assess: context problem → more context; too complex → more capable model; too large → break down; plan wrong → escalate
