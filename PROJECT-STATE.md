# PROJECT_STATE.md

## You Are Here

**Phase:** 1 (Real Local + Networked Tools) - IN PROGRESS
**Current step:** Step 9 COMPLETE (register/wire pass: composition root moved,
names namespaced, registry contract changed, REPL commands brought to one
shape). Tree-green. Next: Step 10 (failure handling for the network tools).
Step 9 is UNCOMMITTED; commit planned at phase end (see Known Issues).

## Completed Phases

- **Phase 0 (COMPLETE):** Repo, typed REPL, registry + Pydantic schemas, logging,
  three stub tools. Tree-green.

## Phase 1 Progress

- **Plan:** Approved. Four info tools: calculate, clock, weather (keyless HTTP),
  news (keyed HTTP). open_url/open_app stay stubs -> PC Agent, Phase 2.
- **Step 1 (COMPLETE):** httpx + python-dotenv; .env + .env.example.
- **Step 2 (COMPLETE):** config.py: Settings(BaseSettings), pathlib-anchored .env.
- **Step 3 (COMPLETE):** calculate tool - safe AST evaluator + config rounding.
- **Steps 4 & 5 (COMPLETE):** clock tool. Package tools/hourglass/; command "clock".
- **Step 6 (COMPLETE):** HTTP teaching block (no code). Bottom-up via /learn.
- **Step 7 PART 1 (COMPLETE):** weather tool - lat/lon direct, first real HTTP call.
  WeatherInput lat/lon with Field(ge/le). params dict annotated
  dict[str, str | float]. current= is ONE comma-joined string, no trailing comma,
  no space (both malformations hit and fixed live - read the wire URL to catch
  them). Parse: result['current'][field] / result['current_units'][field].
- **Step 7 PART 2 (COMPLETE):** geocoding - place name -> lat/lon -> weather.
  geocode() standalone in tools/weather/geocode.py, NOT a Tool, keeps weather a
  pure coords-in unit. GeocodeResult with optional admin1/country. Not-found
  guard `if not data.get("results"): return None`. do_weather takes the whole
  arg as the place name, null-checks before dereference, prints a D27
  resolved-place header. Verified live incl. the D28 sevasi case.
- **Step 8 (COMPLETE):** GNews tool - first KEYED HTTP call.
  - Package tools/news/, file gnews.py, REPL command "news" (corrected
    2026-10-26: previously recorded here as "gnews"; registry name was "gnews",
    now "info.news" per D37). One file per provider; gdelt.py lands in the
    same package later.
  - GNewsInput: model_config = ConfigDict(strict=True, str_strip_whitespace=True)
    (D33). topic: str = Field(min_length=1). count: int = Field(default=5,
    ge=1, le=10) - first field with default AND constraint; le=10 is the free
    tier's per-request ceiling, enforced at the boundary so 20 is REJECTED, not
    silently clamped the way GNews would.
  - Article(BaseModel): title, url, source, published, description | None.
    source flattened from the nested source.name object (GDELT's equivalent is
    a flat domain, so flattening here is what lets one model serve both - A2).
    published maps from publishedAt, so field names deliberately differ from
    JSON keys and ** unpacking cannot be used (unlike GeocodeResult).
  - parse_articles(data) -> list[Article]: module-level, .get("articles", []),
    explicit kwargs, .get("description") for the optional field, subscripts for
    required ones (loud KeyError is wanted there).
  - format_articles(articles) -> str: module-level, `if not articles` guard
    (NOT `is None` - parse never returns None), enumerate(start=1), two-level
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
- **Documentation backfill (2026-10-05, COMPLETE):**
  - **D27 and D28 were missing entirely** from DECISIONS.md. They existed only
    as one-liners in this file. Both reconstructed and inserted in numeric
    order. Dates are placeholders pending the Step 7 Part 2 commit date.
  - **D29 and D30 full entries added.** Only the D29 amendment had been
    committed; the entries it amends were absent. The amendment was also moved
    from after D33 to directly under D29.
  - **D34 (cross-platform PC Agent) and D35 (Tauri 2 GUI) added.**
  - **Decision 22 placeholder added.** The number is referenced by D24 but has
    no entry. Recorded as a visible gap with a TODO rather than a silent skip.
  - **D21 amended-by note and typo fix.** D21 now points forward to D30.
  - **DEFERRED.md restructured.** Phase 2 promoted from a `###` nested under
    Phase 1 to its own `##` section. New `## Phase 3+` section added (G0-G5).
    Markdown fixes throughout: the D34 table and several bold paragraphs were
    being absorbed into preceding lists and would not have rendered on GitHub.
