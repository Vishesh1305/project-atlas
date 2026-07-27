# ATLAS - Project State

> Live status of the ATLAS project. Updated at the end of every chat.

---

## You Are Here

**Current Phase:** Phase 0: Foundations (COMPLETE)
**Status:** Phase 0 closed. ATLAS runs via `uv run atlas`: composition root wires logging, registry, three stub tools, and the REPL. Verified end to end. Full tree passes `mypy .`, `ruff check .`, and `pytest` (3 tests). Committed to `main`.

**Next action:** Begin Phase 1 (real local tools). Starts with a Technical Plan and approval gate.

---

## Completed Work

### Pre-Project Planning Session - April 11, 2026
- All 7 architectural decisions made and recorded in `DECISIONS.md`
- High-level architecture diagram drafted (orchestrator + PC Agent + custom protocol)
- Phase roadmap drafted (Phases 0-7+)

### Architecture and Scope Lock-In - June 19, 2026
- Project identity, three-boundary architecture, final four-agent set, MIT license
- Recorded as Decisions 8 through 18 in `DECISIONS.md`

### Phase 0 Implementation - July 2026 (COMPLETE)
- **Step 1:** Monorepo skeleton, `.gitignore`, `.gitattributes` (LF normalization), `.gitkeep` placeholders
- **Step 2:** uv project initialized (`--package --name atlas --python 3.12`); Pydantic runtime dep; Ruff, mypy, pytest dev deps
- **Step 3:** `pyproject.toml` configured; pytest table corrected to `[tool.pytest.ini_options]`
- **Step 4:** `logging_config.py` with `setup_logging()` (root DEBUG, console INFO, file DEBUG)
- **Step 5:** `Tool` ABC in `base.py` (four abstract properties + Template Method: `run()` concrete validates, `_execute()` abstract acts)
- **Step 6:** Three stub tools with Pydantic input models, allowlist validation, and logging:
  - `CalculateTool` (`CalculateInput`: `expression: str`)
  - `OpenUrlTool` (`OpenUrlInput`: `url: HttpUrl`)
  - `OpenAppTool` (`OpenAppInput`: `app_name: str`) with TOML allowlist loaded fail-fast at construction
- **Step 7:** `ToolRegistry` in `registry.py`. `register` keyed off `tool.name` with a duplicate-name collision guard raising `ValueError`; `retrieve` returning `Tool | None` with a logged warning on miss. Dict typed `dict[str, Tool]`. Smoke-tested.
- **Step 8:** `AtlasRepl` in `repl.py`, a subclass of stdlib `cmd.Cmd`. Four commands (`do_calculate`, `do_open_app`, `do_open_url`, `do_quit`) via the explicit `do_*` method approach (Option A). Empty-arg guards; `run()` fed a raw dict so validation stays inside the Template Method; `assert not None` narrowing after each retrieve; docstrings driving `help`; `emptyline` override returning `False`.
- **Step 9:** `main()` in `__init__.py`, the composition root. Calls `setup_logging()` first, builds the `ToolRegistry`, registers the three tools, launches `AtlasRepl(registry).cmdloop()`. Wired to the `atlas = "atlas:main"` script hook, so `uv run atlas` starts the REPL.
- **Step 10:** `tests/` suite. `test_registry.py`: fake `Tool` subclass for isolation, `test_retrieve_returns_registered_tool` (hit), `test_register_duplicate_raises` (collision via `pytest.raises`). `test_tools.py`: `test_run_invalid_input_returns_error_not_raises` (Template Method swallows `ValidationError`). 3 passed. Scope deliberately cut from 5 planned to 3 under time constraint.
- **Step 11:** End-to-end verification. All ten command paths driven live through `uv run atlas`: valid commands, empty-arg guard, bad-URL validation, allowlist rejection, unknown command, help, empty line, quit. Logging confirmed (INFO on success, WARNING on validation failure). No regressions through `main()`.
- **Step 12:** Phase 0 close. Code-review pass (no bugs). README tool names corrected from dotted (`util.calculate`, etc.) to match shipped code (`calculate`, `open_url`, `open_app`). Whole-tree `mypy .` surfaced three missing-annotation / untyped-dict errors that per-file checks had hidden; all fixed. Full suite + linters green tree-wide. Committed.

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

- **Phase 0:** Foundations: repo, REPL, registry, schemas, logging, stub tools (COMPLETE)
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
│   ├── src/
│   │   └── atlas/
│   │       ├── __init__.py        # main() composition root
│   │       ├── logging_config.py
│   │       ├── registry.py
│   │       ├── repl.py
│   │       └── tools/
│   │           ├── base.py
│   │           ├── calculate.py
│   │           ├── open_url.py
│   │           └── open_app.py
│   └── tests/
│       ├── test_registry.py
│       └── test_tools.py
├── pc_agent/
├── shared/
├── docs/
├── DECISIONS.md
├── LICENSE
├── PROJECT-STATE.md
└── README.md

---

## Known Issues / Open Items

- Shared empty-arg guard helper not extracted; the three guard messages are triplicated and can drift. Carried from Phase 0 as the deferred closing refactor.
- Guard messages have a double space in the empty-arg output (cosmetic; fixed for free if the helper is extracted).
- Empty-arg guard uses `if not arg`, which does not catch all-whitespace input (though `cmd` strips the arg, so trailing-space cases collapse to empty and are caught).
- `run()` returns the full Pydantic error string (including the errors.pydantic.dev URL) to the user. Consider a terser user-facing message with full detail in the log, in Phase 1.
- Logging call style inconsistent: `open_app.py` uses f-string interpolation, `registry.py` uses lazy `%s`. Pick one in a Phase 1 sweep.
- Dispatch chosen as Option A (explicit `do_*` methods). Revisit Option B (generic `default()` routing) as a documented decision if tool count grows.
- No `default()` override; unknown commands show `cmd`'s stock `*** Unknown syntax`. Polish candidate.
- Test scope cut at Step 10: `retrieve` miss test and valid-input `run()` test not written. Add before Phase 1 if coverage is wanted.
- `atlas.log` uses a relative path, lands in the current working directory. Ignored by `.gitignore`. Revisit if a fixed location is wanted.
- `PROJECT_STATE.md` (underscore, Master Prompt) vs `PROJECT-STATE.md` (hyphen, repo + README). Resolved in favor of the hyphen; Master Prompt is the outlier to reconcile.
- Phase 4 reminder: revisit Apple Calendar integration (iCloud web vs CalDAV vs Google Calendar).

---

## Next Action

Begin Phase 1: real local tools (calc, time, weather, news). Present the Phase 1 Technical Plan and stop at the approval gate before any code. First design question for Phase 1: whether tool names gain namespace prefixes (the dotted `util.` / `pc.` scheme from the old README), decided properly alongside how tools are keyed and dispatched.