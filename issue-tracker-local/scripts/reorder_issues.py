import re
import sys
from pathlib import Path

ISSUES_DIR = Path("agents/issues")


def reorder_issues():
    if not ISSUES_DIR.exists():
        print("No issues directory found.")
        return

    # Collect all issue files with their current IDs
    issues = []
    for path in ISSUES_DIR.glob("*.md"):
        match = re.match(r"^(\d+)-(.+)", path.name)
        if match:
            current_id = int(match.group(1))
            slug = match.group(2)
            issues.append((current_id, slug, path))

    if not issues:
        print("No issues found.")
        return

    # Sort by current ID
    issues.sort(key=lambda x: x[0])

    # Calculate new sequential IDs
    new_ids = list(range(1, len(issues) + 1))

    # Build rename plan: [(old_path, temp_path, new_path, new_id_str), ...]
    plan = []
    for idx, (current_id, slug, path) in enumerate(issues):
        new_id = new_ids[idx]
        if new_id == current_id:
            continue
        new_id_str = f"{new_id:04d}"
        temp_path = path.parent / f"_reorder_{new_id_str}-{slug}"
        new_path = path.parent / f"{new_id_str}-{slug}"
        plan.append((path, temp_path, new_path, new_id_str))

    if not plan:
        print("Issues are already in order. Nothing to do.")
        return

    # Phase 1: rename to temp names (avoids collisions)
    for old_path, temp_path, new_path, new_id_str in plan:
        old_path.rename(temp_path)

    # Phase 2: rename temp to final, update YAML frontmatter id
    for old_path, temp_path, new_path, new_id_str in plan:
        content = temp_path.read_text(encoding="utf-8")
        content = re.sub(
            r"^id:.*$",
            f"id: {new_id_str}",
            content,
            count=1,
            flags=re.MULTILINE,
        )
        temp_path.write_text(content, encoding="utf-8")
        temp_path.rename(new_path)
        print(f"{old_path.name} -> {new_path.name}")

    print(f"\nReordered {len(plan)} issue(s).")


if __name__ == "__main__":
    try:
        reorder_issues()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
