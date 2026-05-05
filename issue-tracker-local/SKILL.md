---
name: issue-tracker-local
description: Manage local project issues under agents/issues, including issue creation, status inspection, and safe status updates.
---

# Issue Tracker Local

Use this skill for all issue operations in projects that contain an `agents/` workspace.

Issue source:

```text
agents/issues/
```

Helper scripts:

```text
${CLAUDE_SKILL_DIR}/scripts/issue_status.py
${CLAUDE_SKILL_DIR}/scripts/create_issue.py
${CLAUDE_SKILL_DIR}/scripts/set_issue_status.py
${CLAUDE_SKILL_DIR}/scripts/reorder_issues.py
```

Do not manually scan or modify issue files unless the required script is missing or broken.

---

## Issue Format

Each issue is a Markdown file under:

```text
agents/issues/
```

File name format:

```text
0001-short-title.md
```

Issue content format:

```md
---
id: 0001
title: short issue title
status: ready
priority: medium
author: user
source: local
remote_id:
---

## Description

Describe the problem or requested change.

## Expected

Describe the expected result after the issue is resolved.

## Agent Notes

Agents may append notes here while working on this issue.
```

---

## Status

Allowed status values:

```text
draft
ready
doing
done
```

Meaning:

- `draft`: proposed issue, not ready for execution.
- `ready`: confirmed issue, ready for execution.
- `doing`: currently being handled.
- `done`: completed.

Global constraints:

- At any time, only one issue may have `status: doing`.
- An issue may be changed to `done` only after its work is completed and its current status is `doing`.

Allowed flow:

```text
draft -> ready
ready -> draft
ready -> doing
doing -> draft
doing -> done
doing -> ready
```

---

## Author

Allowed author values:

```text
user
agent
```

Rules:

- Issues created from user requests use `author: user`.
- Issues created by agents use `author: agent`.
- User-created issues start as `status: ready`.
- Agent-created issues start as `status: draft`.
- Only issues with `author: user` and `status: ready` are executable.
- Use `author: user` only when the user clearly asks for it or gives permission. Otherwise use `author: agent`.

---

## Check Issue State

Use:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/issue_status.py
```

Possible outputs:

```text
DOING: 0001-example.md [local]
DOING: 0003-example.md [github #42]
NEXT: 0002-example.md [local]
NO_WORK
ERROR: ...
```

Meaning:

- `DOING`: continue this issue only.
- `NEXT`: this is the next executable issue.
- `NO_WORK`: no executable issue exists.
- `ERROR`: protocol violation or invalid issue state.

Rules:

- Always run this before modifying project code.
- If `DOING`, continue that issue.
- If `NEXT`, start that issue.
- If `NO_WORK`, do not modify project code.
- If `ERROR`, stop and report the problem.

---

## Create Issue

Use:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/create_issue.py \
  --title "fix login issue" \
  --description "用户反馈登录有问题" \
  --expected "登录流程应能正常完成" \
  --priority medium \
  --author user
```

Arguments:

```text
--title        short issue title
--description  problem or requested change
--expected     expected result after completion
--priority     low | medium | high
--author       user | agent
--source       local | github
--remote-id    GitHub issue number (required when source is github)
```

Rules:

- AI generates `title`, `description`, and `expected`.
- If user clearly provides expected result, use the user's meaning.
- If user only describes a problem, generate the minimal normal expected behavior.
- Do not invent extra requirements.
- `author: user` creates `status: ready`.
- `author: agent` creates `status: draft`.
- `source: local` is the default for issues created locally.
- `source: github` is used when pulling a GitHub issue to local.
- When `source: github`, `--remote-id` is required and the script checks for duplicates.
- If an issue with the same `remote_id` already exists, creation is skipped.

---

## Start Work

Before editing project code, run:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/issue_status.py
```

If output is:

```text
NEXT: 0001-example.md
```

start that issue with:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/set_issue_status.py 0001-example.md doing
```

Rules:

- Only the issue returned by `NEXT` may be changed to `doing`.
- There must be only one `doing` issue at any time.
- If another issue is already `doing`, the script exits with an error.
- Do not edit project code before the issue is changed to `doing`.

---

## Complete Work

After implementation and verification, use:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/set_issue_status.py 0001-example.md done
```

Rules:

- This only works on an issue whose current status is `doing`.
- It changes `doing -> done`.
- If the issue is not `doing`, the script exits with an error.
- When `source: github`, the script prints `REMOTE_ID: <number>` on a second line for the github skill to use.

---

## Failure Handling

If the issue cannot be completed, append the reason under:

```md
## Agent Notes
```

Then run:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/set_issue_status.py 0001-example.md ready
```

Rules:

- This only works on an issue whose current status is `doing`.
- It changes `doing -> ready`.
- Do not mark failed work as `done`.

---

## Issue Selection

Execution order is FIFO.

The next executable issue is the lowest-numbered issue with:

```yaml
status: ready
author: user
```

`priority` is only an attention signal.

It does not change execution order.

---

## Reorder Issues

Issue numbering gaps are a sequencing problem, not a missing-work problem.

Agents normally should not delete later issues. Therefore, if numbering has gaps, assume the gap was intentionally created by the user unless there is clear evidence otherwise.

If issue numbering has gaps, for example `0001`, `0002`, `0005`, renumber all issues sequentially:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/reorder_issues.py
```

Rules:

- Do not recreate a missing-number issue just to fill the gap.
- Do not assume the missing number means issue creation failed.
- Do not try to repair the deleted issue unless the user explicitly asks for it.
- After reordering, run `issue_status.py` again and follow its result.

---

## New Problems

One issue must describe one problem.

If a new independent problem is discovered:

1. Create a new issue using `create_issue.py`.
2. Use `author: agent`.
3. The new issue starts as `status: draft`.
4. Do not hide the new problem inside the current issue notes.
