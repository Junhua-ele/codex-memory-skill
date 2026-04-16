from __future__ import annotations

import argparse
import json

from memory_common import append_text, build_paths, bulletize, current_date, month_task_file, normalize_tags


def split_multiline(value: str | None) -> list[str]:
    if not value:
        return []
    return [line.strip() for line in value.split("\n") if line.strip()]


def render_entry(
    *,
    title: str,
    problem: list[str],
    root_cause: list[str],
    changes: list[str],
    validation: list[str],
    follow_ups: list[str],
    tags: list[str],
) -> str:
    date = current_date()
    return (
        f"\n## {date} - {title}\n\n"
        f"### Problem\n{bulletize(problem)}\n"
        f"### Root Cause\n{bulletize(root_cause)}\n"
        f"### Changes\n{bulletize(changes)}\n"
        f"### Validation\n{bulletize(validation)}\n"
        f"### Follow-ups\n{bulletize(follow_ups)}\n"
        f"### Tags\n{bulletize(tags)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a task record to .codex-memory/tasks/YYYY-MM.md.")
    parser.add_argument("--root", help="Repository root. Defaults to current directory.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--problem", default="")
    parser.add_argument("--root-cause", default="")
    parser.add_argument("--changes", default="")
    parser.add_argument("--validation", default="")
    parser.add_argument("--follow-ups", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--month", help="Optional target month, e.g. 2026-04")
    args = parser.parse_args()

    paths = build_paths(args.root)
    target = month_task_file(paths, args.month)

    entry = render_entry(
        title=args.title.strip(),
        problem=split_multiline(args.problem),
        root_cause=split_multiline(args.root_cause),
        changes=split_multiline(args.changes),
        validation=split_multiline(args.validation),
        follow_ups=split_multiline(args.follow_ups),
        tags=normalize_tags(args.tags),
    )
    append_text(target, entry)

    print(json.dumps({
        "success": True,
        "file": str(target),
        "title": args.title.strip(),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
