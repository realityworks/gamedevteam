# GameDevStudio — Live Production Dashboard

**Workflow**: `pitch_to_prototype`  
**Mode**: `USER_PROVIDED_PITCH`  
**Last Updated**: 2026-10-01 14:59:19  
**User Pitch**: *"Match3 RPG style game. Combine bejewelled with ultima"*  

---

## Pipeline Steps & Deliverables

| Step | Role | Action | Deliverable File | Status | Review Gate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Game Designer** | Draft Core Mechanics & Design Pillars (Pitch Intake / Autonomous Synthesis) | [`deliverables/docs/GDD.md`](../../deliverables/docs/GDD.md) | 🟡 In Progress | Pending |
| 2 | **Producer** | Create Prototype Milestone Schedule & Backlog | [`deliverables/docs/SPRINT_PLAN.md`](../../deliverables/docs/SPRINT_PLAN.md) | ⚪ Pending | Pending |
| 3 | **Lead Programmer** | Author Technical Architecture RFC | [`deliverables/docs/TECH_SPEC.md`](../../deliverables/docs/TECH_SPEC.md) | ⚪ Pending | Pending |
| 4 | **Art Director** | Author Visual Bible & Mood Board | [`deliverables/art/ART_BIBLE.md`](../../deliverables/art/ART_BIBLE.md) | ⚪ Pending | Pending |
| 5 | **Level & Environment Designer** | Build Graybox Movement Test Arena | [`deliverables/docs/LEVEL_DESIGN.md`](../../deliverables/docs/LEVEL_DESIGN.md) | ⚪ Pending | Pending |
| 6 | **Gameplay & Systems Programmer** | Implement Character Controller & FSM | [`deliverables/code/src/controllers/player_controller.py`](../../deliverables/code/src/controllers/player_controller.py) | ⚪ Pending | Pending |
| 7 | **Technical Artist** | Setup Master Shaders & Performance Baseline | [`deliverables/art/shaders/`](../../deliverables/art/shaders/) | ⚪ Pending | Pending |
| 8 | **QA & Playtesting Engineer** | Execute Prototype Smoke Test & Report Edge Cases | [`deliverables/qa/TEST_PLAN.md`](../../deliverables/qa/TEST_PLAN.md) | ⚪ Pending | Pending |

---

## How to Step In & Review
- Run `python3 orchestration/pipeline_runner.py --status` to inspect current progress.
- Check generated files directly inside `deliverables/`.
- Run `python3 orchestration/pipeline_runner.py --approve-step <N>` to sign off on a deliverable.
