# ATLAS - Project State

> Live status of the ATLAS project. Updated at the end of every chat.

---

## 📍 You Are Here

**Current Phase:** Phase 0: Foundations (NOT YET STARTED)  
**Status:** Pre-Project Planning Session COMPLETE. All 7 architectural decisions made. Awaiting Phase 0 Technical Plan presentation and approval in a new chat.

**Next action:** Open a new chat. Paste/reference this file. Request the Phase 0 Technical Plan. Approve it. Begin building.

---

## ✅ Completed Work

### Pre-Project Planning Session - April 11, 2026
- All 7 architectural decisions made and recorded in `DECISIONS.md`
- High-level architecture diagram drafted (orchestrator + PC Agent + custom protocol)
- Phase roadmap drafted (Phases 0–7+)

---

## 🏗️ Architectural Summary (the locked-in stack)

- **Languages:** Python (orchestrator), C++ (PC Agent, deferred to Phase 1/2)
- **Python framework:** stdlib `cmd` + Pydantic
- **Repo layout:** monorepo with `orchestrator/`, `pc_agent/`, `shared/`, `docs/`
- **Python tooling:** Ruff (lint/format) + mypy (type check)
- **Python IDE:** PyCharm Community Edition
- **C++ IDE (later):** Visual Studio 2026 Community
- **Testing:** pytest
- **Version control:** Git + GitHub Flow (main + feature branches)
- **Dependency management:** uv
- **OS:** Windows
- **Hardware status:** No Raspberry Pi, no NAS, all hardware-dependent features mocked or deferred

See `DECISIONS.md` for full reasoning on each choice.

---

## 🗺️ Phase Roadmap (titles only)

- **Phase 0:** Foundations: repo, venv, REPL, registry, schemas, logging, stub tools
- **Phase 1:** Real local Python tools (calc, time, weather, news)
- **Phase 2:** PC Agent v1 (C++): TCP server, custom protocol, first cross-process tools
- **Phase 3:** PC Agent hardening: allowlists, reconnection, protocol versioning, audit
- **Phase 4:** Sensitive operations: confirmation gates, PIN, dry-run, calendar/Notion writes
- **Phase 5:** Communication tools: email, WhatsApp, Discord (with preview-and-confirm)
- **Phase 6:** Polish + portfolio prep: README, docs, demo, coverage, recruiter-ready
- **Phase 7+:** Hardware-dependent (Pi, NAS, voice, lights, WoL), DEFERRED

---

## 📂 Current File Tree

*Repo not yet initialized. Will be created in Phase 0 step 1.*

### Planned Phase 0 structure:

Project-Atlas/
├── orchestrator/
│   └── src/
├── pc_agent/
├── shared/
├── docs/
├── DECISIONS.md
├── PROJECT_STATE.md
└── README.md