from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MEMORY_DIRNAME = ".codex-memory"


@dataclass(frozen=True)
class MemoryPaths:
    root: Path
    memory_root: Path
    tasks_dir: Path
    archive_dir: Path
    readme: Path
    project: Path
    user: Path
    conventions: Path
    decisions: Path
    open_questions: Path


def resolve_repo_root(root: str | None) -> Path:
    if root:
        return Path(root).expanduser().resolve()
    return Path.cwd().resolve()


def build_paths(root: str | None) -> MemoryPaths:
    repo_root = resolve_repo_root(root)
    memory_root = repo_root / MEMORY_DIRNAME
    return MemoryPaths(
        root=repo_root,
        memory_root=memory_root,
        tasks_dir=memory_root / "tasks",
        archive_dir=memory_root / "archive",
        readme=memory_root / "README.md",
        project=memory_root / "PROJECT.md",
        user=memory_root / "USER.md",
        conventions=memory_root / "CONVENTIONS.md",
        decisions=memory_root / "decisions.md",
        open_questions=memory_root / "open-questions.md",
    )


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")
    return True


def append_text(path: Path, content: str) -> None:
    ensure_parent(path)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def current_month_slug() -> str:
    return datetime.now().strftime("%Y-%m")


def month_task_file(paths: MemoryPaths, month: str | None = None) -> Path:
    slug = month or current_month_slug()
    return paths.tasks_dir / f"{slug}.md"


def target_path(paths: MemoryPaths, target: str) -> Path:
    mapping = {
        "project": paths.project,
        "user": paths.user,
        "conventions": paths.conventions,
        "decisions": paths.decisions,
        "open-questions": paths.open_questions,
    }
    if target not in mapping:
        raise KeyError(f"Unknown target: {target}")
    return mapping[target]


def normalize_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def bulletize(lines: list[str]) -> str:
    if not lines:
        return "- None\n"
    return "".join(f"- {line}\n" for line in lines)
