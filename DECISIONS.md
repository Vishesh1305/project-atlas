# ATLAS - Architectural Decisions Log

This document records every significant architectural decision made during ATLAS development. Each entry includes what was decided, what alternatives were considered, the reasoning, and the date.

---

## Decision 1: Language Split
**Date:** April 11, 2026
**Status:** Decided

**Decided:** Python orchestrator + C++ PC Agent, communicating over a custom local protocol (TCP socket or named pipe exact transport TBD in Phase 2). Phase 0 stays Python-only; the C++ PC Agent enters in Phase 1 or 2 after the Python side is stable.

**Alternatives considered:**
- Python-only (rejected underdelivers on Systems/Network resume signal)
- Python orchestrator + C# PC Agent (rejected C# isn't on the career path)

**Reasoning:** Builder is targeting Systems/Network programmer roles. Multi-process architecture with a custom protocol gives the strongest possible signal to recruiters in those domains: process boundaries, IPC, sockets, framing, lifecycle management. Python is retained for the orchestrator because its ecosystem (Pydantic, async HTTP, JSON) is best-in-class for intent routing. Sequencing safeguard: Phase 0 stays Python-only to prevent learning overload at project start.

---

## Decision 2: Python Framework
**Date:** April 11, 2026
**Status:** Decided

**Decided:** Python's stdlib `cmd` module for the REPL loop + Pydantic for input validation and tool schemas.

**Alternatives considered:**
- Typer + prompt_toolkit (rejected: hides too much framework machinery, wrong shape for free-form string input)
- Click alone (rejected: same shape problem, decorator-heavy)

**Reasoning:** ATLAS's actual shape is "free-form string in → parse → validate → dispatch → respond." That's the same shape voice input will produce later, so writing the parser by hand means one code path serves both typed and voice input with no rewrite when voice arrives. Pydantic earns its place because every tool will need input validation. The extra ~1 hour upfront cost (vs Typer) buys real understanding of REPL mechanics, input parsing, and validation all transferable to systems work.

---

## Decision 3: Project Structure
**Date:** April 11, 2026
**Status:** Decided

**Decided:** Single monorepo with three top-level component folders: `orchestrator/` (Python), `pc_agent/` (C++, deferred to Phase 1/2), and `shared/` (protocol spec, shared schemas, cross-component contracts). Plus standard top-level files: `docs/`, `DECISIONS.md`, `PROJECT_STATE.md`, `README.md`.

**Alternatives considered:**
- Flat by component without `shared/` (rejected: pushes the protocol into one side, implying ownership asymmetry)
- Flat by layer with mixed-language `src/` and `tests/` (rejected: fights every IDE and build tool)

**Reasoning:** The protocol between orchestrator and PC Agent is the highest-value artifact for the builder's Systems/Network career goals. A dedicated `shared/` folder makes the contract first-class, prevents version skew, and signals architectural maturity. Component-based top-level layout keeps each language self-contained with its own build system, dependencies, and tests.

---

## Decision 4: Dev Environment (Python tooling + IDE)
**Date:** April 11, 2026
**Status:** Decided

**Decided:**
- **Python tooling:** Ruff (linter + formatter) + mypy (type checker), both integrated into PyCharm via official plugins, configured to run on save.
- **Python IDE:** PyCharm Community Edition.
- **C++ IDE (Phase 1+):** Visual Studio 2026 Community.

