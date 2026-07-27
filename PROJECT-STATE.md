# ATLAS - Project State

> Live status of the ATLAS project. Updated at the end of every chat.

---

## You Are Here

**Current Phase:** Phase 0: Foundations (IN PROGRESS)
**Status:** Steps 1 through 8 complete. Tool registry and typed command REPL both built, tested, and passing Ruff and mypy. Next is the package entry point.

**Next action:** Step 9, the entry point. Replace the `main()` stub in `__init__.py` with wiring that calls `setup_logging()`, builds the registry, registers the three tools, and launches `cmdloop()`.

---

## Completed Work

### Pre-Project Planning Session - April 11, 2026
- All 7 architectural decisions made and recorded in `DECISIONS.md`
- High-level architecture diagram drafted (orchestrator + PC Agent + custom protocol)
- Phase roadmap drafted (Phases 0-7+)

### Architecture and Scope Lock-In - June 19, 2026
- Project identity, three-boundary architecture, final four-agent set, MIT license
- Recorded as Decisions 8 through 18 in `DECISIONS.md`

### Phase 0 Implementation - July 2026
- **Step 1:** Monorepo skeleton, `.gitignore`, `.gitattributes` (LF normalization), `.gitkeep` placeholders
- **Step 2:** uv project initialized (`--package --name atlas --python 3.12`); Pydantic runtime dep; Ruff, mypy, pytest dev deps
- **Step 3:** `pyproject.toml` configured for all three tools (newer table syntax for pytest)
- **Step 4:** `logging_config.py` with `setup_logging()` (root DEBUG, console INFO, file DEBUG)
- **Step 5:** `Tool` ABC in `base.py` (four abstract properties + Template Method: `run()` concrete, `_execute()` abstract)
- **Step 6:** Three stub tools with Pydantic input models, allowlist validation, and logging:
  - `CalculateTool` (`CalculateInput`: `expression: str`)
  - `OpenUrlTool` (`OpenUrlInput`: `url: HttpUrl`)
  - `OpenAppTool` (`OpenAppInput`: `app_name: str`) with TOML allowlist loaded fail-fast at construction
- **Step 7:** `ToolRegistry` in `registry.py`. `register` keyed off `tool.name` with a duplicate-name collision guard raising `ValueError`; `retrieve` returning `Tool | None` with a logged warning on miss. Smoke-tested via `uv run python -c`.
- **Step 8:** `AtlasRepl` in `repl.py`, a subclass of stdlib `cmd.Cmd`. Four commands (`do_calculate`, `do_open_app`, `do_open_url`, `do_quit`) built with the explicit `do_*` method approach (Option A). Empty-arg guards; `run()` fed a raw dict so validation stays inside the Template Method; `assert not None` narrowing after each retrieve; docstrings driving `help`; `emptyline` override returning `False`. Passes Ruff and mypy.

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

- **Phase 0:** Foundations: repo, REPL, registry, schemas, logging, stub tools
- **Phase 1:** Real local Python tools (calc, time, weather, news)
- **Phase 2:** PC Agent v1 (C++): TCP server, custom protocol, first cross-process tools
- **Phase 3:** PC Agent hardening: allowlists, reconnection, protocol versioning, audit
- **Phase 4:** Sensitive operations: confirmation gates, PIN, dry-run, calendar/Notion writes
- **Phase 5:** Communication tools: email, WhatsApp, Discord (preview-and-confirm)
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
│           ├── __init__.py        # main() stub, replaced in Step 9
│           ├── logging_config.py
│           ├── registry.py
│           ├── repl.py
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

- Dispatch chosen as Option A (explicit `do_*` methods). Revisit Option B (generic `default()` routing) as a documented decision if tool count grows or the extensibility milestone forces it.
- No `default()` override yet; unknown commands show `cmd`'s stock `*** Unknown syntax`. Polish candidate.
- Empty-arg guard uses `if not arg`, which does not catch all-whitespace input.
- Shared empty-arg guard helper not extracted; the three guard messages can drift out of sync (the `open_url` missing-space bug was one instance, fixed locally, pushes with Step 9).
- README names tools `util.calculate`, `pc.open_url`, `pc.open_app`, but code uses `calculate`, `open_url`, `open_app`. Reconcile before Step 12.
- `LICENSE` file still missing; README links to it (MIT decided in Decision 18).
- `PROJECT_STATE.md` (underscore, per Master Prompt) vs `PROJECT-STATE.md` (hyphen, actual repo file) naming mismatch. Pick one.
- Phase 4 reminder: revisit Apple Calendar integration (iCloud web vs CalDAV vs Google Calendar).

---

## Next Action

Step 9: the package entry point. Replace the `main()` stub in `orchestrator/src/atlas/__init__.py` with wiring that calls `setup_logging()`, constructs the `ToolRegistry`, registers the three tools, and launches `AtlasRepl(registry).cmdloop()`. The `atlas = "atlas:main"` script hook in `pyproject.toml` is already waiting for it, so `uv run atlas` will launch the REPL once this lands.