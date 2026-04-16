from __future__ import annotations

import argparse
import json
from pathlib import Path

from memory_common import build_paths


def compact_file(path: Path) -> dict:
    if not path.exists():
        return {"file": str(path), "changed": False, "reason": "missing"}

    original = path.read_text(encoding="utf-8").splitlines()
    seen: set[str] = set()
    compacted: list[str] = []
    blank_run = 0

    for line in original:
        stripped = line.strip()
        if not stripped:
            blank_run += 1
            if blank_run <= 1:
                compacted.append("")
            continue

        blank_run = 0
        if stripped.startswith("- "):
            if stripped in seen:
                continue
            seen.add(stripped)
        compacted.append(line.rstrip())

    content = "\n".join(compacted).rstrip() + "\n"
    old_content = "\n".join(original).rstrip() + "\n"
    if content == old_content:
        return {"file": str(path), "changed": False}

    path.write_text(content, encoding="utf-8")
    return {"file": str(path), "changed": True}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compact .codex-memory files by trimming blank runs and duplicate bullets.")
    parser.add_argument("--root", help="Repository root. Defaults to current directory.")
    args = parser.parse_args()

    paths = build_paths(args.root)
    targets = [
        paths.project,
        paths.user,
        paths.conventions,
        paths.decisions,
        paths.open_questions,
        *sorted(paths.tasks_dir.glob("*.md")),
    ]
    report = [compact_file(path) for path in targets]

    print(json.dumps({
        "success": True,
        "results": report,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
