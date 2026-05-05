## Agent Workspace

This project uses an agent-first workspace:

agents/

### Usage

If any of the following Markdown files are not already in context, you MUST read them first:

- agents/README.md
- agents/PROTOCOL.md
- agents/CONTEXT.md

Use skills for issue operations.

### Principle

- agents/ is source of truth
- issues define work
- protocol defines behavior
- context provides knowledge

### Workspace Maintenance Rules

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