**Alternatives considered:**
- Black + Flake8 + mypy (rejected: three tools where two would do, slower, older generation)
- VS Code for both languages (rejected: JetBrains muscle memory transfers cleanly to PyCharm; VS Code's Win32 C++ debugger is weaker than Visual Studio's)
- Rider for C++ (rejected: Rider's C++ support is Unreal-focused, not Win32 systems-focused)

**Reasoning:** Ruff combines linting and formatting in one Rust binary that runs in milliseconds, ensuring fast feedback that actually gets used on every save. One tool means one config and less cognitive load. Ruff is becoming the Python ecosystem standard. PyCharm gives JetBrains muscle-memory transfer from Rider plus first-class Python tooling. VS 2026 was chosen for C++ based on the builder's correct observation that VS provides more configurability and control than Rider, exactly the philosophy that aligns with systems work.

---

## Decision 5: Testing Framework
**Date:** April 11, 2026
**Status:** Decided

**Decided:** pytest as the testing framework. Tests live in `orchestrator/tests/` mirroring the source layout. Plugin ecosystem (`pytest-cov`, `pytest-mock`, `pytest-asyncio`) added when specific phases require them.

**Alternatives considered:**
- `unittest` (rejected: class-based ceremony, mediocre failure messages, no longer the industry standard)

**Reasoning:** pytest's function-based syntax and assertion introspection produce dramatically clearer tests and failure messages, both of which matter for a learner who will write hundreds of tests. It is the industry default across every major Python project. pytest can also run unittest-style tests, so the choice is non-exclusive.

---

## Decision 6: Version Control Workflow
**Date:** April 11, 2026
**Status:** Decided

**Decided:** GitHub Flow workflow, `main` is the always-stable timeline, all new work happens on feature branches (`feature/*`, `phase/*`), branches merge into `main` only when working and tested. Phase 0 setup commits go directly to `main` as a soft on-ramp; feature-branch discipline begins once real tool code starts. `.gitignore` will be a standard Python + C++ + Windows + JetBrains + Visual Studio template, prepared in Phase 0.

**Alternatives considered:**
- main-only, no branches (rejected: no safety net for experiments, does not teach professional workflow)
- GitFlow (rejected: designed for large teams shipping versioned releases, massively overkill for solo project)

**Reasoning:** GitHub Flow is the industry default for small teams and solo developers. It teaches the exact workflow encountered in professional environments. The safety net is valuable even for solo development. Phase boundaries map naturally to feature branches, producing a clean recruiter-legible commit history.

---

## Decision 7: Dependency Management
**Date:** April 11, 2026
**Status:** Decided

**Decided:** uv as the unified Python dependency manager, virtual environment manager, and project initialization tool. Project metadata, dependencies, and tool configs (Ruff, mypy, pytest) all consolidated in `orchestrator/pyproject.toml`. uv-managed `.venv` (gitignored). `uv.lock` committed for reproducible installs.

**Alternatives considered:**
- pip + requirements.txt + venv (rejected: older toolchain, no real lock file, slower, requires manual venv activation)
- Poetry (rejected: good but uv has surpassed it in speed, ergonomics, and ecosystem momentum)

**Reasoning:** Toolchain consistency with Ruff (same vendor, Astral). Significant speed advantage over pip changes behavior, fast tools get used habitually. Automatic venv management removes a class of beginner errors. Single `pyproject.toml` consolidates project metadata and all tool configs in one place. Real lock file (`uv.lock`) provides reproducibility. Builder has committed to learning uv from scratch with support throughout.

---

## Decision 8: Project Identity and Scope
**Date:** June 19, 2026
**Status:** Decided

**Decided:** ATLAS is, and remains, a local-first personal assistant that each user runs on their own machine. It is not, and will not become, a hosted service, product, or company. It is open source and extensible: the core ships, and users write their own agents and wire them in without modifying the core. The project is deliberately positioned as both a Systems/Network portfolio piece and an AI product, through one synthesis: the orchestration is the portfolio, the agents are the demo that proves it is real and general.

**Alternatives considered:**
- ATLAS as a hosted service/product with users and a backend (rejected: not the goal, adds operational scope, abandons the local-first stance)
- ATLAS as a fixed assistant with only the author's agents, not extensible (rejected: the ceiling is the author's own time, the "platform" claim is unearned, and agents like Poseidon are useless to users who do not need them and cannot be swapped out)
- Pure systems piece with no AI, or pure AI product with no systems depth (rejected: the builder's targets and interests span both, and the synthesis keeps both without fracturing the identity)

**Reasoning:** "Extensible open-source assistant" captures the intent precisely and drops the company connotation the word "platform" carried. The domains-as-demo framing lets the AI ambition ride on top of the systems work instead of competing with it. Framing line carried forward: ATLAS is a multi-process agent-orchestration assistant with a custom protocol, shown working across finance, IoT, news, and weather.

---

## Decision 9: Three-Boundary Architecture with a Tool Registry Core
**Date:** June 19, 2026
**Status:** Decided

**Decided:** The orchestrator exposes a single Tool registry. Every capability is a Tool behind one interface, regardless of where the work happens. Three boundaries hang off the registry:
- **Boundary A (outbound, owned):** hand-written custom binary protocol to native agents and processes the builder controls (PC Agent, Poseidon controller).
- **Boundary B (outbound, external):** an adapter layer that binds any external REST API to a custom command. The builder's own adapter and manifest design.
- **Boundary C (inbound):** a command surface accepting input from a remote network client now, and voice later.

**Alternatives considered:**
- A single protocol that handles both owned agents and external APIs (rejected: category error. An owned protocol is a wire you serve and control on both ends; an external API is one you consume and control on neither. One format cannot be both.)
- No registry, agents wired directly to the orchestrator (rejected: loses the unifying abstraction that makes the system extensible; every agent becomes bespoke)
- Adopting MCP for Boundary B instead of an own design (rejected for this project: building the thing MCP standardizes is the point for a systems portfolio. MCP is known and deliberately not adopted; it also concerns only Boundary B and never competed with the Boundary A protocol.)

**Reasoning:** The Tool registry is the seam the entire system hangs from. From the orchestrator's view, "water the plants" (Boundary A) and "refresh the race" (Boundary B) are both Tools; one Tool's `execute()` speaks the binary protocol, another speaks HTTP, and the registry does not care. That indifference is what makes ATLAS extensible. Boundary C was named explicitly because the remote control surface and voice are both inbound command sources and need one clean place to arrive. The Tool base class (Phase 0, Step 5) is the concrete contract every boundary plugs into.

---

## Decision 10: Agent Set (Final)
**Date:** June 19, 2026
**Status:** Decided

**Decided:** Four named agents, final:
- **Plutus (finance):** expense tracking, categorization, monthly report with charts by sector, and personal cashflow and savings forecasting. Market data surfaced as information only.
- **Poseidon (IoT):** plant watering on the builder's own ESP32/Arduino controller with own firmware, commanded over the network.
- **Athena (news):** personalized news from APIs and RSS, summarized and scheduled, kept decoupled and consumed through the standard tool interface.
- **Zeus (weather):** voice-driven. Fetches and elaborately reads back current conditions and the official forecast, including rain/snow probabilities for dates inside the forecast window, reported honestly with their uncertainty. Built on top of the existing weather tool, not a duplicate of it.

**Alternatives considered:**
- Integrating with the landlord's existing closed watering device (rejected: consumer device with no open API; building an own controller is more impressive and fully owned)
- Wiring Athena directly into Plutus (rejected: Plutus consumes Athena's output through the standard tool interface instead, which demonstrates the abstraction works)
- A second, separate weather implementation for Zeus (rejected: Zeus wraps the existing weather tool; agent-on-top-of-tool layering is the intended pattern)

**Reasoning:** The four agents span four industries (FinTech, AgriTech, News, Weather) and exercise different parts of the architecture (embedded plus protocol, data plus ML, web plus LLM, voice plus external API), which is what proves the system is general rather than single-purpose.

---

## Decision 11: Plugin / Agent SDK with Manifest Format
**Date:** June 19, 2026
**Status:** Decided

**Decided:** ATLAS will provide an agent SDK: a declarative manifest format (commands, input schema, sensitivity, provider) plus a loader that discovers and registers agents at runtime, so the builder or any third party can write an agent and wire it in without modifying ATLAS core. Sequencing is fixed: build the first agents directly and by hand, observe what repeats, then extract the SDK from the common parts. The SDK is built after the first agents, never before.

**Alternatives considered:**
- Designing the SDK, manifest, and loader first, then writing agents against it (rejected: you cannot design a good contract for agents never written; it would produce an abstraction that fits nothing)

**Reasoning:** The SDK is the centerpiece that earns the word "extensible." It is the feature the other infrastructure features exist to support. The build-agents-before-SDK sequencing follows the standard systems practice of harvesting an abstraction from working code rather than front-loading it. Being able to explain this reasoning is itself a strong signal.

---

## Decision 12: Capability-Based Permission Model
**Date:** June 19, 2026
**Status:** Decided

**Decided:** Beyond the app and directory allowlists, each agent declares the capabilities it is permitted to use, and the orchestrator enforces those declarations on every tool call. No agent escalates silently.

**Alternatives considered:**
- Relying on the app/directory allowlists alone (rejected: insufficient once agents come from outside the author)

**Reasoning:** The moment third parties can write agents, the core cannot assume agent code is well-behaved or safe. The capability model is the boundary standing between an untrusted third-party agent and the user's machine. It also reads as security maturity and makes local-first a deliberate design position rather than a slogan.

---

## Decision 13: Platform Infrastructure Feature Set
**Date:** June 19, 2026
**Status:** Decided

**Decided:** The following infrastructure features are in scope, placed by boundary:
- **Boundary A:** protocol inspector (live view of frames on the custom protocol), process supervision with real metrics (heartbeats, restart-on-crash, latency and error stats), service discovery (LAN node discovery instead of hardcoded IPs).
- **Boundary B:** circuit breaker (failing external providers fail fast and recover).
- **Boundary C / core:** remote control surface (authenticated command input from phone or another LAN machine), scheduler / trigger subsystem (run tools on a time or an event; powers Poseidon's schedule and Athena's morning send through one mechanism).

**Alternatives considered:** none recorded; selected from the brainstorm as the highest-signal infrastructure for the builder's target roles.

**Reasoning:** Each feature deepens the system itself so every future agent rides on it for free. The protocol inspector doubles as the bridge to graphics work later. These are Phase 3 and later concerns, surfaced now so foundational decisions leave room for them.

---

## Decision 14: Voice / Keyboard Independence
**Date:** June 19, 2026
**Status:** Decided

**Decided:** Voice is the eventual primary input and enters through Boundary C. The builder will implement the audio capture and streaming layer themselves rather than only sending audio to a cloud STT endpoint. Typed input works from day one and remains the permanent fallback.

**Alternatives considered:**
- Cloud STT only, no self-built capture/streaming (rejected: identical UX but thin systems signal; the capture and streaming path is exactly the threading and real-time work the builder wants)

**Reasoning:** The self-built capture and streaming layer is where the threading and networking learning pays off and where the original C++ ambition legitimately lives. Keeping typed input as a permanent fallback protects daily usability.

---

## Decision 15: Prediction Stance (Surface, Do Not Predict)
**Date:** June 19, 2026
**Status:** Decided

**Decided:** ATLAS surfaces forecasts and market data as information the user acts on. It does not build prediction models for weather or markets. Plutus presents market data, never buy/sell recommendations and never auto-trades. Zeus reads back the official forecast and its probabilities honestly and never claims precise prediction. ML and statistics effort is pointed at Plutus's personal-spending forecasting, where the signal genuinely lives in the available data.

**Alternatives considered:**
- An ML model to predict equity prices (rejected: markets are near-efficient, past prices do not predict future prices, and it is also regulated investment-adviser territory)
- An ML model to predict local weather from historical/statistical data (rejected: the atmosphere is chaotic, local history does not contain the determining signal, and the result would underperform the free API, which is already the output of institutional-scale ML)

**Reasoning:** These three (market prediction, precise weather prediction, and "ML on weather statistics") are one lesson: some problems resist prediction because the future is not determined by the obtainable data, not because insufficient ML was applied. Shipping a model that underperforms its own data source is a negative portfolio signal. Personal spending is predictable from personal history, so that is where the ML belongs. This reasoning is worth defending in front of the CEO.

---

## Decision 16: Vision Feature Deferred
**Date:** June 19, 2026
**Status:** Deferred

**Decided:** The camera object-identification feature ("what am I holding") is deferred to a later optional showpiece, after the core system and the four agents exist.

**Alternatives considered:**
- Building it early as a flagship demo (rejected: it is downstream of the core, the lowest engineering signal on the list because the hard part lives inside the model, and the reference repo `jarvis-mlx` is MLX and Apple-Silicon only, so it does not transfer to Windows)

**Reasoning:** It depends on the foundation; the foundation does not depend on it. Flashy but shallow features belong at the end of the build order. Its priority may rise if a specific demo context calls for it, but it always comes after the core.

---

## Decision 17: Language Split Refinement (extends Decision 1)
**Date:** June 19, 2026
**Status:** Decided (layer-based split). Ratio mandate OPEN, pending builder decision.

**Decided:** The language split is by layer, not by an imposed percentage. Systems and infrastructure (custom protocol, framing, process supervision, service discovery, PC Agent, inspector internals) is C++. Agents, AI/LLM, and data/ML work (Plutus, Athena, Zeus, the web/JSON/HTTP inside Athena and Zeus, the pandas/scikit-learn inside Plutus) is Python. They communicate over the custom protocol. The resulting C++ to Python ratio is whatever this layering produces, and it may grow toward C++ as the systems layer grows.

**OPEN item:** The builder is weighing an explicit 80% C++ / 20% Python mandate across the whole system. Analysis recorded for the decision: forcing C++ into the agent/AI/data layer breaks because that layer is made of Python-shaped problems (no pandas, no scikit-learn, immature HTTP/JSON, no AI ecosystem, and a slow edit-compile loop precisely where iteration is most frequent), which multiplies the cost of the agents that are ATLAS's reason to exist and makes the ML the builder wants to learn harder rather than richer. The systems core in C++ is fine and arguably better. The path to a C++-dominant project without the wreckage is to expand the C++ systems layer, not to force Python-shaped agents into C++. The builder will decide; if 80/20 is chosen, this entry is updated to reflect the override and its accepted consequences.

**Alternatives considered:**
- 80/20 C++ by mandate across all layers (under consideration; analysis above)
- Python-only (already rejected in Decision 1)
- C# agent layer (already rejected in Decision 1)

**Reasoning:** Language should follow the shape of the problem. Most agent work is data, web, and AI, which is Python's home turf; most infrastructure work is low-level and protocol-bound, which is C++'s. A layer-based split lets each part use the right tool and keeps the learning sequenced (one wall at a time) instead of stacking Python-ecosystem learning, heavy C++, networking and threading, and AI-without-ecosystem all at once.

---

## Decision 18: License
**Date:** June 19, 2026
**Status:** Decided

**Decided:** MIT License. ATLAS is released as open source under MIT: anyone may use, modify, and build on it, including in closed or commercial products, with the only obligation being attribution. A `LICENSE` file containing the MIT text will be added to the repo root, and the README license field (currently TBD) updated to "MIT."

**Alternatives considered:**
- Apache 2.0 (rejected for now: excellent and adds explicit patent protection, but more formal than this project needs; MIT's simplicity is the better fit and the more recognizable signal for a personal portfolio project)
- GPL / copyleft (rejected: its purpose is to force downstream versions to stay open, which reduces adoption and can forbid commercial or company use. The goal here is maximum adoption and portfolio signal, the opposite of what copyleft optimizes for. It could also complicate a future closed product the builder might build on their own code.)

**Reasoning:** The goal for ATLAS is adoption and portfolio signal, and permissive licensing maximizes both by letting the maximum number of people use it with zero friction; every user is distribution and evidence the design is good. MIT is the recognized default for this kind of project, short and readable, and signals ecosystem fluency to a hiring engineer or a CEO. It also keeps every future door open, including the builder's own option to later build a separate narrow commercial product, since permissive licensing leaves the author unrestricted. Selling ATLAS itself is explicitly not the path (see Decision 8); any future commercial effort would be a separate closed product, not ATLAS, which remains open under MIT.

---

## Decision 19: Agent Model (LLM Planner Above Deterministic Tools)
**Date:** August 6, 2026
**Status:** Provisional (detailed at agent-layer planning)

**Decided:** ATLAS agents (Athena, Zeus, Plutus, Poseidon) are implemented as an
LLM planner layer that sits *above* the deterministic tool registry, not as LLMs
embedded inside individual tools. The LLM perceives intent, decomposes goals,
decides, and chains tool calls across multi-step workflows. The tools it calls
stay single-purpose, deterministic, and independently testable.

Autonomy is scoped by the existing security policy: the planner may chain freely
over `none`-sensitivity tools (fetch, calculate, read, summarize) without per-step
human oversight. The moment a plan reaches a `confirm` / `PIN` tool, the existing
human-in-the-loop gate fires. Full autonomy through a sensitive action is never a
default; it would be a deliberate per-tool decision.

LLM hosting: local self-hosted model, always-on, co-located with the orchestrator
on the home server. Provisional; hosting details, model choice, and the
optional-vs-mandatory question (given ATLAS's "users run it themselves" identity)
are deferred to agent-layer planning.

**Alternatives considered:**
- LLM baked into each tool (rejected: destroys deterministic input/output
  contracts and pytest-ability; breaks the security gates, since "preview before
  send" becomes "preview whatever the model decided"; multiplies the inference
  dependency across every tool).
- Fully autonomous agent with no human gate on sensitive actions (rejected:
  direct conflict with Decision 2's "ATLAS never guesses" spine and the security
  policy's confirm/PIN/dry-run design).

**Reasoning:** The target behavior is a genuine autonomous agent (perceive,
decompose, decide, use tools, multi-step). Planner-above-tools is the only
architecture that delivers that without tearing up Decision 2 and the security
policy. It also matches ATLAS's existing intent-router-plus-tool-runner identity:
the LLM upgrades the top-level router rather than adding a new subsystem. This
reinforces an existing design instinct: every tool, including the Phase 1 four,
should stay a clean deterministic unit with a well-defined schema, because an LLM
planner will be the thing calling them later.

**Impact on Phase 1:** None. The `news` and `weather` tools remain dumb fetch
primitives. This entry only pins the reconciliation so it isn't rediscovered later.

---

## Decision 20: Phase 1 HTTP Client, Providers, Teaching Depth
**Date:** August 6, 2026
**Status:** Decided

**Decided:**
- HTTP client: `httpx`. Chosen with the governance situation acknowledged
  (issues/discussions closed Feb 2026; HTTPX2 stewardship split under Pydantic
  Services). Accepted trade-off: partial loss of the GitHub-issues escape hatch,
  in exchange for async-readiness that transfers to later phases.
- Weather provider: Open-Meteo (keyless). News provider: key-based (exact
  provider confirmed at wiring time). Pairing chosen deliberately to teach both
  the no-auth and .env-credential auth paths in one phase.
- Teaching depth for Phase 1 networking: full bottom-up, starting from sockets
  and bytes-on-the-wire, building up to HTTP/REST. Foundation intended to
  transfer directly to the C++ PC Agent's TCP work in Phase 2.

**Reasoning:** Builder is entering networking for the first time in any language
and asked for beginner-to-intermediate depth with nothing skipped. Bottom-up is
the higher-upfront-cost path but avoids the shallow-mental-model failure where
HTTP is treated as magic; it also pre-loads the Phase 2 socket work.

---

## Decision 21: Config Layer (pydantic-settings, optional secrets, tool-level enforcement)
**Date:** August 6, 2026
**Status:** Decided (amended by D30)

**Decided:** Config is a `Settings(BaseSettings)` class from `pydantic-settings`,
instantiated once at startup. Secret fields (e.g. NEWS_API_KEY) are OPTIONAL at
the config layer (`str | None`), so ATLAS boots without them. Each tool that
needs a credential asserts its own key at tool load/registration and fails fast
with a specific message ("news tool disabled: NEWS_API_KEY not set in .env") if
absent. Config validation (type/required) still fails fast at startup for any
genuinely required field.

**Alternatives considered:**
- News key required at config layer (rejected: hard-blocks weather-only/clone
  users from booting ATLAS at all; contradicts "users run it themselves"
  identity).
- Plain os.getenv module-level (rejected: no typing, no validation, no
  fail-fast; earlier Shape A).

**Reasoning:** Optional-at-config + enforce-at-tool gives fail-fast clarity at
the tool boundary without collateral app-wide lockout. Matches tool-independence
principle: a tool owns its own credential requirement.

**Amended by D30:** the "at tool load/registration" wording above is superseded.
Enforcement happens inside `_execute`, at the tool boundary. See D30.

---

## Decision 22: Advanced calculate (ENTRY MISSING)
**Date:** unknown
**Status:** Number in use, entry absent

D22 is referenced by Decision 24 ("Advanced-calculate (D22) and vision (D23) are
published as 'future vision' on the site") but no entry for it exists in this
file. Either it was never written or it was lost, the same way D27 and D28 were
lost until they were backfilled on 2026-10-05.

What is recoverable from the D24 reference: D22 concerns an advanced or extended
version of the `calculate` tool, parked as future-vision material and explicitly
NOT built for v1.

TODO: reconstruct the full entry from the original discussion, or retire the
number and amend D24's reference. Recorded so the gap is visible rather than
looking like a numbering skip.

---

## Decision 23: Deferred Capstone Capabilities (roadmap, not yet planned)
**Date:** August 6, 2026
**Status:** Parked — revisit only when ATLAS is mature and all currently-planned
phases are achieved. No design or implementation until then.

**Captured directions (builder-set):**
1. NFC-triggered mic wake. Microphone is NOT always-on; scanning an NFC tag wakes
   ATLAS to listen. NFC hardware acquired with the Raspberry Pi. Rationale:
   privacy/control, explicit physical wake gesture, no passive listening.
2. Voice output (TTS). ATLAS speaks results back, enabling screen-independent use
   (e.g. "what is 10+10" -> spoken "twenty"). Reinforces the clean/structured/
   speakable tool-output constraint.
3. Vision ("eyes"). ATLAS connects to cameras to see and interpret the physical
   world (e.g. identify a circuit board held up to the camera, explain it, answer
   by voice), using a multimodal LLM plus research ability. Capstone-tier;
   depends on LLM planner + voice output. (Ref: huwprosser Jarvis example in
   ATLAS_Discussion.md.)

**Reasoning:** These define ATLAS's end-state vision (voice-first, screen-optional,
multimodal assistant). Recorded now so the vision is on the record and current
phases can be built with it in mind, without pulling any of it into present scope.

---

## Decision 24: v1 Scope Boundary + NFC Placement
**Date:** August 6, 2026
**Status:** Decided (builder-set)

**Decided:**
- v1 (first PUBLIC release) includes: the four Phase-1 tools, C++ PC Agent, LLM
  planner, all four agents (Plutus, Poseidon, Athena, Zeus), voice input+output,
  and NFC-triggered mic wake. NFC is IN v1 (privacy-critical, non-negotiable).
- Beta = internal-only pre-agent build (just the builder). Public advertising +
  ATLAS website begin at beta. Advanced-calculate (D22) and vision (D23) are
  published as "future vision" on the site, discussed in depth at that milestone,
  NOT built for v1.
- NFC wake is built during the voice/Pi hardware phase (same milestone as the
  Pi purchase: typed workflow stable, PC Agent reliable), NOT squeezed into
  Phase 1, because it is hardware-gated. It remains a v1 requirement, not a
  post-v1 add-on.

**Reasoning:** Keeps hardware-dependent work out of the current Python-only
phases while guaranteeing NFC lands before public release. Existing macro roadmap
stands; only tweak is recording NFC as a v1-required item in the voice/Pi phase.
Per-tool roadmaps (calculate, NFC, vision, etc.) designed at the start of each
tool's build, not now.

---

## Decision 25: Docstring Convention (reST/Sphinx style)
**Date:** August 6, 2026
**Status:** Decided

**Decided:** ATLAS uses reStructuredText/Sphinx-style docstrings project-wide.
Format: :param:, :returns:, :raises:. Type information is NOT duplicated in the
docstring (no :type:/:rtype:); types live in the function signature via type
hints, which are authoritative (mypy reads them). Docstrings document intent and
behavior; signatures document types.

Standing rule (added to project instructions): all code written from this point
carries appropriate documentation — reST docstrings on functions/classes, plus
inline comments explaining WHY for non-obvious or security-critical code. When a
new API/library is introduced, official docs are linked alongside the explanation.

**Alternatives considered:**
- NumPy style (rejected: builder preferred reST's compactness; reST is
  Sphinx-native and faster to write).
- Blend of reST + NumPy (rejected: they are distinct machine-parseable formats;
  blending breaks doc tooling and IDE rendering).
- Google style (rejected earlier in favor of the two type-explicit styles).

**Reasoning:** reST is compact, fast to write, and Sphinx-native for future
generated docs. Dropping :type:/:rtype: avoids type info drifting out of sync
with the actual hints.

---

## Decision 26: time Tool Scope (local now, timezones later)
**Date:** August 11, 2026
**Status:** Decided

**Decided:** Phase 1 `time` tool returns current LOCAL time only, no input.
Timezone support (e.g. "time in India", cross-zone difference) deferred to a
later enhancement. When added, the tool returns deterministic times for named
zones (via zoneinfo); cross-zone analysis ("how many hours difference") is the
LLM planner's job on top of the tool, not the tool's. Consistent with D19
(planner above deterministic tools).

**Reasoning:** Keeps Step 4 focused on the minimal-input tool pattern without
dragging in zoneinfo, zone-name validation, and error handling. Timezone
reasoning is a natural agent-layer capability once the LLM planner exists.

---

## D27 — Geocoding disambiguation: pre-qualify plus visible resolution
**Date:** September 2026 (exact date from the Step 7 Part 2 commit)
**Status:** Decided

**Context:** `geocode()` hits the Open-Meteo geocoding search endpoint with
`count=5` and returns a single best match. Place names are ambiguous.
"Vancouver" is both BC and Washington State. The tool has no way to know which
one the user meant.

**Decided:** Two mechanisms, neither of them interactive.

1. **User pre-qualification.** The whole argument is treated as the place name,
   so the user can type "vancouver, united states" and let the provider's own
   ranking disambiguate. No splitting on whitespace, no argument-count check.
2. **Show what was resolved.** `do_weather` prints a resolved-place header
   built from the returned `GeocodeResult` before the weather itself. Parts
   list skips `None` fields and joins with ", ". A wrong match is therefore
   always visible rather than silent.

**Rejected: an interactive picker** ("did you mean 1, 2, or 3?"). Two reasons:

- It puts conversational state in the tool layer, which fights D19. Judgment
  and multi-turn context belong to the planner above the registry, not to a
  deterministic tool.
- It fights `cmd.Cmd`'s one-input-one-output model. A picker needs a second
  prompt-and-read cycle inside a single `do_*` call.

**Implementation note:** the header is built in `do_weather`, NOT inside the
weather tool. The tool stays a pure coordinates-in unit, so Step 7 Part 1 was
reused completely unchanged when Part 2 added geocoding. Presentation belongs
to the REPL layer.

**Verified live:** "vancouver, united states" correctly resolved to WA rather
than BC, proving the pre-qualification path works without any tool-side logic.

---

## D28 — Fuzzy-match resolution belongs to the planner
**Date:** September 2026 (exact date from the Step 7 Part 2 commit)
**Status:** Decided

**Context:** D27 makes a wrong geocoding match visible, but does not make it
correct. Trigger case: "sevasi" resolved to Şenyuva, Türkiye. The provider
returned a confident, plausible, wrong answer. Because of D27's header the
error was visible, but nothing in the tool layer could have caught it.

**Decided:** `geocode()` stays deterministic: best-match-or-`None`, no
heuristics, no scoring, no second-guessing the provider. Detecting a
wrong-but-plausible match is the future LLM planner's job.

**Reasoning:** knowing that "sevasi" is more likely a locality in Gujarat than
a village in Türkiye requires world knowledge plus conversational context
(where the user is, what they were just talking about). That is exactly the
class of judgment D19 assigns to the planner. Any tool-side attempt would be a
pile of heuristics that is wrong in a different set of cases.

**Consequence for the planner-era tool:** it will expose **all** `count=5`
matches, not just `[0]`, so the planner can choose using context. `geocode()`
already requests `count=5`; only the first result is consumed today. The data
is already on the wire, so this is an interface change, not a new API call.

**Pairing:** D27 and D28 are one decision split in two. D27 decides that wrong
matches are made visible. D28 decides who is responsible for fixing them.

---

## D29 — News source strategy
**Date:** September 10, 2026
**Status:** Decided (amended 2026-09-20, below)

**Decided:** Four-source strategy for the eventual aggregation pipeline, but
Step 8 builds GNews only.

- **GNews** — ranking and description text. Keyed (`apikey` query param).
  Free tier: 100 req/day, 10 articles/request, ~1 req/sec, resets 00:00 UTC,
  truncated content, development/testing only and non-commercial.
- **GDELT** — volume source. Keyless, full-text search across 65+ languages,
  rolling 3-month window, 8 metadata fields, no article body. Own step later.
- **RSS** — curated third source. No key, no quota, no terms problem.
  Coverage only as good as the hand-maintained feed list.
- **NewsAPI.ai** — EXCLUDED as an ingestion source. See below.

**Why GNews first:** Step 8's teaching purpose is the credentialed HTTP path
(D20 pairing: weather taught keyless, news teaches auth). GDELT is keyless, so
building it first would leave three keyless calls and zero keyed ones. GNews
also has the simpler response shape of the two.

**Why NewsAPI.ai is excluded as a source:**

1. Free tier is a one-time allowance (~2,000 tokens / 30 days), not a recurring
   quota. Sources conflict (one claims 2,000 results/day) but the vendor's own
   SDK docs say one-time. A source that runs dry permanently is worse than no
   source, because it passes testing and dies silently later.
2. It already performs deduplication, event clustering, entity linking, and
   returns full article text plus summaries. That is stages 2, 3, 6, and 7 of
   the planned pipeline. Ingesting it means either discarding that work or
   building a pipeline whose output is worse than one of its inputs.

**Instead:** the one-time token allowance is reserved as an evaluation oracle.
Run a fixed article batch through our clustering and through NewsAPI.ai's event
endpoint, compare. This gives ground truth for tuning the similarity threshold,
which is otherwise the hardest parameter in the system to pick. Recorded as
deferred item A11.

**Rate-limit consequence:** GNews at 100 req/day (4/hour) cannot be the polling
workhorse. GDELT (paced ~1 req/5 sec, no hard documented quota) is. This is the
functional justification for pairing them.

**Alternatives considered:** Guardian Open Platform (free, production-safe,
returns full text, but single-publisher). NewsData.io and Currents (commercial
use permitted on free tier, but metadata only and delayed). Rejected in favour
of the GDELT+GNews split, which covers both volume and ranking.

---

## D29 amendment
**Date:** September 20, 2026
**Status:** Amends D29

GNews free-tier delay is CONFIRMED at 12 hours, reported by the API itself in
`information.realTimeArticles` on every response. This resolves the conflicting
third-party reports noted when D29 was written. Consequence: GNews cannot serve
a real-time feed, which strengthens the case for GDELT as the volume source.

---

## D30 — Credential guard placement
**Date:** September 10, 2026
**Status:** Decided

**Decided:** Enforce required credentials inside `_execute`, at the tool
boundary. Missing key returns an ordinary tool output string
("news disabled: NEWS_API_KEY not set in .env"). The tool still constructs,
still registers, still appears as a known command. It just refuses to work.

**Amends D21.** D21's wording said "asserts its own key at tool load/
registration." That wording is superseded. Enforcement is at the tool
boundary, not at load or registration time.

**Alternatives considered:**

- Raise in `__init__`. Rejected: the composition root registers
  unconditionally, so a missing key would crash startup, contradicting D21's
  own "ATLAS boots without them."
- Raise in `__init__` plus conditional registration in the composition root.
  Cleanest separation, rejected because `news` would then not be a known
  command at all, so the user gets `*** Unknown syntax: news` instead of a
  message explaining what is wrong.

**Cost accepted:** the check runs on every call. It is a null check.

**Secondary benefit:** the guard is also the mypy narrowing construct.
`settings.news_api_key` is `str | None`; the early return proves it is `str`
on every line after it.

**Implementation note:** the guard tests falsiness (`if not key`), not
`is None`. A `.env` line of `NEWS_API_KEY=""` yields an empty string, not
`None`, and an identity check would let it through to the wire as `apikey=`.
"Not configured" means falsy.

---

## D31 — Secret redaction at the logging layer
**Date:** September 20, 2026
**Status:** Decided

**Context:** GNews carries credentials as a query parameter, so every httpx
INFO request line contains the key. It appeared in terminal scrollback and was
written to `atlas.log` by the DEBUG file handler. It also leaked into two chat
pastes during development, which is the evidence that manual redaction does not
work as a practice.

**Decided:** A `RedactSecrets(logging.Filter)` in `logging_config.py`,
initialised from the shared `Settings` instance, attached to BOTH handlers.
Replaces any known secret value with `***REDACTED***`.

**Rejected: silencing the httpx logger** (setting it to WARNING). Would have
removed the request line entirely. That line caught both Step 7 Part 1 bugs and
is the primary debugging tool for wire-level work, so discarding it to solve a
redaction problem is the wrong trade.

**Rejected: keeping the key out of the URL.** Not available. GNews requires
query-param auth.

**Two implementation facts worth recording:**

1. The filter is attached to HANDLERS, not to the root logger. `callHandlers`
   walks ancestor loggers invoking their handlers, NOT their filters. A filter
   on root would never see a record originating from the `httpx` logger.
2. httpx logs with lazy `%`-style formatting, so the URL is in `record.args`,
   not `record.msg`. Mutating `msg` alone does nothing. The filter handles
   both, and converts args via `str()` because httpx passes an `httpx.URL`
   object rather than a string.

**Design property:** the secret is read from settings, not hardcoded, so key
rotation requires no filter change. The constructor takes an iterable, so a
second keyed provider is one more list entry rather than a second mechanism.

---

## D32 — Single shared Settings instance
**Date:** September 20, 2026
**Status:** Decided

**Decided:** `Settings()` is constructed exactly once, at module level in
`config.py`. Every module imports that instance. No module constructs its own.

**Trigger:** `gnews.py` was building `configurations = Settings()`, producing a
second independent instance. The redaction filter was initialised from
`config.py`'s instance while the tool read its own. They agreed only by
coincidence, and a divergence would have meant the filter redacting a string
the tool was not sending, leaking the key silently.

**Applied project-wide**, not just to `gnews.py`.

---

## D33 — Validation strictness is project-wide, via model config
**Date:** September 20, 2026
**Status:** Decided

**Decided:** input models set `model_config = ConfigDict(strict=True,
str_strip_whitespace=True)` at the class level rather than repeating
constraints per field.

**Reasoning:** per-field `strict=True` produced an asymmetry (strict `topic`,
coercive `count`) that reads as accidental. Class-level config applies to
fields added later and scales to the models still to come (canonical
`Article`, `GdeltInput`).

**Verified behaviour**, previously assumed without evidence:

- `str_strip_whitespace` DOES fire under `strict=True`. Stripping transforms a
  value that is already a valid `str`; strict mode governs coercion. They
  compose.
- Config-level `strict` reaches every field, confirmed with `count="5"`
  raising rather than coercing.

**Note:** on the REPL path, `cmd.Cmd` strips the argument before `do_news` sees
it, so `str_strip_whitespace` currently never fires there. It still earns its
place because the D19 planner will call `.run()` directly, bypassing `cmd`.

---

## D34 — PC Agent is cross-platform
**Date:** October 5, 2026
**Status:** Decided

**Decided:** The Phase 2 C++ PC Agent targets Windows, macOS, and Linux. One
codebase, split into a portable transport layer and a platform-specific action
layer behind a single interface.

**Trigger:** the original design assumed Windows, because both dev machines
were Windows. The main machine is now a MacBook Pro, so a Windows-only agent
would be an agent the builder cannot run day to day.

**Structure:**

- **Transport layer (portable):** sockets, message framing, request/response
  loop. Needs only a thin shim for Winsock's `SOCKET` handle type and
  `WSAStartup`, or none at all if an abstraction like ASIO is used.
- **Action layer (per platform):** every tool the agent performs is a platform
  API call. A `PlatformActions` interface with `WindowsActions`,
  `MacActions`, and `LinuxActions` implementations selected at compile time.

| Action | Windows | macOS | Linux |
|---|---|---|---|
| Open URL | `ShellExecute` | `open` | `xdg-open` |
| Launch app | `CreateProcess` | `open -a` | `.desktop` lookup, or exec on `$PATH` |
| Media control | SMTC | `MPRemoteCommandCenter` | MPRIS over D-Bus |
| Window management | Win32 HWNDs | Accessibility API (needs permission) | X11 only, see below |

**Implementation order:** macOS first, because it is the machine that can be
tested. Windows second. Linux last, and possibly incompletely.

**Alternatives considered:**

- macOS only (rejected: abandons the Windows machines and the original design).
- Windows only (rejected: cannot run on the daily driver).
- Two separate agents (rejected: duplicates the transport, which is the part
  with the actual engineering value).

**Reasoning:** the abstraction costs almost nothing if designed in from the
start and is painful to retrofit. It also demonstrates a clean boundary between
portable logic and platform-specific code, which is a better portfolio signal
than either single-platform version.

**Known limitation, recorded now:** Wayland deliberately blocks global window
control as a security property. It is not a gap to work around. Any
window-management feature on Linux is X11 only, and Wayland is the default on
most current distributions. See DEFERRED.md.

---

## D35 — GUI is Tauri 2 with Rust and TypeScript
**Date:** October 5, 2026
**Status:** Decided (direction only; build deferred to Phase 3+)

**Decided:** The eventual graphical front end is Tauri 2, with a TypeScript web
frontend and a deliberately thin Rust shell.

**Layering:**

```
TypeScript UI  ──HTTP/WebSocket──>  Python orchestrator  ──>  C++ agent
      │
   Tauri (Rust)
   windowing, tray, packaging, OS integration only
```

The frontend talks to the orchestrator directly. Rust does only what a native
shell must: the window, the system tray, auto-start, global hotkeys, packaging.

**Rule:** no business logic in Rust. Logic split across Python, C++, and Rust
would mean three places to look for any bug and three languages to keep in
sync. The Rust layer stays small and purposeful.

**Prerequisite, not optional:** an orchestrator API. Today the REPL calls tools
in-process; a Tauri app is a separate process in a different language and
cannot. The orchestrator must listen on a local port (HTTP plus WebSocket).
Once it exists, the REPL becomes just another client of the API, and the
claim that "the backend does not change" becomes literally true rather than
approximately true. See DEFERRED.md.

**Alternatives considered:**

- **Flutter** (considered first, rejected): framework is production-ready for
  desktop, but costs Dart, a fourth language serving none of the builder's
  target roles. Its strongest argument, code sharing with a mobile app, does
  not apply.
- **Local web UI served by the orchestrator** (rejected as the end state, still
  viable as a first experiment): cheapest path to a modern look, zero new
  toolchain, but no native shell for tray, hotkeys, or packaging.
- **Qt Quick / QML** (rejected): keeps the backend in C++ and is strong for
  systems-role signalling, but adds QML as its own language and a heavier
  toolchain than Tauri for the same visual result.

**Reasoning:** Rust is a systems language, so the time compounds with the
builder's goals in a way Dart does not. The web frontend gives the modern look
without inventing a UI vocabulary. Binaries are 2 to 10 MB versus Flutter's
30 to 80 MB because Tauri uses the system WebView.

**Tooling note:** the visual layer may be generated with Claude Code or Codex
(components, layout, styling, state wiring), consistent with the existing
Copilot rule: single-file work and boilerplate yes, architecture and security
boundaries no. The API contract, the local-port authentication model, and the
confirmation-gate screens are designed deliberately, not generated. The
confirmation screen IS the security boundary for sensitive actions.

**Timing:** Phase 3 at the earliest, after Phase 2 establishes the protocol and
after the orchestrator API exists. Building the GUI first would mean designing
the API under UI pressure, which produces a worse API.
