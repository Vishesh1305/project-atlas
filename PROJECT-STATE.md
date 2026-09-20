# PROJECT_STATE.md

## You Are Here
**Phase:** 1 (Real Local + Networked Tools) — IN PROGRESS
**Current step:** Step 8 COMPLETE (news tool, first keyed HTTP call, live and
tree-green). Next: Step 9 (register/wire pass).

## Completed Phases
- **Phase 0 (COMPLETE):** Repo, typed REPL, registry + Pydantic schemas, logging,
  three stub tools. Tree-green.

## Phase 1 Progress
- **Plan:** Approved. Four info tools: calculate, clock, weather (keyless HTTP),
  news (keyed HTTP). open_url/open_app stay stubs -> PC Agent, Phase 2.
- **Step 1 (COMPLETE):** httpx + python-dotenv; .env + .env.example.
- **Step 2 (COMPLETE):** config.py — Settings(BaseSettings), pathlib-anchored .env.
- **Step 3 (COMPLETE):** calculate tool — safe AST evaluator + config rounding.
- **Steps 4 & 5 (COMPLETE):** clock tool. Package tools/hourglass/; command "clock".
- **Step 6 (COMPLETE):** HTTP teaching block (no code). Bottom-up via /learn.
- **Step 7 PART 1 (COMPLETE):** weather tool — lat/lon direct, first real HTTP call.
  WeatherInput lat/lon with Field(ge/le). params dict annotated
  dict[str, str | float]. current= is ONE comma-joined string, no trailing comma,
  no space (both malformations hit and fixed live — read the wire URL to catch
  them). Parse: result['current'][field] / result['current_units'][field].
- **Step 7 PART 2 (COMPLETE):** geocoding — place name -> lat/lon -> weather.
  geocode() standalone in tools/weather/geocode.py, NOT a Tool, keeps weather a
  pure coords-in unit. GeocodeResult with optional admin1/country. Not-found
  guard `if not data.get("results"): return None`. do_weather takes the whole
  arg as the place name, null-checks before dereference, prints a D27
  resolved-place header. Verified live incl. the D28 sevasi case.
- **Step 8 (COMPLETE):** GNews tool — first KEYED HTTP call.
  - Package tools/news/, file gnews.py, command "gnews". One file per provider;
    gdelt.py lands in the same package later.
  - GNewsInput: model_config = ConfigDict(strict=True, str_strip_whitespace=True)
    (D33). topic: str = Field(min_length=1). count: int = Field(default=5,
    ge=1, le=10) — first field with default AND constraint; le=10 is the free
    tier's per-request ceiling, enforced at the boundary so 20 is REJECTED, not
    silently clamped the way GNews would.
  - Article(BaseModel): title, url, source, published, description | None.
    source flattened from the nested source.name object (GDELT's equivalent is
    a flat domain, so flattening here is what lets one model serve both — A2).
    published maps from publishedAt, so field names deliberately differ from
    JSON keys and ** unpacking cannot be used (unlike GeocodeResult).
  - parse_articles(data) -> list[Article]: module-level, .get("articles", []),
    explicit kwargs, .get("description") for the optional field, subscripts for
    required ones (loud KeyError is wanted there).
  - format_articles(articles) -> str: module-level, `if not articles` guard
    (NOT `is None` — parse never returns None), enumerate(start=1), two-level
    join ("\n" within a block, "\n\n" between), three-space indent, description
    line conditionally appended.
  - Parse and format are SEPARATE operations, so A1's eventual structured-return
    refactor is a one-line change.
  - _execute order: credential guard, cast, params, request, parse, format.
  - Credential guard per D30: `if not key` (truthiness, because .env may hold
    an empty string, not None), returns an ordinary string. Also the mypy
    narrowing construct for str | None.
  - Verified live: "formula 1" (multi-word), "brics" (single word), gibberish
    (empty-results path), missing key (disabled message), default count=5 firing.
  - Tree-green: ruff check + mypy clean, 23 files.
