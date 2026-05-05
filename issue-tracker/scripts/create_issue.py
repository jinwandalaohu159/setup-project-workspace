import argparse
import re
import sys
from pathlib import Path

ISSUES_DIR = Path("agents/issues")

VALID_PRIORITY = {"low", "medium", "high"}
VALID_AUTHOR = {"user", "agent"}


def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "issue"


def next_issue_id() -> int:
    ISSUES_DIR.mkdir(parents=True, exist_ok=True)

    ids = []

    for path in ISSUES_DIR.glob("*.md"):
        match = re.match(r"^(\d+)-", path.name)
        if match:
            ids.append(int(match.group(1)))

    return max(ids, default=0) + 1


def create_issue(
    title: str,
    description: str,
    expected: str,
    priority: str,
    author: str,
):
    if priority not in VALID_PRIORITY:
        raise ValueError(f"Invalid priority: {priority}")

    if author not in VALID_AUTHOR:
        raise ValueError(f"Invalid author: {author}")

    status = "ready" if author == "user" else "draft"

    issue_id = next_issue_id()
    issue_id_str = f"{issue_id:04d}"
    filename = f"{issue_id_str}-{slugify(title)}.md"
    path = ISSUES_DIR / filename

    content = f"""---
id: {issue_id_str}
title: {title}
status: {status}
priority: {priority}
author: {author}
---

## Description

{description}

## Expected

{expected}

## Agent Notes

"""

    path.write_text(content, encoding="utf-8")
    print(str(path))


def main():
    parser = argparse.ArgumentParser(
        description="Create a new agent issue."
    )

    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument(
        "--priority",
        default="medium",
        choices=sorted(VALID_PRIORITY),
    )
    parser.add_argument(
        "--author",
        default="agent",
        choices=sorted(VALID_AUTHOR),
    )

    args = parser.parse_args()

    create_issue(
        title=args.title,
        description=args.description,
        expected=args.expected,
        priority=args.priority,
        author=args.author,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
