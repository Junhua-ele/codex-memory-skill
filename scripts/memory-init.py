from __future__ import annotations

import argparse
import json

from memory_common import build_paths, month_task_file, write_if_missing


README_TEMPLATE = """# Project Memory

This directory stores repo-scoped memory for Codex.

- `PROJECT.md`: stable facts about the repo
- `USER.md`: repo-scoped user preferences
- `CONVENTIONS.md`: coding and review conventions
- `decisions.md`: important technical decisions
- `open-questions.md`: unresolved issues worth revisiting
- `tasks/YYYY-MM.md`: task history and episodic recall
"""


PROJECT_TEMPLATE = """# Project Memory

## Overview

## Structure

## Run Commands

## Test Commands

## Build and Release

## Environment Constraints

## Important Files

## Known Stable Facts
"""


USER_TEMPLATE = """# User Memory

## Communication Preferences

## Workflow Preferences

## Repo-Specific Preferences
"""


CONVENTIONS_TEMPLATE = """# Project Conventions

## Code Style

## Naming

## Testing

## Review Expectations

## Documentation
"""


DECISIONS_TEMPLATE = "# Decisions\n"
OPEN_QUESTIONS_TEMPLATE = "# Open Questions\n"
TASK_TEMPLATE = "# Task History\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize .codex-memory in a repo.")
    parser.add_argument("--root", help="Repository root. Defaults to current directory.")
    args = parser.parse_args()

    paths = build_paths(args.root)
    created: list[str] = []

    paths.memory_root.mkdir(parents=True, exist_ok=True)
    paths.tasks_dir.mkdir(parents=True, exist_ok=True)
    paths.archive_dir.mkdir(parents=True, exist_ok=True)

    for path, content in [
        (paths.readme, README_TEMPLATE),
        (paths.project, PROJECT_TEMPLATE),
        (paths.user, USER_TEMPLATE),
        (paths.conventions, CONVENTIONS_TEMPLATE),
        (paths.decisions, DECISIONS_TEMPLATE),
        (paths.open_questions, OPEN_QUESTIONS_TEMPLATE),
        (month_task_file(paths), TASK_TEMPLATE),
    ]:
        if write_if_missing(path, content):
            created.append(str(path))

    print(json.dumps({
        "success": True,
        "root": str(paths.root),
        "memory_root": str(paths.memory_root),
        "created": created,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