- **Step 9 (COMPLETE, 2026-10-26):** register/wire pass. Baseline green before
  starting (ruff clean, mypy 23 files).
  - **9.1, composition root (D36).** `main()` moved from `atlas/__init__.py`
    to `atlas/app.py`; `__init__.py` is now empty; `[project.scripts]` is
    `atlas = "atlas.app:main"`; `uv sync` regenerated `.venv/bin/atlas`
    (verified it now imports from `atlas.app`). Proof: with `.env` moved aside,
    `tests/test_registry.py` passes; `tests/test_tools.py` still needs `.env`
    (the separate Settings-at-import item).
  - **9.2, registry contract (D38).** `retrieve` returns plain `Tool` via
    direct indexing and raises `KeyError` on a missing name. Internal dict
    renamed `_tools`. `register` keeps its LBYL membership check. New test
    `test_retrieve_missing_raises`. Old `retrieve` body kept as comments.
  - **9.3, names (D37).** `util.calculate`, `util.clock`, `info.weather`,
    `info.news`, `pc.open_app`, `pc.open_url`. 12 string sites (6 pairs)
    verified by grep. REPL commands unchanged (cmd cannot parse dots).
  - **9.4, `do_*` shape (D38).** Docstring (summary, Usage, Example), guard
    with example, unchecked retrieve, pre-processing after retrieve, run/print.
    `clock` rejects arguments. `do_weather` retrieves before geocoding. All
    locals named `tool`. `do_*` docstrings drop `:param:` (scoped D25
    exception). Superseded guards, asserts and the `do_news` None check kept as
    comments.
  - **9.6, docs.** DECISIONS D36-D38 added, D25 amended-by note. DEFERRED:
    Step 11 contract item marked resolved, Step 12 correction (tests DO exist)
    plus the REPL-to-registry name test, help-indentation note, Phase 2 items
    (failed-construction policy, Windows-only allowlist, typed sensitivity),
    G5 ordering lock, A3 GDELT naming question. All additions; no lines removed.
  - Verified: pytest 4 passed, ruff clean, mypy clean 24 files. REPL: `help`
    lists all 8 commands as documented; every empty-arg message correct;
    `clock foo` rejected; stubs and live tools unchanged.
  - Corrections surfaced during the review: five `do_*` methods used `assert`
    (not just `do_weather`); `OpenAppTool.__init__` does I/O (reads
    allowlist.toml), so "no constructor does real work" was false.
- **Steps 9-12:** Pending (register/wire pass, error handling, cleanup, tests).
  Update 2026-10-26: Step 9 complete; Steps 10-12 pending.

## Key Decisions (recent)

- **D38:** `ToolRegistry.retrieve` raises `KeyError` (EAFP); REPL does not catch
  it, the planner will. Canonical `do_*` shape; no-arg commands reject args.
  `do_*` docstrings are user-facing help (scoped D25 exception).
- **D37:** Tool names are `<namespace>.<capability>`: `util.*` local, `info.*`
  network reads, `pc.*` actions on the user's machine. Never the provider name.
  REPL commands stay dot-free.
- **D36:** Composition root in `atlas/app.py`; `__init__.py` empty, no re-export.
- **D35:** GUI is Tauri 2 + TypeScript, with a thin Rust shell (windowing,
  tray, packaging only, no business logic). Flutter considered and rejected
  (Dart serves no career goal). Hard prerequisite: an orchestrator API, since
  the REPL currently calls tools in-process. Phase 3+ at the earliest.
- **D34:** PC Agent is cross-platform (Windows, macOS, Linux). Portable
  transport, platform-specific action layer behind a `PlatformActions`
  interface. macOS implemented first. Wayland blocks global window control by
  design, so Linux window management is X11 only.
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

