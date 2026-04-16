from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from memory_common import build_paths


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def collect_matches(
    *,
    files: list[Path],
    query: str,
    path_filter: str | None,
    month: str | None,
    tag: str | None,
    case_sensitive: bool,
    context_lines: int,
) -> list[dict]:
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(re.escape(query), flags)
    results: list[dict] = []

    for path in files:
        rel = str(path)
        if path_filter and path_filter not in rel:
            continue
        if month and path.parent.name == "tasks" and month not in path.name:
            continue

        lines = path.read_text(encoding="utf-8").splitlines()
        if tag and not any(tag in line for line in lines):
            continue

        for index, line in enumerate(lines):
            if not pattern.search(line):
                continue
            start = max(0, index - context_lines)
            end = min(len(lines), index + context_lines + 1)
            snippet = "\n".join(lines[start:end]).strip()
            results.append({
                "file": rel,
                "line": index + 1,
                "snippet": snippet,
            })
    return results


def print_text(results: list[dict]) -> None:
    if not results:
        print("No matches found.")
        return
    for item in results:
        print(f"{item['file']}:{item['line']}")
        print(item["snippet"])
        print("-" * 60)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search .codex-memory markdown files.")
    parser.add_argument("query")
    parser.add_argument("--root", help="Repository root. Defaults to current directory.")
    parser.add_argument("--path", help="Only search files whose path contains this substring.")
    parser.add_argument("--month", help="Only search a given task month, e.g. 2026-04.")
    parser.add_argument("--tag", help="Only return files containing this tag substring.")
    parser.add_argument("--case-sensitive", action="store_true")
    parser.add_argument("--context-lines", type=int, default=2)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    paths = build_paths(args.root)
    files = iter_markdown_files(paths.memory_root)
    results = collect_matches(
        files=files,
        query=args.query,
        path_filter=args.path,
        month=args.month,
        tag=args.tag,
        case_sensitive=args.case_sensitive,
        context_lines=max(0, args.context_lines),
    )

    if args.json:
        print(json.dumps({
            "success": True,
            "count": len(results),
            "results": results,
        }, ensure_ascii=False, indent=2))
    else:
        print_text(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
