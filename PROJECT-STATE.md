# PROJECT_STATE.md

## You Are Here
**Phase:** 1 (Real Local + Networked Tools) — IN PROGRESS
**Current step:** Step 3 COMPLETE (calculate tool fully wired). Next: Step 4 (time tool).

## Completed Phases
- **Phase 0 (COMPLETE):** Repo, typed REPL, registry + Pydantic schemas, logging,
  three stub tools. `uv run atlas` verified. Tree-green (mypy, ruff, pytest x3).

## Phase 1 Progress
- **Plan:** Approved. Four info tools: calculate, time, weather (keyless HTTP),
  news (key HTTP). open_url/open_app stay stubs → PC Agent, Phase 2.
- **Step 1 (COMPLETE):** httpx + python-dotenv; .env (git-ignored) + .env.example.
- **Step 2 (COMPLETE):** config.py — Settings(BaseSettings), pathlib-anchored .env,
  news_api_key optional (D21). Added pydantic-settings.
- **Step 3 (COMPLETE):** calculate tool fully working.
  - calc_engine.py: safe AST evaluator (Constant, BinOp, UnaryOp, whitelisted Call).
    Whitelist-by-construction security; single CalculatorError contract; div-by-zero
    and domain errors rewrapped. Full precision preserved.
  - calculate.py: wraps engine. Validates via base, calls safe_eval in try/except
    CalculatorError, returns clean user message on failure (no traceback leaks),
    lazy %s logging.
  - Config-driven rounding: calc_round (bool) + calc_decimals (int) fields on
    Settings. Toggle verified live via .env (CALC_ROUND=false → full precision).
  - Tree-green (ruff, mypy 16 files).
- **Steps 4–12:** Pending (time, HTTP teaching, weather, news, cleanup, tests).

## Key Decisions (recent)
- **D25:** reST docstrings (no :type:/:rtype:). Standing doc rule + link official docs.
- **D24:** v1 scope + NFC placement. Beta internal. Advanced-calc/vision post-beta.
- **D23:** Deferred capstone caps parked (NFC, voice output, vision).
- **D22:** calculate scalar now, powerful later.
- **D21:** Config secrets optional at config layer, enforced at tool boundary.

## File Tree (abbreviated)

orchestrator/
├── config/allowlist.toml
└── src/atlas/
├── config.py # Settings: news_api_key, calc_round, calc_decimals
├── repl.py # do_calculate wired to real tool
└── tools/
├── base.py # Tool base (root)
├── calculator/
│ ├── init.py
│ ├── calculate.py # DONE: wraps engine, config rounding
│ └── calc_engine.py# DONE: safe evaluator
├── url_launcher/ # stub
└── app_launcher/ # stub

## Known Issues / Carried Debt
- Phase 0 carryover → Step 11: shared empty-arg guard helper (do_calculate/
  do_open_app/do_open_url all duplicate the not-arg check); unify logging style
  (mostly done — verify no f-string logs remain).
- Two machines (laptop E:\ / workstation Z:\), git-synced. Push before switching.

## Next Action
Step 4: build the `time` tool. Simplest real tool — near-empty input, local-only,
no HTTP. Teaches the minimal-input Pydantic case. Then register + wire do_time.