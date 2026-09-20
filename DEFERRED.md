# DEFERRED.md

Everything designed, discussed, or deliberately postponed but not yet built.
Two sections: items with a step number, and items with no step yet.

Rule: nothing gets deferred in conversation without landing here.

---

## Phase 1 — Assigned to a step

### Step 10 — Failure handling (network tools)
Applies to weather, geocode, AND news. All three share the same four gaps:
- No status-code check. A 4xx/5xx body gets `.json()`-parsed and returned as
  data. Observed live on weather.
- No `httpx.RequestError` guard. Wifi off produces a traceback.
- No timeout. `get` can hang indefinitely.
- No `KeyError` guard on response shape change.

Plus, new with news:
- Handle 429 specifically. GNews returns an `errors` array in the body.
- Key redaction is DONE, see D31. Moved out of this item.

Testing note: GNews allows 100 requests/day, resetting 00:00 UTC. Step 10 needs
real failure responses to test against, so budget requests for it.

### Step 11 — Cleanup
- **Registry missing-name contract.** `retrieve` returns `Tool | None`, so every
  caller needs a null check. `do_weather` uses `assert tool is not None`, which
  is stripped under `-O`: the check silently stops existing and becomes an
  `AttributeError` instead of a clear message. `do_news` was fixed to an
  explicit `if tool is None`. DECIDE whether `retrieve` should raise `KeyError`
  instead, making the return type plain `Tool` and removing per-caller checks
  entirely. Then fix `do_weather`. Deciding the contract once is worth more
  than fixing the symptom in two places.
- `weather` `description` property is still the placeholder "Weather tool".
  Rewrite for the D19 planner.
- Same for `GNewsTool.description`, currently "Provides News headlines and
  titles using G-News API". Describes the provider rather than the trigger
  condition, which is what a planner needs.
- Shared empty-arg guard helper. `clock` breaks the "all commands reject empty
  arg" assumption, so the pattern is currently inconsistent across commands.
  Phase 0 carryover.
- Unify logging style across tools.
- **README new-machine setup note.** `.env` is gitignored and does not sync. A
  fresh clone crashes at import with a `ValidationError` naming the calc
  fields, because `Settings()` runs at module import in `config.py`. Document:
  copy `.env.example` to `.env` and fill it. Hit once already on the Mac
  migration.
- **`lang=en` is hardcoded** in `gnews.py`'s params dict. Candidate for a
  `GNewsInput` field.
- **`le=10` on `GNewsInput.count` is tier-specific.** It is the GNews free-tier
  ceiling of articles per request, not a universal limit. Wrong the moment the
  plan changes, and invisible six months from now if not recorded here.

### Step 12 — Tests
No automated tests exist yet. All Phase 1 verification has been manual.

### Noted option, not planned work — generic `Tool` base
`Tool._execute` receives `validated_input: BaseModel`, so each tool casts to its
own input type. That states the input type twice (once in `input_model`, once in
the cast) with nothing tying them together, and `cast` is unchecked: mypy stops
looking after it.

A generic `Tool[GNewsInput]` would tie them together. Deliberately NOT planned:
- the failure is loud anyway, an `AttributeError` on the first call
- the cost of not doing it is one cast per tool, six total, none of which can be
  wrong because `run()` builds the object from `input_model` two lines earlier
- the D19 planner dispatches by name with a dict of arguments, which is dynamic
  by nature; no static type flows through the path the system actually uses
- generics and `TypeVar` are real new material for a six-line payoff

**Revisit if:** the tool count grows enough that the `input_model`/cast
duplication becomes a place mistakes actually happen, or a future layer needs
static types through `_execute`. Neither is true now.

### Noted, not planned — comprehensions vs type narrowing
`do_weather`'s `parts` list was briefly rewritten as a comprehension filtering
`(place.name, place.admin1, place.country)` on truthiness. mypy rejected it:
the tuple's element type is `str | None`, and narrowing does NOT propagate from
a comprehension's `if` clause to the element expression, so the result is
`list[str | None]` and `str.join` refuses it.

The explicit three-`if` version type-checks precisely because each `if` is a
real conditional branch that mypy can narrow inside. Reverted, correctly.

Recorded because the instinct will recur: a comprehension is not a free win
when the loop body does something the type checker can follow and the
comprehension does not.

### Phase 2 — PC Agent
- `open_url` and `open_app` remain stubs. They move to the PC Agent.

