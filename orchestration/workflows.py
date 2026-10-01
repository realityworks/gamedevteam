"""
Workflows module for GameDevTeam multi-agent orchestration.
Defines end-to-end task pipelines connecting Producer, Leads, Designers, Developers, and QA.
"""

from typing import List, Dict, Any

WORKFLOWS: Dict[str, Dict[str, Any]] = {
    "pitch_to_prototype": {
        "name": "Pitch to Playable Prototype",
        "description": "Transforms a game pitch (or autonomous design synthesis when no pitch is provided) into a validated technical prototype with core movement, graybox testing, and visual styling.",
        "input_parameters": {
            "pitch_prompt": {
                "type": "string",
                "required": False,
                "default": None,
                "description": "General idea or high concept for the pitch. If omitted or empty, the Game Designer autonomously discovers a novel concept by combining orthogonal game design patterns with an unconventional visual representation."
            }
        },
        "special_cases": {
            "no_prompt_provided": "Autonomous Ideation: The Game Designer synthesizes a novel concept by selecting 2-3 disparate game design patterns (e.g. inertia recoil + temporal ghost replay + spatial inventory) and coupling them with a distinct, unconventional visual aesthetic (e.g. Risograph halftone, stained-glass refraction, or brutalist blueprint)."
        },
        "steps": [
            {
                "step": 1,
                "role": "game_designer",
                "action": "Draft Core Mechanics & Design Pillars (Pitch Intake / Autonomous Synthesis)",
                "output": "deliverables/docs/GDD.md",
                "notes": "If pitch provided: expand into full GDD. If no pitch: autonomously synthesize a unique pattern combination + visual representation."
            },
            {
                "step": 2,
                "role": "producer",
                "action": "Create Prototype Milestone Schedule & Backlog",
                "output": "deliverables/docs/SPRINT_PLAN.md",
                "notes": "Deconstruct GDD into prototype sprint deliverables."
            },
            {
                "step": 3,
                "role": "lead_programmer",
                "action": "Author Technical Architecture RFC",
                "output": "deliverables/docs/TECH_SPEC.md",
                "notes": "Select engine/runtime, state machine pattern, and fixed update loops."
            },
            {
                "step": 4,
                "role": "art_director",
                "action": "Author Visual Bible & Mood Board",
                "output": "deliverables/art/ART_BIBLE.md",
                "notes": "Establish visual style, shape language, and color palette."
            },
            {
                "step": 5,
                "role": "level_designer",
                "action": "Build Graybox Movement Test Arena",
                "output": "deliverables/docs/LEVEL_DESIGN.md",
                "notes": "Set up jumping gaps, slopes, and obstacle courses matching player metrics."
            },
            {
                "step": 6,
                "role": "gameplay_programmer",
                "action": "Implement Character Controller & FSM",
                "output": "deliverables/code/src/controllers/player_controller.py",
                "notes": "Build movement, jumping, coyote time, and input buffering."
            },
            {
                "step": 7,
                "role": "technical_artist",
                "action": "Setup Master Shaders & Performance Baseline",
                "output": "deliverables/art/shaders/",
                "notes": "Provide test materials and set draw call budget monitors."
            },
            {
                "step": 8,
                "role": "qa_playtester",
                "action": "Execute Prototype Smoke Test & Report Edge Cases",
                "output": "deliverables/qa/TEST_PLAN.md",
                "notes": "Validate physics edge cases, collision boundaries, and game feelsnappiness."
            }
        ]
    },
    "feature_sprint": {
        "name": "Feature Implementation Sprint",
        "description": "Standard two-week feature production cycle from specification to QA sign-off.",
        "steps": [
            {
                "step": 1,
                "role": "game_designer",
                "action": "Deliver Feature Spec Document",
                "output": "deliverables/docs/FEATURE_SPECS.md",
                "notes": "Define inputs, state transitions, audio-visual feedback, and tuning vars."
            },
            {
                "step": 2,
                "role": "producer",
                "action": "Triage & Assign Sprint Tasks",
                "output": "deliverables/docs/SPRINT_PLAN.md",
                "notes": "Confirm scope with Art Director and Lead Programmer."
            },
            {
                "step": 3,
                "role": "lead_programmer",
                "action": "Code Review Architecture & Assign Coding Subtasks",
                "output": "deliverables/docs/TECH_SPEC.md",
                "notes": "Define data contracts and state handlers."
            },
            {
                "step": 4,
                "role": "art_director",
                "action": "Assign Visual Assets & Review Submissions",
                "output": "deliverables/art/",
                "notes": "Review 2D sprites / 3D models against Art Bible."
            },
            {
                "step": 5,
                "role": "gameplay_programmer",
                "action": "Code Gameplay Systems & Hook Events",
                "output": "deliverables/code/src/systems/",
                "notes": "Implement logic, expose config variables, write unit tests."
            },
            {
                "step": 6,
                "role": "technical_artist",
                "action": "Implement VFX & Optimize Draw Calls",
                "output": "deliverables/art/vfx/",
                "notes": "Hook particle triggers into gameplay events."
            },
            {
                "step": 7,
                "role": "qa_playtester",
                "action": "Execute Acceptance Testing & Log Bug Tickets",
                "output": "deliverables/qa/BUG_REPORTS.md",
                "notes": "Validate feature against acceptance criteria."
            }
        ]
    },
    "narrative_quest_pipeline": {
        "name": "Narrative & Quest Integration Pipeline",
        "description": "Integrates worldbuilding lore, quest state machines, and level placement.",
        "steps": [
            {
                "step": 1,
                "role": "narrative_designer",
                "action": "Write Lore Bible & Quest Arc",
                "output": "deliverables/docs/NARRATIVE_BIBLE.md",
                "notes": "Define character motivations, branching choices, and dialogue trees."
            },
            {
                "step": 2,
                "role": "game_designer",
                "action": "Align Quest Rewards with Economy Balancing",
                "output": "deliverables/docs/GDD.md",
                "notes": "Ensure XP, currency, and loot align with player progression."
            },
            {
                "step": 3,
                "role": "level_designer",
                "action": "Embed Story Landmarks & Audio Logs",
                "output": "deliverables/docs/LEVEL_DESIGN.md",
                "notes": "Position narrative triggers and landmark silhouettes in the map."
            },
            {
                "step": 4,
                "role": "gameplay_programmer",
                "action": "Implement Quest State Machine & Dialogue UI Parser",
                "output": "deliverables/code/src/systems/quest_manager.py",
                "notes": "Read dialogue JSON and handle flag persistence."
            },
            {
                "step": 5,
                "role": "qa_playtester",
                "action": "Validate Branching Dialogue & Prevent Softlocks",
                "output": "deliverables/qa/TEST_PLAN.md",
                "notes": "Verify all quest states trigger correctly."
            }
        ]
    }
}
