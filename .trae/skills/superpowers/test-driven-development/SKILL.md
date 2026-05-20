---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## The Iron Law

NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. Write code before the test? Delete it. Start over.

## Red-Green-Refactor

**RED** - Write one minimal failing test showing what should happen. Clear name, tests real behavior, one thing.

**Verify RED** - Watch it fail. Confirm failure is expected, fails because feature missing (not typos). Test passes? Fix test. Test errors? Fix error.

**GREEN** - Write simplest code to pass the test. Don't add features, refactor other code, or "improve" beyond the test.

**Verify GREEN** - Watch it pass. Confirm test passes, other tests still pass, output pristine.

**REFACTOR** - After green only: remove duplication, improve names, extract helpers. Keep tests green. Don't add behavior.

## Verification Checklist

Before marking work complete:
- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)

Can't check all boxes? You skipped TDD. Start over.
