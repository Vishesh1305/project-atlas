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