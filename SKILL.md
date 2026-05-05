# setup-project-workspace/SKILL.md

---
name: setup-project-workspace
description: Initialize a long-term agent-first workspace and ensure issue-tracker skill exists.
---

# Setup Project Workspace

Initialize a project-level `agents/` workspace and ensure the `issue-tracker` skill is available.

## Goal

Create in the current project root:

```text
agents/
  README.md
  PROTOCOL.md
  CONTEXT.md
  issues/
```

Also ensure:

```text
~/.claude/skills/issue-tracker/
  SKILL.md
  scripts/
    issue_status.py
    create_issue.py
    set_issue_status.py
    reorder_issues.py
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

### 1. Ensure project workspace

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

### 2. Create or update project-local CLAUDE.md

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

### 3. Ensure issue-tracker skill

Create missing directories:

```text
~/.claude/skills/issue-tracker/
~/.claude/skills/issue-tracker/scripts/
```

Copy template files into target folders using the current operating system's native copy operation:

```text
issue-tracker/SKILL.md
  -> ~/.claude/skills/issue-tracker/SKILL.md

issue-tracker/scripts/issue_status.py
  -> ~/.claude/skills/issue-tracker/scripts/issue_status.py

issue-tracker/scripts/create_issue.py
  -> ~/.claude/skills/issue-tracker/scripts/create_issue.py

issue-tracker/scripts/set_issue_status.py
  -> ~/.claude/skills/issue-tracker/scripts/set_issue_status.py

issue-tracker/scripts/reorder_issues.py
  -> ~/.claude/skills/issue-tracker/scripts/reorder_issues.py
```

Rules:

- Do not overwrite existing target files.
- Do not inspect template contents before copying.
- Preserve all copied files exactly.

---

## Completion

```text
Initialized agent workspace and ensured issue-tracker skill. Please restart Claude Code to load the new skill.
```
