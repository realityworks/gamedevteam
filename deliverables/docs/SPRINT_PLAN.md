# [Game Title] — Sprint & Milestone Plan

**Sprint Cycle**: Sprint [Number] ([Start Date] to [End Date])  
**Owner / Author**: Producer  
**Milestone Focus**: [Prototype / First Playable / Alpha / Beta / Gold]  

---

## 1. Sprint Goals & High-Level Objectives

- **Goal 1**: [Primary gameplay delivery - e.g. Functional player combat controller with dash].
- **Goal 2**: [Primary art/level delivery - e.g. Whitebox Level 1 arena with graybox enemy].
- **Goal 3**: [Infrastructure - e.g. Input action binding system and CI pipeline setup].

---

## 2. Cross-Functional Task Assignment Matrix

| Task ID | Discipline | Assignee | Task Description | Dependencies | Est. (Pts / Days) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TSK-101** | Production | Producer | Setup sprint backlog & milestone tracking | None | 1d | Done |
| **TSK-102** | Design | Game Designer | Draft GDD Section 3: Player Movement & Dash | None | 2d | In Progress |
| **TSK-103** | Tech Lead | Lead Programmer | Architecture RFC: State machine & fixed timestep loop | TSK-102 | 2d | Pending |
| **TSK-104** | Art Lead | Art Director | Mood board & color key for Level 1 Sanctuary | None | 2d | In Progress |
| **TSK-105** | Tech Art | Technical Artist | Master PBR shader & texture packing pipeline | TSK-104 | 3d | Pending |
| **TSK-106** | Gameplay | Gameplay Dev | Implement Character Controller FSM & coyote time | TSK-103 | 3d | Pending |
| **TSK-107** | Level | Level Designer | Graybox blockout for Level 1 introductory section | TSK-102 | 2d | Pending |
| **TSK-108** | Narrative | Narrative Dev | Write intro dialogue barks and faction lore primer | None | 2d | In Progress |
| **TSK-109** | QA | QA Playtester | Formulate Test Suite for Character Controller physics | TSK-106 | 2d | Pending |

---

## 3. Risks, Blockers & Mitigations

| Risk / Blocker ID | Description | Impact | Mitigation Strategy | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | Controller coyote time might feel floaty | Medium | Expose tuning config values for rapid designer tweaks | Gameplay Dev |
| **RSK-02** | Custom shaders exceeding mobile GPU budgets | High | Fallback unlit / simple PBR shader variant | Tech Artist |

---

## 4. Milestone Acceptance Criteria

- [ ] Character controller verified with 0 dropped frames or physics clipping.
- [ ] Graybox arena playable start-to-finish without softlocks.
- [ ] All code PRs merged with 100% passing tests and Lead Programmer sign-off.
- [ ] QA smoke test completed with zero P0/P1 defects remaining open.
