import argparse
import re
import sys
import yaml
from pathlib import Path

ISSUES_DIR = Path("agents/issues")

VALID_PRIORITY = {"low", "medium", "high"}
VALID_AUTHOR = {"user", "agent"}
VALID_SOURCE = {"local", "github"}


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


def remote_id_exists(remote_id: int) -> bool:
    if not ISSUES_DIR.exists():
        return False
    for path in ISSUES_DIR.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if match:
            data = yaml.safe_load(match.group(1)) or {}
            if data.get("remote_id") == remote_id:
                return True
    return False


def create_issue(
    title: str,
    description: str,
    expected: str,
    priority: str,
    author: str,
    source: str,
    remote_id: int | None,
):
    if priority not in VALID_PRIORITY:
        raise ValueError(f"Invalid priority: {priority}")

    if author not in VALID_AUTHOR:
        raise ValueError(f"Invalid author: {author}")

    if source not in VALID_SOURCE:
        raise ValueError(f"Invalid source: {source}")

    if source == "github" and remote_id is None:
        raise ValueError("--remote-id is required when --source is github")

    if source == "local" and remote_id is not None:
        raise ValueError("--remote-id should not be set when --source is local")

    if remote_id is not None and remote_id_exists(remote_id):
        print(f"SKIP: remote_id {remote_id} already exists locally")
        return

    status = "ready" if author == "user" else "draft"

    issue_id = next_issue_id()
    issue_id_str = f"{issue_id:04d}"
    filename = f"{issue_id_str}-{slugify(title)}.md"
    path = ISSUES_DIR / filename

    remote_id_line = f"remote_id: {remote_id}" if remote_id is not None else "remote_id:"

    content = f"""---
id: {issue_id_str}
title: {title}
status: {status}
priority: {priority}
author: {author}
source: {source}
{remote_id_line}
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
    parser.add_argument(
        "--source",
        default="local",
        choices=sorted(VALID_SOURCE),
    )
    parser.add_argument(
        "--remote-id",
        type=int,
        default=None,
    )

    args = parser.parse_args()

    create_issue(
        title=args.title,
        description=args.description,
        expected=args.expected,
        priority=args.priority,
        author=args.author,
        source=args.source,
        remote_id=args.remote_id,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
