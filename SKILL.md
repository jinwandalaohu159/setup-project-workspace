# setup-project-workspace/SKILL.md

---
name: setup-project-workspace
description: Initialize a long-term agent-first workspace and ensure issue-tracker skills exist.
---

# Setup Project Workspace

Initialize a project-level `agents/` workspace and ensure issue-tracker skills are available.

## Goal

Create in the current project root:

```text
agents/
  README.md
  PROTOCOL.md
  CONTEXT.md
  TRACKING.md
  issues/
```

Also ensure:

```text
~/.claude/skills/issue-tracker-local/
  SKILL.md
  scripts/
    issue_status.py
    create_issue.py
    set_issue_status.py
    reorder_issues.py
```

And optionally (when tracker is github):

```text
~/.claude/skills/issue-tracker-github/
  SKILL.md
```

exists.

---

## Rules

- Do not modify business code
- Do not create issues
- Do not execute agent workflow
- Do not commit or push
- Preserve existing files
- Only create missing files
- Treat the current working directory as the project root; never read, copy, or modify parent-level `CLAUDE.md`
- Treat all templates as opaque files: copy them verbatim; do not read, interpret, rewrite, or regenerate their contents unless copying fails and debugging is required.

---

## Steps

### 1. Ask tracking mode

Use `AskUserQuestion` to ask the user:

> How do you want to track issues?

Options:

- `local` — Local file-based issue tracking only
- `github` — Local issue tracking plus GitHub commit/push version management

If the user chooses `github`:

1. Check if `.git` exists in the project root. If not, run `git init`.
2. Check if a git remote exists (`git remote -v`). If not, run `gh repo create` and add as origin.

---

### 2. Ensure project workspace

Create missing directories:

```text
agents/
agents/issues/
```

Create missing files by copying templates verbatim:

```text
templates/README.md   -> agents/README.md
templates/PROTOCOL.md -> agents/PROTOCOL.md
templates/CONTEXT.md  -> agents/CONTEXT.md
```

Rules:

- Do not overwrite existing target files.
- Do not inspect template contents before copying.
- Use file copy operations only.

---

### 3. Generate TRACKING.md

Create `agents/TRACKING.md` based on the user's tracking mode choice.

If `agents/TRACKING.md` already exists, do not overwrite.

Content template:

```markdown
---
tracker: <user's choice: local|github>
remote: <owner/repo if github, empty if local>
---

This file configures issue tracking mode.

- `tracker`: `local` | `github`
- `remote`: GitHub repo (e.g. `owner/repo`), required when tracker is `github`
```

Fill `remote` by extracting from `git remote -v` (origin URL) when tracker is github.

---

### 4. Create or update project-local CLAUDE.md

Target only:

```text
./CLAUDE.md
```

If missing, create it by copying this template verbatim:

```text
templates/CLAUDE_AGENT_WORKSPACE.md -> ./CLAUDE.md
```

If present, append this template verbatim only when the same agent workspace section is not already present:

```text
templates/CLAUDE_AGENT_WORKSPACE.md -> ./CLAUDE.md
```

Rules:

- Do not rewrite existing `CLAUDE.md`.
- Do not read or modify parent-level `CLAUDE.md`.
- Only operate on `./CLAUDE.md` in the current project root.
- Only inspect `./CLAUDE.md` enough to determine whether the agent workspace section already exists.

---

### 5. Ensure issue-tracker-local skill

Create missing directories:

```text
~/.claude/skills/issue-tracker-local/
~/.claude/skills/issue-tracker-local/scripts/
```

Copy template files into target folders using the current operating system's native copy operation:

```text
issue-tracker-local/SKILL.md
  -> ~/.claude/skills/issue-tracker-local/SKILL.md

issue-tracker-local/scripts/issue_status.py
  -> ~/.claude/skills/issue-tracker-local/scripts/issue_status.py

issue-tracker-local/scripts/create_issue.py
  -> ~/.claude/skills/issue-tracker-local/scripts/create_issue.py

issue-tracker-local/scripts/set_issue_status.py
  -> ~/.claude/skills/issue-tracker-local/scripts/set_issue_status.py

issue-tracker-local/scripts/reorder_issues.py
  -> ~/.claude/skills/issue-tracker-local/scripts/reorder_issues.py
```

Rules:

- Do not overwrite existing target files.
- Do not inspect template contents before copying.
- Preserve all copied files exactly.

---

### 6. Ensure issue-tracker-github skill (if needed)

Only when the user chose `github`:

Create missing directory:

```text
~/.claude/skills/issue-tracker-github/
```

Copy:

```text
issue-tracker-github/SKILL.md
  -> ~/.claude/skills/issue-tracker-github/SKILL.md
```

Rules:

- Do not overwrite existing target files.
- Do not inspect template contents before copying.
- Preserve all copied files exactly.

---

## Completion

```text
Initialized agent workspace and ensured issue-tracker skills. Please restart Claude Code to load the new skills.
```
