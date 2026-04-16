# Memory Schema

This file defines the expected structure of `.codex-memory/`.

## Directory

```text
.codex-memory/
├── README.md
├── PROJECT.md
├── USER.md
├── CONVENTIONS.md
├── decisions.md
├── open-questions.md
├── tasks/
│   └── YYYY-MM.md
└── archive/
```

## `PROJECT.md`

Recommended sections:

```markdown
# Project Memory

## Overview
## Structure
## Run Commands
## Test Commands
## Build and Release
## Environment Constraints
## Important Files
## Known Stable Facts
```

Only keep stable, reusable repo facts here.

## `USER.md`

Recommended sections:

```markdown
# User Memory

## Communication Preferences
## Workflow Preferences
## Repo-Specific Preferences
```

Only keep project-scoped user preferences here.

## `CONVENTIONS.md`

Recommended sections:

```markdown
# Project Conventions

## Code Style
## Naming
## Testing
## Review Expectations
## Documentation
```

## `decisions.md`

One entry per decision:

```markdown
## 2026-04-15 - Decision title

### Decision
...

### Reason
...

### Consequence
...
```

## `open-questions.md`

One entry per unresolved item:

```markdown
## 2026-04-15 - Question title

- Context: ...
- What is unknown: ...
- Next check: ...
```

## `tasks/YYYY-MM.md`

One entry per task:

```markdown
## 2026-04-15 - Task title

### Problem
- ...

### Root Cause
- ...

### Changes
- ...

### Validation
- ...

### Follow-ups
- ...

### Tags
- build
- ci
```

## Promotion rules

Promote to long-lived files only when the item is:

- likely to remain true
- likely to be reused
- specific enough to be actionable

Do not promote:

- temporary logs
- speculative explanations
- one-off paths
- raw stack traces
- chain-of-thought
- plain-text secrets
