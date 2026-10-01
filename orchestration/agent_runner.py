"""
Agent Runner for GameDevTeam Orchestration.
Executes autonomous AI agents using the Antigravity CLI (agy) to author
deliverable documents, architecture specs, code, and test plans.
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, Callable

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "deliverables" / "logs"

class AgentRunner:
    def __init__(self, base_dir: Optional[Path] = None, model: Optional[str] = None, effort: Optional[str] = None):
        self.base_dir = base_dir or BASE_DIR
        self.agy_bin = self._find_agy()
        self.model = model or os.environ.get("AGY_MODEL")
        self.effort = effort or os.environ.get("AGY_EFFORT")

    def _find_agy(self) -> str:
        bin_path = shutil.which("agy")
        if bin_path:
            return bin_path
        # Check standard user local bin
        user_local = Path.home() / ".local" / "bin" / "agy"
        if user_local.exists():
            return str(user_local)
        raise RuntimeError("Antigravity CLI ('agy') binary not found in PATH or ~/.local/bin.")

    def build_step_prompt(self, step: Dict[str, Any], user_pitch: Optional[str] = None) -> str:
        role_title = step.get("role_title", "Agent")
        role_id = step.get("role_id", "")
        action = step.get("action", "")
        target_output = step.get("target_output", "")
        notes = step.get("notes", "")
        pitch_text = user_pitch.strip() if user_pitch else "Autonomous Design Synthesis (combine unique mechanics patterns with an unconventional visual style)"

        base_instructions = (
            f"You are the **{role_title}** in the GameDevTeam studio orchestration working on a new game project.\n\n"
            f"### Game Pitch & Context:\n"
            f"> \"{pitch_text}\"\n\n"
            f"### Your Task:\n"
            f"Execute: **{action}**\n"
            f"Target Deliverable File: `{target_output}`\n"
            f"Notes: {notes}\n\n"
        )

        specific_guidance = ""
        if step["step"] == 1:
            specific_guidance = (
                "### Detailed Instructions for Step 1 (Game Designer):\n"
                "- Read the template schema in `templates/GDD_TEMPLATE.md`.\n"
                "- Author a complete, highly engaging Game Design Document replacing the contents of `deliverables/docs/GDD.md`.\n"
                "- Define: High Concept Hook, Setting, 3 Core Pillars, the 30-Second Loop (with mermaid diagram), "
                "10-Minute Loop, Meta Progression, Locomotion & Mechanics Table, Combat/Interaction Rules, "
                "Balancing Formulas, and Roadmap Milestones.\n"
                "- Make sure all details specifically reflect the pitch ('" + pitch_text + "').\n"
                "- Write the completed document directly into `deliverables/docs/GDD.md`.\n"
            )
        elif step["step"] == 2:
            specific_guidance = (
                "### Detailed Instructions for Step 2 (Producer):\n"
                "- Read the approved Game Design Document in `deliverables/docs/GDD.md`.\n"
                "- Read the template schema in `templates/SPRINT_PLAN_TEMPLATE.md`.\n"
                "- Author the complete Sprint and Milestone Plan replacing the contents of `deliverables/docs/SPRINT_PLAN.md`.\n"
                "- Break down the features into tasks assigned to specific roles (Lead Programmer, Art Director, Gameplay Dev, Level Designer, Tech Artist, QA).\n"
                "- Define task priorities (P0 to P3), dependencies, risk triage, and acceptance criteria.\n"
                "- Write the completed plan directly into `deliverables/docs/SPRINT_PLAN.md`.\n"
            )
        elif step["step"] == 3:
            specific_guidance = (
                "### Detailed Instructions for Step 3 (Lead Programmer):\n"
                "- Read the approved Game Design Document in `deliverables/docs/GDD.md`.\n"
                "- Read the template schema in `templates/TECH_SPEC_TEMPLATE.md`.\n"
                "- Author the Technical Architecture Specification into `deliverables/docs/TECH_SPEC.md`.\n"
                "- Detail: Engine/Runtime choice, Entity/Component architecture, State Machine diagram, Input buffering, "
                "Fixed update loop, Frame budgets (60 FPS / 16.6ms), Memory limits, and Data persistence schemas.\n"
                "- Write the completed spec directly into `deliverables/docs/TECH_SPEC.md`.\n"
            )
        elif step["step"] == 4:
            specific_guidance = (
                "### Detailed Instructions for Step 4 (Art Director):\n"
                "- Read the approved Game Design Document in `deliverables/docs/GDD.md`.\n"
                "- Read the template schema in `templates/ART_BIBLE_TEMPLATE.md`.\n"
                "- Author the complete Art Bible into `deliverables/art/ART_BIBLE.md`.\n"
                "- Detail: Visual style pillars, mood & lighting rules, color hex palette (Dominant, Secondary, Danger), "
                "silhouette guides, polygon/vertex budgets, texture resolutions, and animation/VFX telegraphing rules.\n"
                "- Write the completed bible directly into `deliverables/art/ART_BIBLE.md`.\n"
            )
        elif step["step"] == 5:
            specific_guidance = (
                "### Detailed Instructions for Step 5 (Level Designer):\n"
                "- Read `deliverables/docs/GDD.md` and `deliverables/docs/TECH_SPEC.md`.\n"
                "- Author the Level Design & Graybox Blockout spec in `deliverables/docs/LEVEL_DESIGN.md`.\n"
                "- Detail: Character metrics (jump width, mantle height, corridor clearances), spatial flow diagram, "
                "encounter zoning, sightline signposting, and obstacle obstacle test arena layout.\n"
                "- Write directly into `deliverables/docs/LEVEL_DESIGN.md`.\n"
            )
        elif step["step"] == 6:
            specific_guidance = (
                "### Detailed Instructions for Step 6 (Gameplay Programmer):\n"
                "- Read `deliverables/docs/GDD.md` and `deliverables/docs/TECH_SPEC.md`.\n"
                "- Write the core player controller and state machine in `deliverables/code/src/controllers/player_controller.py`.\n"
                "- Implement responsive movement, jump with coyote time and jump buffering, action triggers, and state transitions.\n"
                "- Ensure code is modular, clean, and includes tests in `deliverables/code/tests/`.\n"
            )
        elif step["step"] == 7:
            specific_guidance = (
                "### Detailed Instructions for Step 7 (Technical Artist):\n"
                "- Read `deliverables/art/ART_BIBLE.md` and `deliverables/docs/TECH_SPEC.md`.\n"
                "- Setup the master shader guidelines and VFX triggers in `deliverables/art/shaders/` and `deliverables/art/vfx/`.\n"
                "- Document draw call batching, LOD thresholds, and particle emitter budgets.\n"
            )
        elif step["step"] == 8:
            specific_guidance = (
                "### Detailed Instructions for Step 8 (QA & Playtesting Engineer):\n"
                "- Read `deliverables/docs/GDD.md`, `deliverables/docs/TECH_SPEC.md`, and code deliverables.\n"
                "- Read the template schema in `templates/QA_TEST_PLAN_TEMPLATE.md`.\n"
                "- Author the Master Test Plan in `deliverables/qa/TEST_PLAN.md` with test matrices covering movement, "
                "collision boundaries, state corruption edge cases, and performance stress tests.\n"
                "- Create initial bug reports and verification notes in `deliverables/qa/BUG_REPORTS.md`.\n"
            )

        closing = (
            "\n### Quality Standard:\n"
            "Produce production-grade, highly articulated content. Do NOT leave placeholder brackets (like '[Title]'). "
            "Write the actual files to disk before concluding your turn."
        )

        return base_instructions + specific_guidance + closing

    def run_step_process(self, step: Dict[str, Any], user_pitch: Optional[str] = None, log_callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Executes the autonomous agent for a given step using agy in a subprocess.
        Logs output to deliverables/logs/step_<N>_<role>.log.
        """
        step_num = step["step"]
        role_id = step.get("role_id", "agent")
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_file_path = LOGS_DIR / f"step_{step_num}_{role_id}.log"

        prompt = self.build_step_prompt(step, user_pitch)

        cmd = [
            self.agy_bin,
            "--dangerously-skip-permissions",
            "-p",
            prompt
        ]
        if self.model:
            cmd.extend(["--model", self.model])
        if self.effort:
            cmd.extend(["--effort", self.effort])

        if log_callback:
            log_callback(f"Launching autonomous agent [{step['role_title']}] for Step {step_num}...")

        with open(log_file_path, "w", encoding="utf-8") as log_file:
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir),
                stdout=log_file,
                stderr=subprocess.STDOUT
            )

            # Wait for agent process to finish
            process.wait()
            exit_code = process.returncode

        if exit_code == 0:
            if log_callback:
                log_callback(f"[✓] Step {step_num} completed successfully by [{step['role_title']}]. Log: {log_file_path.name}")
            return True
        else:
            if log_callback:
                log_callback(f"[!] Step {step_num} failed with exit code {exit_code}. Check {log_file_path}")
            return False
