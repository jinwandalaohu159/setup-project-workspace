# Agent Protocol

This file defines project-level agent rules.

Detailed issue operations are handled by the `issue-tracker` skill.

---

## Workspace Structure

```text
agents/
  README.md
  PROTOCOL.md
  CONTEXT.md
  issues/
```

---

## Core Principle

- `agents/` is the project coordination layer.
- `PROTOCOL.md` defines project-level rules.
- `CONTEXT.md` stores long-term project knowledge.
- `issues/` stores task data.
- Issue operations must use the `issue-tracker` skill.

---

## Required Reading

If required context is not available in the current conversation, read:

```text
agents/README.md
agents/PROTOCOL.md
agents/CONTEXT.md
```

Do not read all issue files by default.

Use the `issue-tracker` skill to locate the relevant issue.

---

## Issue Rules

Use the `issue-tracker` skill for all issue operations, including:

- creating issues
- checking issue state
- starting work
- completing work
- returning failed work to ready

Rules:

- Only one issue may be `doing` at a time.
- Execution order is FIFO.
- One issue must describe one problem.
- New independent problems must be created as new issues.
- Do not manually scan or modify issue files unless the `issue-tracker` skill is unavailable.
- An issue may be changed to `done` only after its work is completed and its current status is `doing`.

---

## Small Steps Principle

- Always make the smallest meaningful change at a time.
- Prefer many small, clear steps over one large change.
- Each step must be understandable, verifiable, and easy to revert.
- Advance strictly in small steps when coding, testing, or refactoring — even with vibe coding.
- One issue should naturally be completed through multiple small steps instead of a single big modification.

---

## Completion Rules

Before any issue, feature, or module is marked as complete, the agent must perform TDD.

Use the `tdd` skill if available; otherwise, write and run the tests directly.

Only after tests pass may the agent proceed to code-quality improvement.

Use the `improve-codebase` skill if available.

Refactor the implementation toward deep modules: simple public interfaces, hidden internal complexity, and clear boundaries.

Do not mark the issue as `done` until tests pass and code-quality improvement is complete.

---

## Context Rules

Agents may read:

```text
agents/CONTEXT.md
```

Agents must not modify `agents/CONTEXT.md` unless the user explicitly asks.

Project-specific long-term knowledge should be stored in `CONTEXT.md`.

---

## Git Rules

Git records what actually changed.

Do not commit or push unless the user explicitly asks.

When committing issue-related work, include the issue filename or id in the commit message when possible.

---

## Fallback

If the `issue-tracker` skill or required scripts are unavailable:

1. Stop.
2. Report what is missing.
3. Do not continue issue execution unless the user explicitly asks.
