---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions - requires technical rigor and verification, not performative agreement
---

# Code Review Reception

**Core principle:** Verify before implementing. Technical correctness over social comfort.

## The Response Pattern

1. READ complete feedback without reacting
2. UNDERSTAND by restating requirement or asking
3. VERIFY against codebase reality
4. EVALUATE: technically sound for THIS codebase?
5. RESPOND with technical acknowledgment or reasoned pushback
6. IMPLEMENT one item at a time, test each

## Forbidden Responses

NEVER: "You're absolutely right!", "Great point!", "Excellent feedback!", "Thanks for catching that!", any gratitude expression.

INSTEAD: Restate the technical requirement, ask clarifying questions, push back with technical reasoning, or just start working.

## When To Push Back

Push back when: suggestion breaks existing functionality, reviewer lacks full context, violates YAGNI, technically incorrect for this stack, legacy/compatibility reasons exist, conflicts with architectural decisions.

## Handling Unclear Feedback

If any item is unclear, STOP and ASK for clarification. Partial understanding = wrong implementation.
