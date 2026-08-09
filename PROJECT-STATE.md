# PROJECT_STATE.md

## You Are Here
**Phase:** 1 (Real Local + Networked Tools) — IN PROGRESS
**Current step:** Step 3 core complete (calc_engine.py — safe evaluator). Next:
wire calc_engine into calculate.py (the Tool), incl. rounding feature.

## Completed Phases
- **Phase 0 (COMPLETE):** Repo, typed REPL, registry + Pydantic schemas, logging,
  three stub tools. `uv run atlas` verified. Tree-green (mypy, ruff, pytest x3).

## Phase 1 Progress
- **Plan:** Approved. Four info tools: calculate, time, weather (keyless HTTP),
  news (key HTTP). open_url/open_app stay stubs → PC Agent, Phase 2.
- **Step 1 (COMPLETE):** httpx + python-dotenv added; .env (git-ignored, verified)
  + .env.example.
- **Step 2 (COMPLETE):** config.py — Settings(BaseSettings), pathlib-anchored .env,
  news_api_key optional (D21). Added pydantic-settings.
- **Step 3 core (COMPLETE):** calc_engine.py — safe AST-based scalar evaluator.
  Handles Constant, BinOp (+ - * / // % **), UnaryOp (neg/pos), Call (whitelisted
  math functions). Security model: whitelist-by-construction, single else-refusal.
  Verified: __import__/foo() refused (don't execute); nested args recurse;
  div-by-zero rewrapped. Single CalculatorError contract. Full precision preserved
  (rounding deferred to tool layer). Tree-green (ruff, mypy).
- **Step 3 remaining:** wire calc_engine → calculate.py (Pydantic input schema,
  try/except CalculatorError, logging, 4-dp rounding w/ on-off toggle via config).
- **Steps 4–12:** Pending (time, HTTP teaching, weather, news, cleanup, tests).

## Key Decisions (recent)
- **D25:** reST/Sphinx docstrings (no :type:/:rtype:; types in signatures). Standing
  doc rule: code carries docstrings as written; link official docs on new APIs.
- **D24:** v1 scope + NFC placement (NFC in v1, built in voice/Pi phase). Beta =
  internal. Advanced-calc + vision = post-beta "future vision" on site.
- **D23:** Deferred capstone caps parked (NFC wake, voice output, vision).
- **D22:** calculate scalar now, powerful later (vector/symbolic via libs/LLM).
- **D21:** Config secrets optional at config layer, enforced at tool boundary.

## File Tree (abbreviated)

orchestrator/src/atlas/
├── config.py # Settings(BaseSettings)
└── tools/
├── base.py # Tool base (stays at root)
├── calculator/
│ ├── init.py
│ ├── calculate.py # Tool wrapper (NEXT: wire engine in)
│ └── calc_engine.py # DONE: safe evaluator
├── url_launcher/
│ ├── init.py
│ └── url_launcher.py # stub
└── app_launcher/
├── init.py
└── app_launcher.py # stub

(Tools refactored to package-per-tool: folder + __init__.py each, base.py at root.)

## Known Issues / Carried Debt
- Phase 0 carryover → Phase 1 Step 11: shared empty-arg guard helper; unify logging.
- Rounding (4-dp + toggle) to be built at calculate.py tool boundary, NOT engine.
- Two machines (laptop E:\ / workstation Z:\), git-synced. Push before switching.

## Next Action
Wire calc_engine.safe_eval into calculate.py: define Pydantic input schema, call
safe_eval inside try/except CalculatorError, log failures, return clean result to
user, add 4-decimal rounding with config toggle. Then register/verify via REPL.