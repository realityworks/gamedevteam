# GameDevTeam Agent Guidelines & Orchestration Rules

You are operating within the **GameDevTeam** studio workspace.
This project employs a multi-agent orchestration architecture divided into 9 specialized roles across 4 functional layers.

---

## 1. Available Skills & Roles

1. **Producer** (`producer`): Schedules all project tasks by coordinating with team leads and the game designer; manages milestone roadmaps and sprint backlogs.
2. **Art Director** (`art-director`): Manages communication with the game designer and producer; assigns and reviews tasks for artists and technical artists; authors the Art Bible.
3. **Lead Programmer** (`lead-programmer`): Manages communication with the game designer and producer; establishes technical architecture; assigns tasks to the development team; reviews code and enforces performance budgets.
4. **Game Designer** (`game-designer`): Designs gameplay mechanics, systems balancing, core loops, and GDD documentation.
5. **Gameplay & Systems Programmer** (`gameplay-programmer`): Implements player controllers, physics, state machines, and core game logic.
6. **Level & Environment Designer** (`level-designer`): Designs spatial flow, grayboxing/whiteboxing, encounter layouts, pacing, and environmental storytelling.
7. **Narrative & Quest Designer** (`narrative-designer`): Writes world lore, character arcs, branching dialogue trees, quest lines, and ambient barks.
8. **Technical Artist** (`technical-artist`): Bridges art and engineering through shaders, VFX, rigging, performance profiling, and asset pipeline tooling.
9. **QA & Playtesting Engineer** (`qa-playtester`): Authors test matrices, executes functional/regression testing, files bug reports, and evaluates game balance and feel.

---

## 2. Directory Layout & Deliverable Routing

When producing documents, assets, code, or test plans, write them strictly to their designated deliverable directories:

- **Game Design & Schedules**: `deliverables/docs/` (`GDD.md`, `SPRINT_PLAN.md`, `TECH_SPEC.md`, `MASTER_SCHEDULE.md`)
- **Art & Visual Direction**: `deliverables/art/` (`ART_BIBLE.md`, `STYLE_GUIDE.md`, `shaders/`, `vfx/`)
- **Code & Architecture**: `deliverables/code/` (`src/controllers/`, `src/systems/`, `tests/`)
- **QA & Testing**: `deliverables/qa/` (`TEST_PLAN.md`, `BUG_REPORTS.md`, `PLAYTEST_FEEDBACK.md`)

---

## 3. Operational Protocols

- **Respect Role Boundaries**: If user requests a feature, consult the Game Designer spec and Producer schedule before coding.
- **Data-Driven Logic**: Keep game parameters (speed, health, damage) in editable data configurations rather than hardcoded in engine logic.
- **Quality Gate**: Every feature or code change should be paired with QA verification steps.
- **Orchestration CLI**: You can inspect team state or workflows at any time with:
  `python3 orchestration/run_orchestration.py --list`
  `python3 orchestration/run_orchestration.py --workflow <name>`
