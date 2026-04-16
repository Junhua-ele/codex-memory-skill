from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from memory_common import build_paths


VAGUE_PATTERNS = [
    re.compile(r"\bmaybe\b", re.IGNORECASE),
    re.compile(r"\bprobably\b", re.IGNORECASE),
    re.compile(r"\bguess\b", re.IGNORECASE),
]


def inspect_file(path: Path) -> list[dict]:
    issues: list[dict] = []
    if not path.exists():
        issues.append({"file": str(path), "type": "missing"})
        return issues

    seen: dict[str, int] = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped in seen:
            issues.append({
                "file": str(path),
                "line": index,
                "type": "duplicate-line",
                "first_seen": seen[stripped],
                "text": stripped,
            })
        else:
            seen[stripped] = index

        for pattern in VAGUE_PATTERNS:
            if pattern.search(stripped):
                issues.append({
                    "file": str(path),
                    "line": index,
                    "type": "vague-language",
                    "text": stripped,
                })
                break

        for candidate in re.findall(r"`([^`]+)`", stripped):
            if ("/" in candidate or "\\" in candidate) and not Path(candidate).exists():
                issues.append({
                    "file": str(path),
                    "line": index,
                    "type": "broken-path-reference",
                    "text": candidate,
                })
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check .codex-memory for missing files and obvious quality issues.")
    parser.add_argument("--root", help="Repository root. Defaults to current directory.")
    args = parser.parse_args()

    paths = build_paths(args.root)
    targets = [
        paths.readme,
        paths.project,
        paths.user,
        paths.conventions,
        paths.decisions,
        paths.open_questions,
        *sorted(paths.tasks_dir.glob("*.md")),
    ]

    issues: list[dict] = []
    for target in targets:
        issues.extend(inspect_file(target))

    print(json.dumps({
        "success": True,
        "issue_count": len(issues),
        "issues": issues,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
