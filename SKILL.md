---
name: project-memory
description: Use when working in an existing software project that benefits from durable repo-scoped memory. This skill defines how Codex should read, search, capture, promote, compact, and check `.codex-memory/` so stable project facts stay separate from task history.
---

# Project Memory

This skill gives Codex a repo-scoped memory workflow using project files plus helper scripts.

Use it when:

- working in an existing repo with recurring context
- the user references prior work, decisions, or known pitfalls
- a complex task should leave behind durable notes
- a project needs consistent startup context across sessions

Do not use it for:

- one-off throwaway tasks
- generic global preferences unrelated to one repo
- storing secrets in plain text

## Memory model

Treat `.codex-memory/` as three layers:

1. Stable facts
   - `PROJECT.md`
   - `USER.md`
   - `CONVENTIONS.md`
2. Historical recall
   - `tasks/YYYY-MM.md`
   - `decisions.md`
   - `open-questions.md`
3. Control surface
   - this skill
   - repo `AGENTS.md`
   - helper scripts

Rule:

- stable facts go to long-lived files
- task outcomes go to monthly task logs
- major decisions go to `decisions.md`
- unresolved items go to `open-questions.md`

## Operating procedure

First-use rule:

- The first time this skill is used in a repository, if `.codex-memory/` does not exist, initialize it immediately before doing other memory operations.
- Do not ask the user whether to initialize unless the repository is read-only or the user explicitly forbids repo-local memory files.

### Start of task

1. Locate the repo root.
2. Check whether `.codex-memory/` exists.
3. If missing, initialize it immediately with:

```powershell
python project-memory-skill/scripts/memory-init.py --root <repo>
```

4. After initialization or if memory already exists, read, in this order:
   - `.codex-memory/PROJECT.md`
   - `.codex-memory/CONVENTIONS.md`
   - latest `.codex-memory/tasks/YYYY-MM.md`
   - `.codex-memory/decisions.md` when architecture or tradeoffs matter

When the user says "last time", "before", "we already solved this", or similar, search memory first:

```powershell
python project-memory-skill/scripts/memory-search.py "<query>" --root <repo>
```

### During task

- Do not write unverified guesses to long-term memory.
- Do not dump raw logs or step-by-step chain-of-thought into memory files.
- Do not store secrets in plain text.
- If sensitive information truly must be remembered, confirm with the user first and keep it out of shared memory files by default.

### End of task

Capture the event record:

```powershell
python project-memory-skill/scripts/memory-capture.py ^
  --root <repo> ^
  --title "<task title>" ^
  --problem "<problem>" ^
  --root-cause "<root cause>" ^
  --changes "<what changed>" ^
  --validation "<how it was checked>" ^
  --follow-ups "<remaining work>" ^
  --tags tag1,tag2
```

If the task produced durable project knowledge, promote it:

```powershell
python project-memory-skill/scripts/memory-promote.py ^
  --root <repo> ^
  --target project ^
  --content "<durable fact>"
```

Valid targets:

- `project`
- `user`
- `conventions`
- `decisions`
- `open-questions`

## Maintenance

Run periodic cleanup:

```powershell
python project-memory-skill/scripts/memory-compact.py --root <repo>
python project-memory-skill/scripts/memory-check.py --root <repo>
```

Use `memory-compact.py` to reduce duplication and normalize files.
Use `memory-check.py` to find missing files, repeated lines, vague entries, broken links, and obvious consistency problems.

## File semantics

- `PROJECT.md`: stable repo facts, commands, structure, environment constraints
- `USER.md`: repo-specific user preferences only
- `CONVENTIONS.md`: coding and review rules for this repo
- `decisions.md`: durable design choices and reasons
- `open-questions.md`: unresolved items worth revisiting
- `tasks/YYYY-MM.md`: event memory, not permanent truth

Read [references/memory-schema.md](references/memory-schema.md) when you need the detailed schemas and examples.
