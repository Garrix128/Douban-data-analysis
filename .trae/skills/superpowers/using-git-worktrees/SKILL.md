---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace. Prefer native tools. Fall back to git worktree only when no native tool available.

**Core principle:** Detect existing isolation first. Then use native tools. Then fall back to git.

### Step 0: Detect Existing Isolation

If already in a linked worktree (GIT_DIR != GIT_COMMON, and not a submodule), skip creation. Report: "Already in isolated workspace on branch `<name>`."

### Step 1: Create Isolated Workspace

Try native worktree tools first. Only use `git worktree add` as fallback.

### Step 3: Project Setup

Auto-detect: npm install / pip install / cargo build / go mod download.

### Step 4: Verify Clean Baseline

Run tests. If they fail, report and ask whether to proceed.

## Red Flags

Never: create worktree when already isolated, use git fallback when native tool available, skip ignore verification, proceed with failing tests without asking.
