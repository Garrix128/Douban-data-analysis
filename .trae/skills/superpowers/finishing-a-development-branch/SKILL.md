---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work
---

# Finishing a Development Branch

## The Process

### Step 1: Verify Tests
Run tests. If failing, stop and fix. If passing, continue.

### Step 2: Detect Environment
Determine workspace state: normal repo, named-branch worktree, or detached HEAD.

### Step 3: Present Options

**Standard (normal repo/named branch):**
1. Merge back to main locally
2. Push and create a Pull Request
3. Keep the branch as-is
4. Discard this work

**Detached HEAD:** Options 1 excluded.

### Step 4: Execute Choice

**Option 1 (Merge):** Checkout main, pull, merge feature branch, verify tests, remove worktree, delete branch.
**Option 2 (PR):** Push branch, create PR with gh CLI. Keep worktree for iteration.
**Option 3 (Keep):** Report preserved. Don't cleanup.
**Option 4 (Discard):** Require typed "discard" confirmation. Remove worktree, force-delete branch.

## Red Flags
Never: proceed with failing tests, merge without verifying, delete without confirmation, force-push without request, clean up worktrees you didn't create.