- **Step 8 side work (not in the original plan):**
  - **D31 redaction filter.** Key was appearing in the httpx request line, in
    terminal scrollback and in atlas.log. RedactSecrets(logging.Filter) on both
    handlers. Verified live.
  - **D32 shared Settings.** gnews.py was constructing a second Settings
    instance; fixed project-wide.
  - **Key rotated twice** during development after two accidental exposures.
    atlas.log confirmed gitignored (.gitignore:92 `*.log`) and never committed
    (`git log --all -- orchestrator/atlas.log` empty).
- **Steps 9–12:** Pending (register/wire pass, error handling, cleanup, tests).

## Key Decisions (recent)
- **D33:** Validation strictness is project-wide via model_config, not per
  field. Verified: str_strip_whitespace DOES fire under strict=True; config
  strict reaches every field.
- **D32:** One shared Settings instance, constructed once in config.py.
- **D31:** Secret redaction via a logging.Filter on both handlers (not by
  silencing httpx). Filter must be on HANDLERS, not loggers. httpx uses lazy
  %-formatting so the URL is in record.args, not record.msg.
- **D30:** Credential enforcement inside _execute at the tool boundary,
  returning an ordinary string. Amends D21's "at load/registration" wording.
- **D29 (+ amendment):** GDELT (volume, keyless) + GNews (ranking, keyed) + RSS
  (curated third). NewsAPI.ai excluded as a source, reserved as a clustering
  benchmark oracle. GNews free-tier 12-hour delay now CONFIRMED by the API's own
  `information.realTimeArticles` field.
- **D28:** Geocoding fuzzy-match is the planner's job, not the tool's.
- **D27:** Geocoding disambiguation = user pre-qualify + show-matches header,
  no interactive picker.
- **D26:** clock tool local-time only; timezones deferred.
- **D25:** reST docstrings (no :type:/:rtype:).
- **D20:** httpx, not requests, not an SDK. Learn from the wire.

## File Tree (abbreviated)

DECISIONS.md
DEFERRED.md
PROJECT_STATE.md
orchestrator/src/atlas/
    config.py          # settings = Settings() — the ONE shared instance (D32)
    repl.py            # do_calculate, do_clock, do_weather, do_news,
                       #   do_open_app, do_open_url
    registry.py
    logging_config.py  # + RedactSecrets filter (D31)
    tools/
        base.py
        calculator/    # calculate.py + calc_engine.py
        hourglass/     # clock.py — command "clock"
        weather/       # weather.py + geocode.py — command "weather"
        news/          # gnews.py — command "gnews"
        url_launcher/  # stub
        app_launcher/  # stub

## Known Issues / Carried Debt
Near-term only. Design-level and Athena-era items live in DEFERRED.md.

- **All three network tools have NO failure handling (deliberate, Step 10):**
  no status-code check, no RequestError guard, no timeout, no KeyError guard.
  Applies to weather, geocode, AND news.
- **do_weather still uses `assert tool is not None`.** Stripped under -O, would
  become an AttributeError. do_news was fixed to an explicit check. The real
  question is the registry's contract; see DEFERRED.md Step 11.
- weather + gnews `description` properties need rewriting for the D19 planner
  before Phase 1 close.
- Phase 0 carryover -> Step 11: shared empty-arg guard helper (clock breaks the
  "all commands reject empty arg" assumption). Also unify logging style.
- **THREE machines now:** Windows laptop (E:\), Windows workstation (Z:\), and
  the MacBook Pro, which is now the main machine. Git-synced, push before
  switching. `.env` is gitignored and does NOT sync: a fresh clone crashes at
  import until it is created. Watch path handling and line endings across OSes.
- GNews quota is 100 requests/day, resets 00:00 UTC. Step 10 will need real
  failure responses to test against; budget for it.

## Next Action
Step 9: register/wire pass. Review that every tool is registered consistently
and that the composition root in __init__.py is coherent now that five real
tools exist.