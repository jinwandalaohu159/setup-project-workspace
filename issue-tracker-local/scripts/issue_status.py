import re
import sys
import yaml
from pathlib import Path

ISSUES_DIR = Path("agents/issues")
VALID_STATUS = {"draft", "ready", "doing", "done"}


def _source_tag(issue: dict) -> str:
    source = issue.get("source", "local")
    remote_id = issue.get("remote_id")
    if source == "github" and remote_id:
        return f"[github #{remote_id}]"
    return "[local]"


def parse_frontmatter(path: Path):
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)

    if not match:
        return None

    data = yaml.safe_load(match.group(1)) or {}

    data["_file"] = path.name
    data["_path"] = str(path)
    return data


def main():
    if not ISSUES_DIR.exists():
        print("NO_ISSUES_DIR")
        return 0

    issues = []

    for path in sorted(ISSUES_DIR.glob("*.md")):
        issue = parse_frontmatter(path)
        if issue:
            issues.append(issue)

    invalid = [
        i for i in issues
        if i.get("status") not in VALID_STATUS
    ]

    if invalid:
        print("ERROR: Invalid issue status detected")
        for issue in invalid:
            print(f"- {issue['_file']}: {issue.get('status')}")
        return 1

    doing = [i for i in issues if i.get("status") == "doing"]
    ready = [
        i for i in issues
        if i.get("status") == "ready" and i.get("author") == "user"
    ]

    if len(doing) > 1:
        print("ERROR: Multiple doing issues detected")
        for issue in doing:
            print(f"- {issue['_file']}")
        return 1

    if doing:
        issue = doing[0]
        source_tag = _source_tag(issue)
        print(f"DOING: {issue['_file']} {source_tag}")
        return 0

    if ready:
        issue = sorted(ready, key=lambda x: int(str(x.get("id", 0))))[0]
        source_tag = _source_tag(issue)
        print(f"NEXT: {issue['_file']} {source_tag}")
        return 0

    print("NO_WORK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
