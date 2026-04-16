from __future__ import annotations

import argparse
import json
from pathlib import Path

from memory_common import append_text, build_paths, current_date, target_path


def read_source(path: str | None) -> str:
    if not path:
        return ""
    return Path(path).expanduser().resolve().read_text(encoding="utf-8").strip()


def has_exact_line(path: Path, content: str) -> bool:
    if not path.exists():
        return False
    lines = {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
    return content.strip() in lines


def render_promoted_entry(target: str, content: str, title: str | None) -> str:
    date = current_date()
    clean = content.strip()
    if target == "decisions":
        heading = title or "Promoted decision"
        return (
            f"\n## {date} - {heading}\n\n"
            f"### Decision\n{clean}\n"
        )
    if target == "open-questions":
        heading = title or "Promoted open question"
        return (
            f"\n## {date} - {heading}\n\n"
            f"- Context: {clean}\n"
            f"- Next check: TBD\n"
        )
    return f"\n- {clean}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote durable knowledge into long-lived memory files.")
    parser.add_argument("--root", help="Repository root. Defaults to current directory.")
    parser.add_argument("--target", required=True, choices=["project", "user", "conventions", "decisions", "open-questions"])
    parser.add_argument("--content", default="")
    parser.add_argument("--source", help="Optional text file to read content from.")
    parser.add_argument("--title", help="Optional title for decisions/open questions.")
    args = parser.parse_args()

    content = args.content.strip() or read_source(args.source)
    if not content:
        raise SystemExit("No content provided. Use --content or --source.")

    paths = build_paths(args.root)
    destination = target_path(paths, args.target)

    if has_exact_line(destination, content):
        print(json.dumps({
            "success": True,
            "file": str(destination),
            "skipped": True,
            "reason": "duplicate",
        }, ensure_ascii=False, indent=2))
        return 0

    append_text(destination, render_promoted_entry(args.target, content, args.title))
    print(json.dumps({
        "success": True,
        "file": str(destination),
        "target": args.target,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
