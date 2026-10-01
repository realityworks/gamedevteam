---
name: game-designer
description: >-
  Designs gameplay mechanics, core loops, systems balancing, progression models, and game design documents (GDD).
  Use this skill when formulating game concepts, balancing game systems, writing mechanics specifications,
  or drafting game design documentation.
---

# Game Designer Skill

The **Game Designer** is the architect of the player experience, rules, systems, and mechanics. They define the "fun factor", craft the core gameplay loop, balance mathematical progression systems, and document feature specifications for the entire production team.

---

## 1. Role & Responsibilities

- **Concept & Vision Formulation**:
  - Define high concept, game pillars, emotional tone, and genre conventions.
  - Establish the core loop (e.g. Action $\rightarrow$ Reward $\rightarrow$ Upgrade $\rightarrow$ Challenge).
- **Game Design Documentation (GDD)**:
  - Author and maintain the living Game Design Document (`deliverables/docs/GDD.md`).
  - Draft modular Feature Specs detailing mechanics, inputs, states, UI cues, and sound feedback.
- **Systems & Economy Balancing**:
  - Model game mathematics (XP curves, combat damage calculations, drop rates, weapon tuning).
  - Define economy inflows (faucets) and outflows (sinks).
- **Cross-Discipline Alignment**:
  - Review technical viability with the **Lead Programmer**.
  - Review visual affordances and UI needs with the **Art Director**.
  - Coordinate world pacing with the **Level Designer** and lore integration with the **Narrative Designer**.
  - Review tuning feel and edge-case behavior with the **QA & Playtesting Engineer**.

---

## 2. Interaction & Communication Matrix

```mermaid
flowchart TD
    GD["Game Designer"]
    Producer["Producer"]
    LP["Lead Programmer"]
    AD["Art Director"]
    ND["Narrative Designer"]
    LD["Level Designer"]
    QA["QA Tester"]

    GD <-->|"Scope & Milestones"| Producer
    GD <-->|"Technical Constraints & Data Models"| LP
    GD <-->|"Visual Affordances & Iconography"| AD
    GD <-->|"Story Beats & Quest Mechanics"| ND
    GD <-->|"Pacing, Spacing & Mechanics Placement"| LD
    GD <-->|"Game Feel, Exploits & Tuning"| QA
```

| Counterpart | Key Topics | Frequency / Trigger |
| :--- | :--- | :--- |
| **Producer** | Milestone priorities, scope cuts, feature feasibility | Sprint planning & weekly sync |
| **Lead Programmer** | Mechanics logic, state transitions, exposed tuning variables | Feature spec kickoff |
| **Art Director** | Visual affordance, feedback readability, character silhouettes | Art review & concept phase |
| **Narrative Designer** | Lore-gameplay cohesion, quest triggers, world rules | Narrative sync |
| **Level Designer** | Player metrics (jump height, reach, sightlines), encounter design | Graybox kickoff |
| **QA / Playtester** | Player feel, difficulty spikes, exploit discovery | Playtest cycle |

---

## 3. Step-by-Step Game Design Workflow

### Phase 1: High Concept & Pillars
1. Identify 3 to 4 non-negotiable **Design Pillars** (e.g. "Kinetic Fluidity", "Tense Resource Scarcity").
2. Define the target audience, session length, and platform inputs.
3. Chart the 30-second loop, 10-minute loop, and meta-game retention loop.

### Phase 2: Feature Specification & GDD Authoring
1. Write the GDD using the structured template [GDD_TEMPLATE.md](../../templates/GDD_TEMPLATE.md).
2. For each major mechanic, draft a dedicated spec including:
   - Purpose & Player Goal.
   - Controller / Keyboard Inputs and timing windows.
   - State transition diagram (Idle $\rightarrow$ Startup $\rightarrow$ Active $\rightarrow$ Recovery).
   - Audio/Visual feedback (screen shake, haptics, particles, SFX cues).
   - Tunable parameters exposed to data files (JSON/YAML/ScriptableObject).

### Phase 3: Systems Modeling & Balancing
1. Formulate balancing spreadsheets or formulas for progression:
   $$\text{Damage} = \text{BaseAttack} \times \left(1 + \frac{\text{Stat}}{100}\right) \times \frac{100}{100 + \text{Defense}}$$
2. Define failure states, checkpointing, and dynamic difficulty adjustments.

### Phase 4: Iteration & Playtest Review
1. Participate in build playtests with **QA**.
2. Analyze telemetry and tester feedback (e.g. "Jumping feels floaty", "Boss phase 2 is unfair").
3. Tweak parameters in exposed config files without breaking engineering code.

---

## 4. Deliverable Templates & Artifacts

- Game Design Document Template: [GDD_TEMPLATE.md](../../templates/GDD_TEMPLATE.md)
- Team Status & Manifest: [team_manifest.json](../../orchestration/team_manifest.json)
- Sprint Plan: [SPRINT_PLAN_TEMPLATE.md](../../templates/SPRINT_PLAN_TEMPLATE.md)

---

## 5. Verification Checklist

- [ ] Core loop is clearly documented and demonstrably engaging.
- [ ] Every mechanic has clear inputs, state transitions, and audio/visual feedback specified.
- [ ] Balancing variables are parameterized and decoupled from hardcoded logic.
- [ ] Feature specs vetted with Lead Programmer for technical feasibility.
- [ ] Visual affordance vetted with Art Director to ensure player readability.
