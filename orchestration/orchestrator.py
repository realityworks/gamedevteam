"""
GameDevTeam Orchestrator Engine.
Manages multi-agent coordination, role resolution, pipeline execution,
and task dispatching across the game development team.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = BASE_DIR / "orchestration" / "team_manifest.json"

try:
    from workflows import WORKFLOWS
except ImportError:
    from .workflows import WORKFLOWS


class GameDevOrchestrator:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or BASE_DIR
        self.manifest = self._load_manifest()
        self.roles = self.manifest.get("roles", {})
        self.workflows = WORKFLOWS

    def _load_manifest(self) -> Dict[str, Any]:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_roles(self) -> List[Dict[str, Any]]:
        """Return formatted metadata for all available team roles."""
        result = []
        for role_id, info in self.roles.items():
            result.append({
                "id": role_id,
                "title": info["title"],
                "layer": info["layer"],
                "skill_name": info["skill_name"],
                "summary": info["summary"],
                "coordinates_with": info["coordinates_with"],
                "primary_outputs": info["primary_outputs"]
            })
        return result

    def get_role(self, role_id: str) -> Optional[Dict[str, Any]]:
        """Get role definition by id."""
        return self.roles.get(role_id)

    def find_role_by_trigger(self, prompt: str) -> List[str]:
        """Match roles based on trigger keywords in a user prompt."""
        prompt_lower = prompt.lower()
        matched = []
        for role_id, info in self.roles.items():
            for trigger in info.get("triggers", []):
                if trigger in prompt_lower:
                    matched.append(role_id)
                    break
        return matched

    def get_skill_path(self, role_id: str) -> Optional[Path]:
        """Resolve absolute path to a role's SKILL.md."""
        role = self.get_role(role_id)
        if not role:
            return None
        skill_name = role.get("skill_name")
        skill_path = self.base_dir / ".agents" / "skills" / skill_name / "SKILL.md"
        return skill_path if skill_path.exists() else None

    def get_subagent_spec(self, role_id: str, custom_task: Optional[str] = None) -> Dict[str, str]:
        """
        Generate instructions and role metadata for spawning an Antigravity subagent.
        """
        role = self.get_role(role_id)
        if not role:
            raise ValueError(f"Unknown role ID: {role_id}")

        skill_file = self.get_skill_path(role_id)
        skill_ref = f"Refer to your detailed skill guide at {skill_file}" if skill_file else ""

        task_desc = custom_task or f"Execute standard duties for {role['title']} according to sprint goals."

        prompt = (
            f"You are operating as the **{role['title']}** in the GameDevTeam orchestration.\n\n"
            f"### Role Summary:\n{role['summary']}\n\n"
            f"### Team Coordination:\n"
            f"- You report to / coordinate with: {', '.join(role['coordinates_with'])}\n"
            f"- Your expected outputs: {', '.join(role['primary_outputs'])}\n\n"
            f"{skill_ref}\n\n"
            f"### Current Assignment:\n{task_desc}\n\n"
            f"Please write your deliverables to the appropriate paths inside `{self.base_dir}`."
        )

        return {
            "role": role["title"],
            "typeName": "self",
            "prompt": prompt
        }

    def generate_pitch_to_prototype_plan(self, user_pitch: Optional[str] = None) -> Dict[str, Any]:
        """
        Generates a tailored execution plan for the Pitch to Prototype workflow.
        If user_pitch is provided: directs the Game Designer to expand the concept.
        If user_pitch is empty/None: triggers autonomous design synthesis combining
        unique game design patterns with an unconventional visual representation.
        """
        clean_pitch = user_pitch.strip() if user_pitch else ""
        workflow = self.get_workflow("pitch_to_prototype")
        if not workflow:
            raise ValueError("Workflow 'pitch_to_prototype' not found.")

        if clean_pitch:
            mode = "USER_PROVIDED_PITCH"
            mode_description = f"User Concept Expansion: \"{clean_pitch}\""
            designer_directive = (
                f"### User Pitch Intake:\n"
                f"The user has provided the following concept:\n"
                f"> \"{clean_pitch}\"\n\n"
                f"### Game Designer Directives:\n"
                f"1. Deconstruct the user's pitch into 3 distinct Core Design Pillars.\n"
                f"2. Formulate the primary 30-second gameplay loop (Action -> Feedback -> Reposition -> Reward).\n"
                f"3. Specify player locomotion metrics (walk/sprint speed, jump height, gravity scale, buffer/coyote frames).\n"
                f"4. Document the feature spec in `deliverables/docs/GDD.md` using the GDD template.\n"
                f"5. Hand off scope parameters to the Producer and technical constraints to the Lead Programmer."
            )
        else:
            mode = "AUTONOMOUS_SYNTHESIS"
            mode_description = "Autonomous Design Synthesis: Unique Pattern Combination + Distinct Visual Representation"
            designer_directive = (
                f"### Autonomous Creative Synthesis Mode (No Prompt Provided):\n"
                f"You must discover and formulate an original, non-cliché game concept by synthesizing a unique combination "
                f"of orthogonal **Game Design Patterns** paired with an **Unconventional Visual Representation**.\n\n"
                f"#### 1. Game Design Patterns Matrix (Select 2-3 orthogonal patterns):\n"
                f"- **Locomotion / Momentum**: Kinetic recoil-propulsion, orbital slinging, gravity inversion, wall-running friction.\n"
                f"- **Temporal / Causality**: Time-echo / ghost replays (cooperating with past self), asynchronous ticks, scrub-back rewind.\n"
                f"- **Spatial / Dimensional**: Non-Euclidean topology, fold-out origami geometry, perspective alignment puzzle-spaces.\n"
                f"- **Resource / Friction**: Degradable abilities as ammunition, health-as-currency, memory sacrifice progression.\n"
                f"- **Perception / Sensorium**: Echoloaction wave visualization, thermal conductivity, light/shadow phase shifting.\n\n"
                f"#### 2. Unique Visual Representation (Select 1 distinct aesthetic):\n"
                f"- **Risograph Print**: Offset grainy textures, neon spot inks, and CMYK halftone screen dithering.\n"
                f"- **Architectural Cyanotype / Blueprint**: Pristine white drafting lines on deep Prussian blue drafting paper.\n"
                f"- **Stained-Glass Leadlight**: Heavy black lead caming dividing luminous, refractive colored jewel-tone glass.\n"
                f"- **Microscopic Dark-Field Bioluminescence**: Phosphorescent organisms against deep aqueous black, chromatic aberration.\n"
                f"- **Bauhaus Geometric Modernism**: Primary colors (red, yellow, blue), stark geometric primitives, clean typography.\n"
                f"- **Woodblock Ukiyo-e**: Dynamic Japanese woodblock grain, washi paper texture, and stylized sumi-e ink washes.\n"
                f"- **Tactile Claymation**: Hand-sculpted clay with visible thumbprint seams, stop-motion framerate jitter (12-15 fps).\n\n"
                f"#### 3. Synthesis Requirements:\n"
                f"1. Name the game and define its high concept in one punchy sentence.\n"
                f"2. Explain how the chosen mechanics patterns create unexpected emergent gameplay.\n"
                f"3. Explain how the visual representation reinforces player readability and game feel.\n"
                f"4. Author the complete Game Design Document in `deliverables/docs/GDD.md` following `templates/GDD_TEMPLATE.md`.\n"
                f"5. Notify the Producer, Lead Programmer, and Art Director to initiate downstream tasks."
            )

        steps_detail = []
        for step in workflow["steps"]:
            role_info = self.get_role(step["role"])
            step_prompt = designer_directive if step["step"] == 1 else (
                f"Review deliverables from previous steps and execute Step {step['step']}: "
                f"{step['action']}. Target output: `{step['output']}`. Notes: {step['notes']}"
            )
            steps_detail.append({
                "step": step["step"],
                "role_id": step["role"],
                "role_title": role_info["title"] if role_info else step["role"],
                "action": step["action"],
                "target_output": step["output"],
                "notes": step["notes"],
                "directive": step_prompt
            })

        return {
            "workflow": "pitch_to_prototype",
            "mode": mode,
            "mode_description": mode_description,
            "user_pitch": clean_pitch if clean_pitch else None,
            "steps": steps_detail
        }

    def get_workflow(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a predefined multi-stage workflow."""
        return self.workflows.get(workflow_name)

    def print_team_status(self):
        """Prints a human-readable overview of the studio team."""
        print(f"\n=======================================================")
        print(f"  {self.manifest.get('team_name')} (v{self.manifest.get('version')})")
        print(f"=======================================================\n")
        print("Team Hierarchy & Roles:\n")
        for r in self.list_roles():
            print(f"• [{r['layer']}] {r['title']} (skill: `{r['skill_name']}`)")
            print(f"  Summary: {r['summary']}")
            print(f"  Coordinates With: {', '.join(r['coordinates_with'])}")
            print(f"  Key Outputs: {', '.join(r['primary_outputs'])}")
            print()


if __name__ == "__main__":
    orchestrator = GameDevOrchestrator()
    orchestrator.print_team_status()
