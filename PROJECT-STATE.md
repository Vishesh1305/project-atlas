# PROJECT_STATE.md

## You Are Here
**Phase:** 1 (Real Local + Networked Tools) — IN PROGRESS
**Current step:** Step 7 PART 1 COMPLETE (weather tool, lat/lon direct, first real
HTTP call working end to end). Next: Step 7 PART 2 (geocoding — place name → lat/lon).

## Completed Phases
- **Phase 0 (COMPLETE):** Repo, typed REPL, registry + Pydantic schemas, logging,
  three stub tools. Tree-green.

## Phase 1 Progress
- **Plan:** Approved. Four info tools: calculate, clock, weather (keyless HTTP),
  news (key HTTP). open_url/open_app stay stubs → PC Agent, Phase 2.
- **Step 1 (COMPLETE):** httpx + python-dotenv; .env + .env.example.
- **Step 2 (COMPLETE):** config.py — Settings(BaseSettings), pathlib-anchored .env.
- **Step 3 (COMPLETE):** calculate tool — safe AST evaluator + config rounding.
- **Steps 4 & 5 (COMPLETE):** clock tool. Package tools/hourglass/; command "clock";
  empty-input pattern (ClockInput no fields); ordinal-suffix date format.
- **Step 6 (COMPLETE):** HTTP teaching block (no code). Bottom-up via /learn.
- **Step 7 PART 1 (COMPLETE):** weather tool — lat/lon direct, first real HTTP call.
  - Package tools/weather/ (renamed from weather_tool/ for naming consistency);
    command name "weather".
  - WeatherInput(BaseModel): latitude/longitude as float, Field(ge/le) range
    constraints (-90..90, -180..180). Validates + rejects out-of-range at boundary.
  - _execute: httpx.get() to Open-Meteo keyless forecast endpoint. params dict
    annotated dict[str, str | float] (mixed-value dict → mypy inferred object
    without annotation; annotation gives httpx the concrete types it needs).
  - current= param is ONE comma-joined string "temperature_2m,relative_humidity_2m"
    — NOT a list (list → httpx emits repeated ?current=&current= → 400) and NO
    space after comma (space → %2C+ on wire → 400). Both bugs hit and fixed live.
  - Parse: value → result['current'][field]; unit → result['current_units'][field]
    (same field-name key, two sibling top-level dicts). temperature_unit is a
    REQUEST param, not a response field — docs mix-up caught.
  - Output: "Temperature: 31.8°C\nRelative Humidity: 60%". Verified 200 OK live
    (Vadodara coords).
  - do_weather wired in repl.py: splits arg on whitespace, len()==2 guard (rejects
    1 or 3 args cleanly, no IndexError), builds dict, calls run(). Registered in
    composition root.
  - Tree-green: ruff + mypy both pass on whole tree (20 files).
- **Step 7 PART 2 (NEXT):** geocoding. User types place name → geocode via
  Open-Meteo geocoding endpoint (first HTTP call) → feed resulting lat/lon into
  the Part 1 weather call (second HTTP call). New failure path: place not found
  → geocoding returns empty results → tell user "no such place", NO weather call.
  This is where the "200 OK but empty/not-what-you-wanted body" case becomes real.
- **Steps 8–12:** Pending (news, register/wire pass, error handling, cleanup, tests).

## Key Decisions (recent)
- **D26:** clock tool local-time only; timezones deferred.
- **D25:** reST docstrings (no :type:/:rtype:). Standing doc rule.
- **D24:** v1 scope + NFC placement.
- **D22:** calculate scalar now, powerful later.
- **D21:** Config secrets optional at config layer, enforced at tool boundary.
- **D20:** httpx (not requests, not openmeteo-requests SDK). Rejected the official
  Open-Meteo Python SDK deliberately: it wraps the HTTP call away, drags in
  requests + caching + retry + FlatBuffers, and returns binary objects not JSON —
  defeats the Phase 1 learn-networking-from-the-wire premise. Plain REST + httpx.

## File Tree (abbreviated)

orchestrator/src/atlas/
    config.py
    repl.py            # do_calculate, do_clock, do_weather, do_open_app, do_open_url
    registry.py
    tools/
        base.py
        calculator/    # calculate.py + calc_engine.py
        hourglass/     # clock.py — command "clock"
        weather/       # weather.py — command "weather" (PART 1 done)
        url_launcher/  # stub
        app_launcher/  # stub

## Known Issues / Carried Debt
- **Step 7 Part 1 has NO failure handling (deliberate, scheduled Step 10):**
  no status-code check (a 4xx/5xx body gets .json()-parsed and returned as if it
  were data — observed live during the 400 debugging); no httpx.RequestError guard
  (wifi off → traceback); no timeout (httpx.get can hang — pass timeout= in Step 10);
  no KeyError guard if response shape changes. These are the three failure
  categories from the Step 6 comprehension check + timeout.
- weather description property still placeholder "Weather tool" — rewrite to
  describe behavior (for the D19 LLM planner) before Phase 1 close.
- do_weather empty-arg message still says "Expression" (copied from do_calculate)
  and carries the double-space bug — folds into Step 11 cleanup.
- Phase 0 carryover → Step 11: shared empty-arg guard helper. NOTE: clock breaks
  the "all commands reject empty arg" assumption. Also unify logging style.
- Two machines (laptop E:\ / workstation Z:\), git-synced. Push before switching.

## Next Action
Step 7 Part 2: geocoding. Take place name, hit Open-Meteo geocoding endpoint,
handle the not-found (empty results) case cleanly, feed lat/lon into the existing
Part 1 weather call. Keep "get coordinates" and "get weather for coordinates" as
separate concerns so the Part 1 logic is reused unchanged, not rewritten.