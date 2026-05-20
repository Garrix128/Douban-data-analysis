---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Writing Skills

## Overview

Writing skills IS Test-Driven Development applied to process documentation. You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand superpowers:test-driven-development before using this skill.

## The Process

### RED: Write Pressure Tests First

Before writing any skill content, create scenarios that test whether agents WITHOUT the skill do the wrong thing. Each test: opens a fresh context, asks the agent to do something, and checks the response for the problematic pattern.

### GREEN: Write Minimal Skill

Write the simplest skill that makes the tests pass. Don't over-document. Don't add edge cases your tests don't cover.

### REFACTOR: Tighten

After tests pass: close loopholes in wording, add examples from failed tests, remove redundant sections, sharpen HARD-GATE boundaries.

## Skill Structure

Every skill needs YAML frontmatter with name and description. The description determines when agents invoke the skill — be specific about triggers.

## Testing Methodology

Use subagents to test: dispatch an agent WITHOUT the skill, observe baseline failure, deploy the skill, re-dispatch, confirm compliance.

## Red Flags

Never write skill content before tests, rationalize "simple enough to skip testing", fix tests to match weak skills instead of strengthening skills.
