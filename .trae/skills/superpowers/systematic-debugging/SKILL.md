---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## The Iron Law

NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST. If you haven't completed Phase 1, you cannot propose fixes.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## When to Use

Use for ANY technical issue: test failures, bugs in production, unexpected behavior, performance problems, build failures, integration issues. Use ESPECIALLY when under time pressure, "just one quick fix" seems obvious, you've already tried multiple fixes, or you don't fully understand the issue.

## Phase 1: Root Cause Investigation

1. **Reproduce:** Run the failing test/command. Observe the actual failure.
2. **Isolate:** Narrow to minimal reproduction. Find the exact line/condition.
3. **Understand:** Why does this happen? What's the underlying cause?
4. **Confirm:** Can you reliably reproduce? Can you prevent it?

Only after all 4 steps: propose the fix.

## Phase 2: Fix

1. Write failing test that reproduces the bug
2. Verify test fails with the bug
3. Implement minimal fix
4. Verify test passes
5. Run full test suite to check for regressions

## Red Flags - STOP

- About to fix without reproduction
- "I think I know what's wrong" without evidence
- Multiple attempted fixes without understanding
- Fixes applied without understanding why they work
