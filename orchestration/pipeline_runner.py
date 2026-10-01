#!/usr/bin/env python3
"""
Pipeline Runner for GameDevTeam Orchestration.
Supports running in the background, live status tracking, user review gates,
and populating deliverable files from templates into the deliverables/ folder.

Usage:
    # Initialize and run pipeline in background
    python3 pipeline_runner.py --init --pitch "Cyberpunk gravity stealth"
    python3 pipeline_runner.py --init   # Autonomous mode (no pitch)

    # Check progress & dashboard anytime
    python3 pipeline_runner.py --status

    # Step-in review
    python3 pipeline_runner.py --review-step 1
    python3 pipeline_runner.py --approve-step 1
"""

import argparse
import datetime
import json
import shutil
import sys
from pathlib import Path
from typing import Optional, Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
DELIVERABLES_DIR = BASE_DIR / "deliverables"
STATUS_FILE = BASE_DIR / "deliverables" / "PROJECT_STATUS.json"
DASHBOARD_FILE = BASE_DIR / "deliverables" / "docs" / "PROJECT_DASHBOARD.md"

try:
    from orchestrator import GameDevOrchestrator
except ImportError:
    from .orchestrator import GameDevOrchestrator


class PipelineRunner:
    def __init__(self):
        self.orchestrator = GameDevOrchestrator()
        self.status = self._load_status()

    def _load_status(self) -> Dict[str, Any]:
        if STATUS_FILE.exists():
            try:
                with open(STATUS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_status(self):
        STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.status, f, indent=2)
        self._render_dashboard()

    def _render_dashboard(self):
        """Generates a Markdown dashboard for easy reading and review."""
        if not self.status:
            return

        lines = [
            f"# GameDevStudio — Live Production Dashboard",
            f"",
            f"**Workflow**: `{self.status.get('workflow')}`  ",
            f"**Mode**: `{self.status.get('mode')}`  ",
            f"**Last Updated**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**User Pitch**: *\"{self.status.get('user_pitch') or 'Autonomous Design Synthesis'}\"*  ",
            f"",
            f"---",
            f"",
            f"## Pipeline Steps & Deliverables",
            f"",
            f"| Step | Role | Action | Deliverable File | Status | Review Gate |",
            f"| :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for s in self.status.get("steps", []):
            st = s.get("status", "Pending")
            icon = "⚪"
            if st == "Completed":
                icon = "🟢"
            elif st == "In Progress":
                icon = "🟡"
            elif st == "Awaiting Review":
                icon = "🟠"

            review_str = "Approved" if s.get("approved") else ("Needs Review" if st == "Completed" else "Pending")
            lines.append(f"| {s['step']} | **{s['role_title']}** | {s['action']} | [`{s['target_output']}`](../../{s['target_output']}) | {icon} {st} | {review_str} |")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## How to Step In & Review",
            f"- Run `python3 orchestration/pipeline_runner.py --status` to inspect current progress.",
            f"- Check generated files directly inside `deliverables/`.",
            f"- Run `python3 orchestration/pipeline_runner.py --approve-step <N>` to sign off on a deliverable.",
            f""
        ])

        DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def init_pipeline(self, pitch: Optional[str] = None):
        """Initializes the pipeline and populates initial deliverable files from templates."""
        plan = self.orchestrator.generate_pitch_to_prototype_plan(pitch)

        # Template mapping
        template_map = {
            "deliverables/docs/GDD.md": TEMPLATES_DIR / "GDD_TEMPLATE.md",
            "deliverables/docs/SPRINT_PLAN.md": TEMPLATES_DIR / "SPRINT_PLAN_TEMPLATE.md",
            "deliverables/docs/TECH_SPEC.md": TEMPLATES_DIR / "TECH_SPEC_TEMPLATE.md",
            "deliverables/art/ART_BIBLE.md": TEMPLATES_DIR / "ART_BIBLE_TEMPLATE.md",
            "deliverables/qa/TEST_PLAN.md": TEMPLATES_DIR / "QA_TEST_PLAN_TEMPLATE.md",
            "deliverables/qa/BUG_REPORTS.md": TEMPLATES_DIR / "QA_TEST_PLAN_TEMPLATE.md",
        }

        # Ensure deliverables directories exist and populate starter files if missing
        for dest_rel, src_tpl in template_map.items():
            dest_file = BASE_DIR / dest_rel
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            if not dest_file.exists() and src_tpl.exists():
                shutil.copyfile(src_tpl, dest_file)

        steps_state = []
        for s in plan["steps"]:
            steps_state.append({
                "step": s["step"],
                "role_id": s["role_id"],
                "role_title": s["role_title"],
                "action": s["action"],
                "target_output": s["target_output"],
                "notes": s["notes"],
                "directive": s["directive"],
                "status": "Pending",
                "approved": False,
                "completed_at": None
            })

        self.status = {
            "workflow": plan["workflow"],
            "mode": plan["mode"],
            "mode_description": plan["mode_description"],
            "user_pitch": plan["user_pitch"],
            "initialized_at": datetime.datetime.now().isoformat(),
            "current_step": 1,
            "steps": steps_state
        }

        # Mark step 1 as In Progress
        if self.status["steps"]:
            self.status["steps"][0]["status"] = "In Progress"

        self._save_status()
        print(f"\n[Pipeline Initialized]")
        print(f"Mode: {plan['mode_description']}")
        print(f"Dashboard generated: {DASHBOARD_FILE}")
        print(f"Templates populated in deliverables/:")
        for rel in template_map.keys():
            print(f"  • {rel}")

    def update_step_status(self, step_number: int, new_status: str, approved: bool = False):
        """Update step progress."""
        for s in self.status.get("steps", []):
            if s["step"] == step_number:
                s["status"] = new_status
                s["approved"] = approved
                if new_status == "Completed":
                    s["completed_at"] = datetime.datetime.now().isoformat()
                    # Advance next step to In Progress if exists
                    next_step = step_number + 1
                    for ns in self.status.get("steps", []):
                        if ns["step"] == next_step and ns["status"] == "Pending":
                            ns["status"] = "In Progress"
                            self.status["current_step"] = next_step
                            break
                break
        self._save_status()

    def print_status(self):
        if not self.status:
            print("\nNo active pipeline status found. Initialize one with --init [--pitch '...']")
            return

        print(f"\n=======================================================")
        print(f"  LIVE PRODUCTION STATUS: {self.status.get('workflow')}")
        print(f"=======================================================")
        print(f"Mode: {self.status.get('mode_description')}")
        print(f"User Pitch: {self.status.get('user_pitch') or '(Autonomous Synthesis)'}")
        print(f"Dashboard File: {DASHBOARD_FILE}\n")

        for s in self.status.get("steps", []):
            st = s.get("status", "Pending")
            review = "Approved" if s.get("approved") else ("Review Ready" if st == "Completed" else "Waiting")
            print(f"Step {s['step']}: [{st.upper()}] {s['role_title']} — {s['action']}")
            print(f"  Deliverable: {s['target_output']} ({review})")
        print()


def main():
    parser = argparse.ArgumentParser(description="GameDevTeam Background Pipeline Runner")
    parser.add_argument("--init", action="store_true", help="Initialize the pipeline and populate deliverables from templates")
    parser.add_argument("--pitch", nargs="?", const="", default=None, help="Optional pitch idea for the pipeline")
    parser.add_argument("--status", action="store_true", help="View current production status and step deliverables")
    parser.add_argument("--approve-step", type=int, help="Approve and mark a step deliverable as reviewed")
    parser.add_argument("--complete-step", type=int, help="Mark a step as completed")

    args = parser.parse_args()
    runner = PipelineRunner()

    if args.init:
        runner.init_pipeline(args.pitch)
        return

    if args.status or len(sys.argv) == 1:
        runner.print_status()
        return

    if args.approve_step:
        runner.update_step_status(args.approve_step, "Completed", approved=True)
        print(f"Step {args.approve_step} approved and marked completed.")
        runner.print_status()
        return

    if args.complete_step:
        runner.update_step_status(args.complete_step, "Completed", approved=False)
        print(f"Step {args.complete_step} marked completed. Awaiting review.")
        runner.print_status()
        return


if __name__ == "__main__":
    main()
