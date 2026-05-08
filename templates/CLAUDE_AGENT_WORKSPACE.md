## Agent Workspace

This project uses an agent-first workspace:

agents/

### Usage

The following Markdown files are the first principle of development; if not already in context, you ALWAYS MUST read them first:

- agents/README.md
- agents/PROTOCOL.md
- agents/CONTEXT.md
- agents/TRACKING.md

Use skills for issue operations.

### Principle

- agents/ is source of truth
- issues define work
- protocol defines behavior
- context provides knowledge

### Workspace Maintenance Rules

Agents must stay within the current project workspace by default. Any operation outside this workspace requires explicit user approval before proceeding.

These files are long-term maintained by agents:

```text
CLAUDE.md
agents/README.md
agents/PROTOCOL.md
agents/CONTEXT.md
```

Agents may only append under `## Agent Notes`.

If missing, add `## Agent Notes` at the end first.

Do not modify any existing default content outside `## Agent Notes`.

Append format:

```md
### Title

- Problem / Reason:
- Content:

```
