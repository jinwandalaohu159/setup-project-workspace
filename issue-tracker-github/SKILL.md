---
name: issue-tracker-github
description: 1. Automatically triggered after an issue is marked done when TRACKING.md has tracker: github — commit, push, close. 2. When user requests, pull GitHub issues to local and close them after completion.
---

# Issue Tracker GitHub

This skill manages the GitHub side of issue tracking. It depends on `issue-tracker-local` for all local issue operations.

Prerequisite: `agents/TRACKING.md` must exist with `tracker: github`.

---

## Trigger

Automatically triggered when an issue is marked `done` and `agents/TRACKING.md` has `tracker: github`.

When triggered, execute: Login Check → Commit → Push → Close GitHub Issue (if applicable).

---

## Login Check

Before any GitHub operation, verify authentication:

```bash
gh auth status
```

If not authenticated, stop and ask the user to run `gh auth login`.

---

## Pull GitHub Issues

When the user asks to check GitHub issues:

```bash
gh issue list --repo <remote> --state open --json number,title,body
```

For each GitHub issue not yet pulled locally, create a local issue:

```bash
python ${CLAUDE_SKILL_DIR}/../issue-tracker-local/scripts/create_issue.py \
  --title "<title>" \
  --description "<body>" \
  --expected "To be determined from GitHub issue #<number>" \
  --author user \
  --source github \
  --remote-id <number>
```

If the remote_id already exists locally, `create_issue.py` will skip it.

---

## Commit

After an issue is marked `done` (TDD + improve-codebase passed), commit with the issue ID:

- Local issue: `[<local_id>] commit message`
- GitHub issue: `[<local_id>] commit message (#<github_issue_number>)`

Example:

```bash
git add <files>
git commit -m "[<local_id>] fix login bug"
```

```bash
git add <files>
git commit -m "[<local_id>] fix login bug (#<github_issue_number>)"
```

---

## Push

After committing, push immediately:

```bash
git push
```

---

## Close GitHub Issue

When `set_issue_status.py` outputs `REMOTE_ID: <number>`, close the original GitHub issue:

```bash
gh issue close <number> --repo <remote>
```

Get `<remote>` from `agents/TRACKING.md` `remote` field.
