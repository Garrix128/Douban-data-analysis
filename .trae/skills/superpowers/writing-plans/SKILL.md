---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans with exact file paths, complete code in every step, and bite-sized tasks (2-5 min each). DRY. YAGNI. TDD. Frequent commits.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## Bite-Sized Task Granularity
Each step is one action (2-5 minutes): write the failing test, run it to make sure it fails, implement minimal code, run tests and make sure they pass, commit.

## No Placeholders
Every step must contain the actual content. NEVER write: "TBD", "TODO", "add appropriate error handling", "write tests for the above", "Similar to Task N". Steps that describe what to do without showing how (code blocks required for code steps).

## Plan Document Header
Every plan MUST start with header containing: Goal, Architecture, Tech Stack. Tasks use checkbox syntax (`- [ ]`).
