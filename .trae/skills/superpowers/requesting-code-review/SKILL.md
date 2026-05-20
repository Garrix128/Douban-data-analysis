---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:** After each task in subagent-driven development, after completing major feature, before merge to main.

**Optional:** When stuck (fresh perspective), before refactoring, after fixing complex bug.

## How to Request

1. Get git SHAs: `BASE_SHA=$(git rev-parse HEAD~1)` and `HEAD_SHA=$(git rev-parse HEAD)`
2. Dispatch code reviewer subagent with DESCRIPTION, PLAN_OR_REQUIREMENTS, BASE_SHA, HEAD_SHA
3. Act on feedback: fix Critical immediately, fix Important before proceeding, note Minor for later

## Red Flags

Never: skip review because "it's simple", ignore Critical issues, proceed with unfixed Important issues, argue with valid technical feedback. If reviewer is wrong, push back with technical reasoning.
