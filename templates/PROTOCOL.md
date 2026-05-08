# Agent Protocol

This file defines project-level agent rules.

Detailed issue operations are handled by the `issue-tracker-local` skill.

---

## Workspace Structure

```text
agents/
  README.md
  PROTOCOL.md
  CONTEXT.md
  TRACKING.md
  issues/
```

---

## Core Principle

- `agents/` is the project coordination layer.
- `PROTOCOL.md` defines project-level rules.
- `CONTEXT.md` stores long-term project knowledge.
- `issues/` stores task data.
- Issue operations must use the `issue-tracker-local` skill.

---

## Required Reading

If required context is not available in the current conversation, read:

```text
agents/README.md
agents/PROTOCOL.md
agents/CONTEXT.md
```

Do not read all issue files by default.

Use the `issue-tracker-local` skill to locate the relevant issue.

---

## Issue Rules

Use the `issue-tracker-local` skill for all issue operations, including:

- creating issues
- checking issue state
- starting work
- completing work
- returning failed work to ready
- check the tracker type in `agents/TRACKING.md` to decide whether to commit and push, check details in ## Git Rules

Rules:

- Every change starts with an issue. When a user describes a problem or requests a change, create an issue first — this is the starting point of all work.
- To find the next issue to work on, use `issue_status.py` — it handles ordering, status filtering, and author validation.
- Only one issue may be `doing` at a time.
- Execution order is FIFO.
- One issue must describe one problem.
- New independent problems must be created as new issues.
- Do not manually scan or modify issue files unless the `issue-tracker-local` skill is unavailable.
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

After marking an issue as `done`:

1. Read `agents/TRACKING.md`.
2. If `tracker: github`, invoke the `issue-tracker-github` skill to commit and push.
3. If `tracker: local` or missing, do not commit or push unless the user explicitly asks.

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

When `agents/TRACKING.md` has `tracker: local` or is missing, do not commit or push unless the user explicitly asks.

When `agents/TRACKING.md` has `tracker: github`, MUST commit and push automatically after an issue is marked `done`. Use the `issue-tracker-github` skill. Each issue must be committed individually before starting the next — do not batch multiple issues into a single commit.

When committing issue-related work, include the issue id in the commit message:

- Local issue: `[<local_id>] commit message`
- GitHub issue: `[<local_id>] commit message (#<github_issue_number>)`

---

## Fallback

If the `issue-tracker-local` skill or required scripts are unavailable:

1. Stop.
2. Report what is missing.
3. Do not continue issue execution unless the user explicitly asks.
