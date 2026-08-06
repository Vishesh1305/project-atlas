# PROJECT_STATE.md

## You Are Here
**Phase:** 1 (Real Local + Networked Tools) — IN PROGRESS
**Current step:** Step 1 complete (Dependency + Secrets Setup). Next: Step 2 (config.py).

## Completed Phases
- **Phase 0 (COMPLETE):** Repo structure, `cmd`-based typed REPL, tool registry
  + Pydantic schemas, logging, three stub tools (`calculate`, `open_url`,
  `open_app`). Runs via `uv run atlas`. Full tree passes `mypy .`, `ruff check .`,
  `pytest` (3 tests). Committed to `main`.

## Phase 1 Progress
- **Plan:** Approved. Four information tools: `calculate` (real safe eval),
  `time` (local), `weather` (HTTP, keyless), `news` (HTTP, key-based).
  `open_url`/`open_app` remain stubs — they are PC Agent actions, deferred to Phase 2.
- **Step 1 (COMPLETE):** Added `httpx` and `python-dotenv` via uv. Created `.env`
  (git-ignored, verified via `git check-ignore`), `.env.example` (committed
  template). `.gitignore` updated to exclude `.env` before any real key was added.
- **Steps 2–12:** Pending. Next is Step 2 (config.py: load .env via dotenv, expose
  keys using pathlib).

## Key Decisions (recent)
- **D20:** HTTP client = `httpx` (governance situation acknowledged, async-readiness
  chosen). Providers = Open-Meteo (keyless weather) + key-based news. Networking
  taught full bottom-up from sockets, deferred to Step 6.
- **D19:** Agents = LLM planner layer above deterministic tool registry. Autonomy
  scoped by security policy (free over `none`, gated at `confirm`/`PIN`). LLM
  hosting provisional: local, always-on, co-located with orchestrator.

## File Tree (abbreviated)

Atlas/
├── DECISIONS.md
├── PROJECT_STATE.md
└── orchestrator/
├── .env # NEW (git-ignored)
├── .env.example # NEW (committed template)
├── .gitignore # MODIFIED (ignores .env)
├── pyproject.toml # MODIFIED (httpx, python-dotenv added)
├── uv.lock # MODIFIED (locked graph)
├── config/allowlist.toml
├── src/atlas/
│ ├── tools/ # calculate, open_url, open_app (stubs)
│ ├── registry.py
│ └── repl.py
└── tests/test_tools.py

## Known Issues / Carried Debt
- Phase 0 carryover, folded into Phase 1 Step 11: extract shared empty-arg guard
  helper in repl.py; unify logging style.
- Working across two machines: laptop (cloned at E:\Projects\Atlas\) and main
  workstation (Z:\Projects\Windows\project-atlas\). Same repo, synced via git.
  Commit/push before switching machines to stay current.