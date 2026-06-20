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