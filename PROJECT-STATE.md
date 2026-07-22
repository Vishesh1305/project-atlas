# ATLAS - Project State

> Live status of the ATLAS project. Updated at the end of every chat.

---

## You Are Here

**Current Phase:** Phase 0: Foundations (IN PROGRESS)
**Status:** Steps 1 through 6 complete. Three stub tools built and validated. Currently at the Step 7 approval gate (Tool Registry).

**Next action:** Approve the Step 7 (Tool Registry) technical plan, then build the registry.

---

## Completed Work

### Pre-Project Planning Session - April 11, 2026
- All 7 architectural decisions made and recorded in `DECISIONS.md`
- High-level architecture diagram drafted (orchestrator + PC Agent + custom protocol)
- Phase roadmap drafted (Phases 0-7+)

### Architecture and Scope Lock-In - June 19, 2026
- Project identity, three-boundary architecture, final four-agent set, MIT license
- Recorded as Decisions 8 through 18 in `DECISIONS.md`

### Phase 0 Implementation (Steps 1-6) - July 2026
- **Step 1:** Monorepo skeleton, `.gitignore`, `.gitattributes` (LF normalization), `.gitkeep` placeholders
- **Step 2:** uv project initialized (`--package --name atlas --python 3.12`); Pydantic runtime dep; Ruff, mypy, pytest dev deps
- **Step 3:** `pyproject.toml` configured for all three tools (newer table syntax for pytest)
- **Step 4:** `logging_config.py` with `setup_logging()` (root DEBUG, console INFO, file DEBUG)
- **Step 5:** `Tool` ABC in `base.py` (four abstract properties + Template Method: `run()` concrete, `_execute()` abstract)
- **Step 6:** Three working stub tools with Pydantic input models, allowlist validation, and logging:
  - `CalculateTool` (`CalculateInput`: `expression: str`)
  - `OpenUrlTool` (`OpenUrlInput`: `url: HttpUrl`)
  - `OpenAppTool` (`OpenAppInput`: `app_name: str`) with TOML allowlist loaded fail-fast at construction

---

## Architectural Summary (the locked-in stack)

- **Languages:** Python (orchestrator), C++ (PC Agent, deferred to Phase 1/2)
- **Python framework:** stdlib `cmd` + Pydantic
- **Repo layout:** monorepo with `orchestrator/`, `pc_agent/`, `shared/`, `docs/`
- **Python tooling:** Ruff (lint/format) + mypy (type check)
- **Python IDE:** PyCharm Community Edition
- **C++ IDE (later):** Visual Studio 2026 Community
- **Testing:** pytest
- **Version control:** Git + GitHub Flow (main + feature branches)
- **Dependency management:** uv
- **OS:** Windows
- **Hardware status:** No Raspberry Pi, no NAS, all hardware-dependent features mocked or deferred

See `DECISIONS.md` for full reasoning on each choice.

---

## Phase Roadmap (titles only)

- **Phase 0:** Foundations: repo, venv, REPL, registry, schemas, logging, stub tools
- **Phase 1:** Real local Python tools (calc, time, weather, news)
- **Phase 2:** PC Agent v1 (C++): TCP server, custom protocol, first cross-process tools
- **Phase 3:** PC Agent hardening: allowlists, reconnection, protocol versioning, audit
- **Phase 4:** Sensitive operations: confirmation gates, PIN, dry-run, calendar/Notion writes
- **Phase 5:** Communication tools: email, WhatsApp, Discord (with preview-and-confirm)
- **Phase 6:** Polish + portfolio prep: README, docs, demo, coverage, recruiter-ready
- **Phase 7+:** Hardware-dependent (Pi, NAS, voice, lights, WoL), DEFERRED

---

## Current File Tree

project-atlas/
├── orchestrator/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── config/
│   │   └── allowlist.toml
│   └── src/
│       └── atlas/
│           ├── __init__.py
│           ├── logging_config.py
│           └── tools/
│               ├── base.py
│               ├── calculate.py
│               ├── open_url.py
│               └── open_app.py
├── pc_agent/
├── shared/
├── docs/
├── DECISIONS.md
├── PROJECT-STATE.md
└── README.md

---

## Known Issues / Open Items

- DECISIONS entries 8-18 generated in the June 19 brainstorm; confirm they are appended to `DECISIONS.md`
- `PROJECT_STATE.md` (underscore, per Master Prompt) vs `PROJECT-STATE.md` (hyphen, actual repo file) naming mismatch; pick one
- Phase 4 reminder: revisit Apple Calendar integration (iCloud web vs CalDAV vs Google Calendar)

---

## Next Action

Approve the Step 7 (Tool Registry) technical plan, then implement `orchestrator/src/atlas/registry.py`.