### Deferred by earlier decisions
- **D26:** `clock` is local-time only. Timezone support postponed.
- **D28:** geocoding fuzzy-match / ambiguity resolution belongs at the planner
  layer. `geocode()` stays deterministic best-match-or-None. The planner-era
  tool will expose all `count=5` matches, not just `[0]`.

---

## Athena-era — No step assigned

Design settled in the 2026-09-10 pipeline discussion. Build order is deliberate;
see A0.

### A0 — Build order
Thinnest vertical slice first, then thicken. Building left-to-right across the
pipeline diagram produces nothing runnable for months.
1. One source (GNews) + store. Fetch, canonicalize, write rows, print feed.
2. Add GDELT as second source. Forces the canonical Article model and fan-in
   partial-failure handling.
3. Add URL + title dedup. Immediately visible, since GDELT floods duplicates.
4. Scheduling + per-stage counters. Run unattended for a week. Fix what breaks.
   THIS IS THE STEP THAT GETS SKIPPED AND MATTERS MOST.
5. Embeddings + clustering. Tune against A11.
6. Extraction + validation. Last: highest pain, lowest certainty, and steps 1-5
   are useful without it.
7. Summarization, which needs 6 to be worth doing well.
RSS slots in around 2 or 3. Nearly free, but a bad first source.

### A1 — `Tool` contract returns `str`
`Tool._execute` returns a formatted human-readable string. Correct for the REPL,
useless for an aggregation layer: you cannot dedupe, embed, or cluster a
formatted string. Eventually `base.py` returns structured data and formatting
moves to a presentation layer. Touches every tool.
**Mitigated in Step 8:** parse and format are written as separate operations, so
the refactor is "return the list instead of calling the formatter."
NOT a Phase 1 change. One consumer exists today.

### A2 — Canonical `Article` model and normalization boundary
GDELT gives `url, title, domain, seendate, language, sourcecountry`. GNews gives
`title, description, content, url, image, publishedAt, source{}`. Overlap:
title, url, source, published time.
**Decided placement:** normalize in each source tool. Each tool is the adapter
for its provider and emits canonical Articles. Adding a source is then a pure
tool-layer change and Athena never learns a provider name. Rejected: adapters
inside Athena, which would mean editing the agent to add a source.
**Started in Step 8:** `gnews.py` defines an `Article` model and flattens the
nested `source{}` object to a plain `source` string, precisely so GDELT's flat
`domain` field can map to the same shape. The model currently lives in
`gnews.py`; it moves to a shared module when the second source arrives.

### A3 — GDELT source tool
Own step. Base: `https://api.gdeltproject.org/api/v2/doc/doc`,
`mode=artlist&format=json`, default 75 records, max 250 via `maxrecords`.
Teaches three things nothing else has:
- **Errors arrive as HTTP 200 with a plain-text body.** `maxrecords=251`
  returns 200 OK and the text "A maximum of 250 records can be returned."
  `.json()` raises a decode error. Step 7 taught that 200 OK is not data;
  GDELT teaches that 200 OK is not even JSON.
- Fields omitted entirely (not empty) for thinly-indexed sources. Everything
  except `url` must be optional.
- Client-side pacing. Documented ~1 req/5 sec, reported stricter in practice.
  First real rate limiter, and the concept transfers to the C++ agent.

### A4 — RSS source tool
No key, no quota, no terms problem. Curated feed list required.

### A5 — Persistence layer
SQLite first (single file, no server, stdlib). Not an optimization: it is what
makes the pipeline idempotent. Required by:
- cross-run dedup (otherwise every run reprocesses everything)
- extraction cache (never fetch a URL twice)
- summary cache (never pay for the same summary twice)
- feed history (otherwise the feed is a snapshot, not a feed)
Postgres only if concurrent writers ever appear.

### A6 — Article state machine + observability
Model an article as a row with a status, not a value flowing downward:
`discovered -> canonicalized -> deduped -> extracted -> validated ->
clustered -> summarized`, with terminal failure statuses carrying a reason.
Gives three things: each stage independently re-runnable, crashes lose nothing,
and per-stage counters become one `GROUP BY status`.
Per-stage counters (in, out, dropped-and-why) are near-free to add as you go
and miserable to retrofit. A seven-stage pipeline that silently drops 80% of
its input is undebuggable without them.

