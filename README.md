# memory-skill

`memory-skill` is a project-level memory solution designed for codex referencing the Hermes' memory framework.

It includes:

- a `SKILL.md`
- a `references/` folder
- some python scripts

Enable Codex to have more stable long-term memory and historical recall ability in specific software projects.

## What it can do

It mainly addresses the following types of problems:

- Each time the same project is entered, codex have to re-understand the context
- Project rules and preferences previously explained by the user are easily lost
- Experience cannot be accumulated after completing complex tasks
- Historical issue repair records are difficult to reuse

This skill devides project memory into two categories：

- **Stable facts**
  - Project structure
  - Run Commands
  - Test Commands
  - Environment Constraints
  - User preferences
- **Historical recall**

## Directory Structure

```text
project-memory-skill/
├── SKILL.md
├── README.md
├── references/
│   ├── memory-schema.md
└── scripts/
    ├── memory_common.py
    ├── memory-init.py
    ├── memory-search.py
    ├── memory-capture.py
    ├── memory-promote.py
    ├── memory-compact.py
    └── memory-check.py
```

## Description

### `SKILL.md`

The skill file.

### `references/memory-schema.md`

Define the files structure of `.codex-memory/` and responsibilies of each file.

### `scripts/`

There are seven python scripts. In most cases, it is decided by codex itself whether to call it.

- `memory-init.py`
  - Initialize `.codex-memory/`
- `memory-search.py`
  - Search historical memory
- `memory-capture.py`
  - Record a test event
- `memory-promote.py`
  - Update a test event to long-term memory
- `memory-compact.py`
  - Compress and organize memory files
- `memory-check.py`
  - Quality Inspection
- `memory_common.py`

## How to use

### 1. Install it to Codex skills

Copy the skill to：

```text
.codex\skills\memory
```

### 2. Initialize it in a project repo

Please let codex to initialize the memory repo at the first time.

### 3. daily use

It's just like using hermes agent.