```
DECISIONS.md       # D1-D38; D22 is a placeholder, entry missing
DEFERRED.md        # Phase 1 steps, Phase 2, Phase 3+ (G0-G5), Athena-era (A0-A16)
PROJECT_STATE.md
README.md          # STALE: still says "Phase 0 in progress" (DEFERRED G5)
orchestrator/src/atlas/
    __init__.py        # empty (D36)
    app.py             # composition root: main(), registration (D36)
    config.py          # settings = Settings(): the ONE shared instance (D32)
    repl.py            # do_calculate, do_clock, do_weather, do_news,
                       #   do_open_app, do_open_url (one shape, D38)
    registry.py        # retrieve raises KeyError; _tools (D38)
    logging_config.py  # + RedactSecrets filter (D31)
    tools/
        base.py
        calculator/    # calculate.py + calc_engine.py: util.calculate
        hourglass/     # clock.py: util.clock, command "clock"
        weather/       # weather.py + geocode.py: info.weather, command "weather"
        news/          # gnews.py: info.news, command "news"
        url_launcher/  # stub: pc.open_url
        app_launcher/  # stub: pc.open_app
orchestrator/tests/
    test_registry.py   # 3 tests
    test_tools.py      # 1 test
```

## Known Issues / Carried Debt

Near-term only. Design-level, Phase 2+, and Athena-era items live in DEFERRED.md.

- **All three network tools have NO failure handling (deliberate, Step 10):**
  no status-code check, no RequestError guard, no timeout, no KeyError guard.
  Applies to weather, geocode, AND news.
- **do_weather still uses `assert tool is not None`.** Stripped under -O, would
  become an AttributeError. do_news was fixed to an explicit check. The real
  question is the registry's contract; see DEFERRED.md Step 11.
  **RESOLVED in Step 9 (D38).** Asserts in all five methods are commented out.
- weather + gnews `description` properties need rewriting for the D19 planner
  before Phase 1 close.
- Phase 0 carryover -> Step 11: shared empty-arg guard helper (clock breaks the
  "all commands reject empty arg" assumption). Also unify logging style.
  Shapes are now uniform (D38); the helper must cover "argument required" and
  "argument forbidden".
- **Commented-out superseded code** in `repl.py` and `registry.py` from
  Step 9. Decide whether to remove before Phase 1 close (DEFERRED Step 11).
- **Decision 22 has no entry.** Referenced by D24 as "advanced-calculate".
  Either reconstruct it from the original discussion or retire the number and
  amend D24. Placeholder block in DECISIONS.md marks the gap.
- **D27 and D28 dates are placeholders** ("September 2026"). Replace with the
  real dates from the Step 7 Part 2 commits.
- **README.md is stale** (DEFERRED G5). Says Phase 0, no GUI phase in the
  roadmap table, no mention of the cross-platform agent. Update at Phase 1
  close so it is one edit rather than three.
  **Ordering locked (2026-10-26):** README rewrite is the FIRST action once
  Step 12 is complete, before the Phase 1 completion checklist and before any
  Phase 2 planning. Close DEFERRED G5 in the same commit. If the checklist's
  architecture diagram update changes the diagram, fold it into that same
  README pass.
- **Uncommitted work.** Steps 9 onward are uncommitted by choice (commit at
  phase end). Only on the Mac until pushed. At commit time: plain
  `git reset` (never `--hard`), then `git add -A`; `app.py` was staged early
  and the staged copy is stale.
- **THREE machines now:** Windows laptop (E:\), Windows workstation (Z:\), and
  the MacBook Pro, which is now the main machine. Git-synced, push before
  switching. `.env` is gitignored and does NOT sync: a fresh clone crashes at
  import until it is created. Watch path handling and line endings across OSes.
  SSH keys are per machine; the Mac is now configured with its own.
- GNews quota is 100 requests/day, resets 00:00 UTC. Step 10 will need real
  failure responses to test against; budget for it.

## Next Action

Step 10: failure handling for weather, geocode and news. Four shared gaps
(status-code check, `httpx.RequestError` guard, timeout, `KeyError` guard on
response shape) plus GNews 429 handling. See DEFERRED Step 10.

Files needed at chat start: `tools/weather/weather.py`,
`tools/weather/geocode.py`, `tools/news/gnews.py`.

**Phase 1 close sequence (locked):**
1. Step 12 complete, tree-green.
2. README.md rewrite (closes DEFERRED G5). FIRST, no exceptions.
3. Phase 1 completion checklist: code review, comprehension check, refactor
   opportunity, architecture diagram update.
4. Phase 2 Technical Plan, approval gate.
