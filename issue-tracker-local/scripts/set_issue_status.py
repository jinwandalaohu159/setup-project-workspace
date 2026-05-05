import argparse
import re
import sys
import yaml
from pathlib import Path

ISSUES_DIR = Path("agents/issues")

ALLOWED_TRANSITIONS = {
    "draft": {"ready"},
    "ready": {"doing", "draft"},
    "doing": {"ready", "done", "draft"},
}


def find_issue(filename: str) -> Path:
    path = ISSUES_DIR / filename
    if path.exists() and path.is_file():
        return path
    raise FileNotFoundError(f"Issue not found: {filename}")


def parse_frontmatter(content: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("Missing YAML frontmatter")
    return yaml.safe_load(match.group(1)) or {}


def parse_status(content: str) -> str | None:
    return parse_frontmatter(content).get("status")


def has_other_doing(current_path: Path) -> bool:
    for path in ISSUES_DIR.glob("*.md"):
        if path == current_path:
            continue
        try:
            status = parse_status(path.read_text(encoding="utf-8"))
            if status == "doing":
                return True
        except Exception:
            continue
    return False


def set_issue_status(filename: str, target_status: str):
    path = find_issue(filename)
    content = path.read_text(encoding="utf-8")
    current_status = parse_status(content)

    if current_status is None:
        raise ValueError("Missing status in frontmatter")

    allowed_targets = ALLOWED_TRANSITIONS.get(current_status)
    if not allowed_targets or target_status not in allowed_targets:
        raise ValueError(
            f"Invalid transition: {current_status} -> {target_status}"
        )

    if current_status == "ready" and target_status == "doing":
        if has_other_doing(path):
            raise ValueError("Another issue is already doing")

    new_content = re.sub(
        r"^status:.*$",
        f"status: {target_status}",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    path.write_text(new_content, encoding="utf-8")
    print(f"Updated: {path} [{current_status} -> {target_status}]")

    if target_status == "done":
        frontmatter = parse_frontmatter(new_content)
        if frontmatter.get("source") == "github" and frontmatter.get("remote_id"):
            print(f"REMOTE_ID: {frontmatter['remote_id']}")

        tracking_path = Path("agents/TRACKING.md")
        if tracking_path.exists():
            tracking_content = tracking_path.read_text(encoding="utf-8")
            tracking_fm = parse_frontmatter(tracking_content)
            tracker = tracking_fm.get("tracker", "local")
        else:
            tracker = "local"

        if tracker == "github":
            print("GITHUB_TRACKER: Issue finished. Always Must invoke issue-tracker-github skill to commit and push before starting any next issue")
        else:
            print("LOCAL_TRACKER: Issue finished. MUST NOT commit or push; local development only")


def main():
    parser = argparse.ArgumentParser(
        description="Safely change issue status."
    )
    parser.add_argument(
        "filename",
        help="Issue filename under agents/issues/. Example: 0001-fix-login.md",
    )
    parser.add_argument(
        "status",
        choices=["doing", "ready", "done", "draft"],
        help="Target status: doing, ready, or done.",
    )
    args = parser.parse_args()
    set_issue_status(args.filename, args.status)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
