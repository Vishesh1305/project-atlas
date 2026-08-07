# PROJECT_STATE.md

## You Are Here
**Phase:** 1 (Real Local + Networked Tools) — IN PROGRESS
**Current step:** Step 2 complete (config.py). Next: Step 3 (real calculate — safe eval).

## Completed Phases
- **Phase 0 (COMPLETE):** Repo structure, `cmd`-based typed REPL, tool registry
  + Pydantic schemas, logging, three stub tools (`calculate`, `open_url`,
  `open_app`). Runs via `uv run atlas`. Full tree passes `mypy .`, `ruff check .`,
  `pytest` (3 tests). Committed to `main`.

## Phase 1 Progress
- **Plan:** Approved. Four information tools: `calculate` (real safe eval),
  `time` (local), `weather` (HTTP, keyless), `news` (HTTP, key-based).
  `open_url`/`open_app` remain stubs — PC Agent actions, deferred to Phase 2.
- **Step 1 (COMPLETE):** Added `httpx` + `python-dotenv` via uv. Created `.env`
  (git-ignored, verified via `git check-ignore`), `.env.example` (committed).
- **Step 2 (COMPLETE):** `config.py` written. `Settings(BaseSettings)` from
  pydantic-settings, reads `.env` via `SettingsConfigDict(env_file=...)` anchored
  with pathlib (`Path(__file__).parents[2]`). `news_api_key: str | None = None`
  (optional at config layer, per D21). Verified: reads real value when present,
  falls back to None when absent, no crash. Added `pydantic-settings` dependency.
  Full tree green (ruff, mypy 12 files, pytest 3).
- **Steps 3–12:** Pending. Next is Step 3 (real `calculate`: safe expression
  evaluation, no `eval`).

## Key Decisions (recent)
- **D21:** Config = pydantic-settings `Settings` class. Secret fields optional at
  config layer (str | None), so ATLAS boots without them. Tools assert their own
  credentials and fail-fast with a specific message at the tool boundary.
- **D20:** HTTP client = `httpx`. Providers = Open-Meteo (keyless weather) +
  key-based news. Networking taught full bottom-up from sockets, deferred to Step 6.
- **D19:** Agents = LLM planner layer above deterministic tool registry. Autonomy
  scoped by security policy. LLM hosting provisional: local, always-on, co-located.

## File Tree (abbreviated)

Atlas/
├── DECISIONS.md
├── PROJECT_STATE.md
└── orchestrator/
├── .env # git-ignored (placeholder news key)
├── .env.example # committed template
├── .gitignore # ignores .env, *.key
├── pyproject.toml # httpx, python-dotenv, pydantic-settings
├── uv.lock
├── config/allowlist.toml
├── src/atlas/
│ ├── config.py # NEW: Settings(BaseSettings), pathlib-anchored .env
│ ├── tools/ # calculate, open_url, open_app (stubs)
│ ├── registry.py
│ └── repl.py
└── tests/
├── test_registry.py
└── test_tools.py

## Known Issues / Carried Debt
- Phase 0 carryover, folded into Phase 1 Step 11: extract shared empty-arg guard
  helper in repl.py; unify logging style.
- Working across two machines: laptop (E:\Projects\Atlas\) and workstation
  (Z:\Projects\Windows\project-atlas\). Same repo, git-synced. Push before switching.

## Next Action
Step 3: make `calculate` real. Safe evaluation of a math expression string WITHOUT
`eval` (security trap — taught first). Builder chooses a safe-eval approach, then writes.