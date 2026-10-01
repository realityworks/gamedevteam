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