### A7 — URL canonicalization + two-tier dedup
Canonicalization: strip `utm_*` and `fbclid`, drop fragments, resolve
redirects, normalize host and trailing slash.
Dedup is deliberately dumb, two tiers only:
1. canonical URL match
2. normalized title match (lowercase, strip punctuation, strip trailing
   " | Publisher")
Anything semantic belongs to clustering (A10), not here.
**Dedup runs BEFORE extraction.** This is the load-bearing ordering decision:
extraction is the expensive, politeness-limited stage, and GDELT will hand over
the same story from hundreds of outlets.
**Observed in Step 8:** a single GNews query for "brics" returned two
near-identical articles covering the same story from different outlets, in a
five-article result set. The duplicate problem shows up at trivial scale, long
before GDELT volume enters the picture.

### A8 — Cheap filter gate before extraction
Rule-based drop stage between dedup and extraction: domain blocklist
(aggregator spam, content farms), language filter, non-article URL shapes
(`/tag/`, `/author/`, `/video/`). Every drop here is a fetch not made.

### A9 — Article extraction
Trafilatura. Best in published extraction benchmarks. Apache 2.0 since v1.8.0
(earlier versions GPLv3+, so old READMEs show the wrong licence). Current
release v2.1.0.
Known constraints going in:
- Static HTML only. No headless browser. JS-rendered articles come back empty.
- Paywalls: extraction "succeeds", content is two paragraphs and a subscribe
  prompt. Content validation must catch this (length, boilerplate phrases,
  extracted-text-to-page-size ratio).
- This makes us a crawler, not an API client: robots.txt, honest User-Agent
  with contact info, per-domain rate limiting, timeouts.
- Realistic success rate is well under 100%. The failure path is the common
  path, not the exception.

### A10 — Story clustering
Online/incremental against a time window, NOT batch k-means. k is unknown and
news arrives continuously. New article -> embed -> compare to centroids from
last N days -> join if similarity > threshold, else open a new cluster.
Stories stay open a few days then close.
Three parameters set the quality of the whole feed: embedding model, similarity
threshold, window length. All three need tuning against A11.
LLM scope is tight: embeddings do the grouping, the LLM handles boundary cases
and cluster naming. The LLM never does the O(n^2) comparison work.

### A11 — Clustering benchmark oracle
NewsAPI.ai's one-time ~2,000 tokens, reserved for this and nothing else.
Fixed article batch through our clustering vs their event endpoint, compare.
Never used as an ingestion source (see D29).

### A12 — Summarization
Per CLUSTER, not per article. Per-cluster is what makes the feed read as
intelligent ("what happened, per seven outlets, and where they disagree").
Per-article is cheaper and much less interesting.
Must be idempotent: key the summary on a hash of the input content. Without it,
every run re-summarizes yesterday, which is either GPU time or money.

### A13 — Concurrency structure
Stage latencies differ by orders of magnitude (dedup in microseconds,
extraction 1-5 sec network-bound, LLM in seconds). One synchronous loop means
the slowest stage sets throughput while everything else idles.
Stages decoupled by queues, each pulling at its own rate. `asyncio.Queue`
between coroutines in ONE process. Do NOT build a distributed queue system.
Teaches producer/consumer and backpressure properly, which transfers to the
C++ agent.

### A14 — Ingestion scheduling
No trigger designed yet. This decision sets the entire rate-limit budget:
GNews allows 4 requests/hour, GDELT wants 1 per 5 seconds. Those numbers mean
nothing until a cadence is chosen.

### A15 — Fan-in topology and partial failure
Sources are parallel, not chained. When GNews 429s at request 101, the run
continues on GDELT and RSS with a logged degradation rather than aborting.
Has to be a designed behaviour, not an accident.

### A16 — Article bodies are not available from either primary source
GDELT returns no body at all. GNews free returns truncated content. So A12 will
be summarizing titles and short descriptions, not articles. This caps the
quality of the whole pipeline.
Options, none chosen: accept headline-level summarization; do A9 ourselves
(real work, legally grey per outlet); or pay a provider that returns bodies.
Flagged, not solved.
**Confirmed in Step 8:** GNews free tier truncates `content`, observed as
`"... [2585 chars]"` in live responses. Also confirmed: the free tier runs 12
hours behind real time, reported by the API itself in
`information.realTimeArticles`. Both constraints are now facts rather than
third-party claims.