# PROJECT_STATE.md

## You Are Here
**Phase:** 1 (Real Local + Networked Tools) — IN PROGRESS
**Current step:** Steps 4 & 5 COMPLETE (clock tool built + wired). Next: Step 6
(HTTP teaching block — networking from fundamentals, no code).

## Completed Phases
- **Phase 0 (COMPLETE):** Repo, typed REPL, registry + Pydantic schemas, logging,
  three stub tools. Tree-green.

## Phase 1 Progress
- **Plan:** Approved. Four info tools: calculate, clock, weather (keyless HTTP),
  news (key HTTP). open_url/open_app stay stubs → PC Agent, Phase 2.
- **Step 1 (COMPLETE):** httpx + python-dotenv; .env + .env.example.
- **Step 2 (COMPLETE):** config.py — Settings(BaseSettings), pathlib-anchored .env.
- **Step 3 (COMPLETE):** calculate tool — safe AST evaluator + config rounding.
- **Steps 4 & 5 (COMPLETE):** clock tool.
  - Package tools/hourglass/ (folder avoids time.py stdlib collision); command
    name "clock".
  - Empty-input pattern: ClockInput(BaseModel) with no fields; run({}) validates.
  - _execute formats datetime.now() → "Tue 11th Aug 2026, 09:48 PM" (ordinal
    suffix via _suffix helper). sensitivity "none".
  - Registered in composition root; do_clock wired in repl.py. Verified live via
    `uv run atlas`. Note: clock accepts empty arg (unlike calculate) — relevant
    for Step 11 guard-helper extraction.
- **Steps 6–12:** Pending (HTTP teaching, weather, news, register/wire, error
  handling, cleanup, tests).

## Key Decisions (recent)
- **D26:** clock tool local-time only; timezones deferred (planner does cross-zone
  analysis on top of tool, per D19).
- **D25:** reST docstrings (no :type:/:rtype:). Standing doc rule.
- **D24:** v1 scope + NFC placement.
- **D22:** calculate scalar now, powerful later.
- **D21:** Config secrets optional at config layer, enforced at tool boundary.

## File Tree (abbreviated)

orchestrator/src/atlas/
├── config.py
├── repl.py # do_calculate, do_clock, do_open_app, do_open_url
└── tools/
├── base.py
├── calculator/ # calculate.py + calc_engine.py (DONE)
├── hourglass/ # clock.py (DONE) — command name "clock"
├── url_launcher/ # stub
└── app_launcher/ # stub

## Known Issues / Carried Debt
- Phase 0 carryover → Step 11: shared empty-arg guard helper. NOTE: clock breaks
  the "all commands reject empty arg" assumption — helper can't be blindly applied.
  Also unify logging style.
- Two machines (laptop E:\ / workstation Z:\), git-synced. Push before switching.

## Next Action
Step 6: HTTP teaching block. NO code — networking from fundamentals (sockets, bytes
on the wire, up to HTTP request/response, status codes, JSON). Bottom-up per D20.
Prepares for Step 7 (weather, first real HTTP call).