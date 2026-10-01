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
from typing import Optional, Dict, Any, Callable

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
DELIVERABLES_DIR = BASE_DIR / "deliverables"
STATUS_FILE = BASE_DIR / "deliverables" / "PROJECT_STATUS.json"
DASHBOARD_FILE = BASE_DIR / "deliverables" / "docs" / "PROJECT_DASHBOARD.md"

try:
    from orchestrator import GameDevOrchestrator
except ImportError:
    from .orchestrator import GameDevOrchestrator

try:
    from agent_runner import AgentRunner
except ImportError:
    from .agent_runner import AgentRunner


MAJOR_STAGES = [
    {
        "stage": 1,
        "title": "Design & Scope",
        "gate": "Gate 1: Game Design Document (GDD) & Sprint Plan Approval",
        "steps": [1, 2]
    },
    {
        "stage": 2,
        "title": "Tech Architecture & Visual Bible",
        "gate": "Gate 2: Technical Architecture & Art Bible Approval",
        "steps": [3, 4]
    },
    {
        "stage": 3,
        "title": "Playable Prototype & Core Mechanics",
        "gate": "Gate 3: Playable Prototype, Controls & Level Blockout Approval",
        "steps": [5, 6, 7]
    },
    {
        "stage": 4,
        "title": "QA Verification & Milestone Release",
        "gate": "Gate 4: QA Acceptance, Test Matrix & Release Sign-Off",
        "steps": [8]
    }
]


class PipelineRunner:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or BASE_DIR
        self.orchestrator = GameDevOrchestrator()
        self.status = self._load_status()
        self.agent_runner = AgentRunner(self.base_dir)

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
        """Generates a Markdown dashboard organized by Major Stages & Gates."""
        if not self.status:
            return

        lines = [
            f"# GameDevStudio — Master Production Dashboard",
            f"",
            f"**Workflow**: `{self.status.get('workflow')}`  ",
            f"**Mode**: `{self.status.get('mode')}`  ",
            f"**Last Updated**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**User Pitch**: *\"{self.status.get('user_pitch') or 'Autonomous Design Synthesis'}\"*  ",
            f"",
            f"---",
            f"",
            f"## Production Stages & User Sign-Off Gates",
            f""
        ]

        steps_by_num = {s["step"]: s for s in self.status.get("steps", [])}

        for stg in MAJOR_STAGES:
            stage_num = stg["stage"]
            stage_steps = [steps_by_num[n] for n in stg["steps"] if n in steps_by_num]
            all_done = all(s.get("status") == "Completed" and s.get("approved") for s in stage_steps)
            any_in_prog = any(s.get("status") == "In Progress" for s in stage_steps)

            stg_status_str = "🟢 APPROVED" if all_done else ("🟡 IN PROGRESS" if any_in_prog else "⚪ PENDING")
            lines.append(f"### Major Stage {stage_num}: {stg['title']} — {stg_status_str}")
            lines.append(f"**Sign-Off Gate**: *{stg['gate']}*")
            lines.append("")
            lines.append(f"| Step | Role | Action | Deliverable File | Step Status | Review Gate |")
            lines.append(f"| :--- | :--- | :--- | :--- | :--- | :--- |")

            for s in stage_steps:
                st = s.get("status", "Pending")
                icon = "⚪"
                if st == "Completed":
                    icon = "🟢"
                elif st == "In Progress":
                    icon = "🟡"
                elif st == "Awaiting Review":
                    icon = "🟠"
                review_str = "Approved" if s.get("approved") else ("Needs Review" if st == "Completed" else "Waiting")
                lines.append(f"| {s['step']} | **{s['role_title']}** | {s['action']} | [`{s['target_output']}`](../../{s['target_output']}) | {icon} {st} | {review_str} |")

            lines.append("")

        lines.extend([
            f"---",
            f"",
            f"## User Sign-Off Controls",
            f"- Run `python3 orchestration/pipeline_runner.py --status` to inspect current stage.",
            f"- Review generated deliverables in `deliverables/`.",
            f"- Approve an entire stage: `python3 orchestration/pipeline_runner.py --approve-stage <1-4>`",
            f"- Approve an individual step: `python3 orchestration/pipeline_runner.py --approve-step <N>`",
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
                if approved:
                    s["status"] = "Completed"
                    s["completed_at"] = datetime.datetime.now().isoformat()
                break
        self._save_status()

    def print_status(self):
        self.status = self._load_status()
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
            icon = "⚪"
            if st == "Completed":
                icon = "🟢"
            elif st == "In Progress":
                icon = "🟡"
            elif st == "Awaiting Review":
                icon = "🟠"
            review = "Approved" if s.get("approved") else ("Review Ready" if st == "Completed" else "Waiting")
            print(f"{icon} Step {s['step']}: [{st.upper()}] {s['role_title']} — {s['action']}")
            print(f"   Deliverable: {s['target_output']} ({review})")
        print()

    def print_raw_dashboard(self):
        """Prints the raw Markdown dashboard file to stdout."""
        if DASHBOARD_FILE.exists():
            with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print(f"Dashboard file {DASHBOARD_FILE} does not exist yet. Run with --init first.")

    def watch_dashboard(self, interval: int = 2):
        """Continuously refreshes and renders the live dashboard in the terminal."""
        import time
        print(f"Starting live watch on {DASHBOARD_FILE} (refresh: {interval}s)... Press Ctrl+C to exit.")
        time.sleep(0.5)
        try:
            while True:
                # ANSI clear screen and home cursor
                sys.stdout.write("\033[H\033[J")
                sys.stdout.flush()
                self.status = self._load_status()

                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("================================================================================")
                print(f"  GAMEDEVSTUDIO — LIVE PIPELINE MONITOR   [{now_str}]")
                print("================================================================================")

                if not self.status:
                    print("\n[!] No active pipeline found. Run with --init to start.")
                else:
                    print(f"Workflow : {self.status.get('workflow')}")
                    print(f"Mode     : {self.status.get('mode_description')}")
                    print(f"Pitch    : {self.status.get('user_pitch') or '(Autonomous Synthesis)'}\n")
                    print(f"{'Step':<6} {'Role':<24} {'Status':<14} {'Review':<12} {'Deliverable'}")
                    print("-" * 80)
                    for s in self.status.get("steps", []):
                        st = s.get("status", "Pending")
                        icon = "⚪"
                        if st == "Completed":
                            icon = "🟢"
                        elif st == "In Progress":
                            icon = "🟡"
                        elif st == "Awaiting Review":
                            icon = "🟠"
                        review = "Approved" if s.get("approved") else ("Review Ready" if st == "Completed" else "Waiting")
                        role = s["role_title"][:22]
                        action = s["action"][:30]
                        deliverable = s["target_output"]
                        print(f"{icon} {s['step']:<4} {role:<24} {st:<14} {review:<12} {deliverable}")

                print("\n--------------------------------------------------------------------------------")
                print(f"[Live Auto-Refresh every {interval}s]  •  Press Ctrl+C to exit")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[✓] Exited live watch.")


    def approve_stage(self, stage_number: int):
        target_stage = None
        for stg in MAJOR_STAGES:
            if stg["stage"] == stage_number:
                target_stage = stg
                break
        if not target_stage:
            print(f"Error: Unknown stage {stage_number}. Available: 1, 2, 3, 4")
            return

        for step_num in target_stage["steps"]:
            self.update_step_status(step_num, "Completed", approved=True)

        print(f"\n[✓] Stage {stage_number} ({target_stage['title']}) APPROVED.")
        print(f"Sign-off Gate '{target_stage['gate']}' satisfied.")
        if stage_number < len(MAJOR_STAGES):
            next_stg = MAJOR_STAGES[stage_number]
            print(f"[>] Major Stage {next_stg['stage']} ({next_stg['title']}) is now UNLOCKED and ready for execution.\n")
        else:
            print("[🎉] All 4 Major Stages complete! Final Milestone reached.\n")
        self._save_status()

    def run_step(self, step_number: int, log_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Executes the autonomous agent for a specific step."""
        self.status = self._load_status()
        step = next((s for s in self.status.get("steps", []) if s["step"] == step_number), None)
        if not step:
            print(f"Error: Step {step_number} not found.")
            return False

        step["status"] = "In Progress"
        self._save_status()

        user_pitch = self.status.get("user_pitch")
        success = self.agent_runner.run_step_process(step, user_pitch, log_callback=log_callback or print)

        if success:
            step["status"] = "Awaiting Review"
            step["approved"] = False
            step["completed_at"] = datetime.datetime.now().isoformat()
            self._save_status()
            return True
        else:
            step["status"] = "Failed"
            self._save_status()
            return False

    def run_stage(self, stage_number: int, log_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Runs all steps for a Major Stage sequentially, halting at the sign-off gate."""
        target_stage = next((stg for stg in MAJOR_STAGES if stg["stage"] == stage_number), None)
        if not target_stage:
            print(f"Error: Unknown stage {stage_number}. Available: 1, 2, 3, 4")
            return False

        print(f"\n================================================================================")
        print(f"  EXECUTING MAJOR STAGE {stage_number}: {target_stage['title'].upper()}")
        print(f"================================================================================")
        print(f"Deliverables Target: {', '.join([str(s) for s in target_stage['steps']])}\n")

        for step_num in target_stage["steps"]:
            self.status = self._load_status()
            s_data = next((s for s in self.status.get("steps", []) if s["step"] == step_num), None)
            if s_data and s_data.get("status") == "Completed" and s_data.get("approved"):
                print(f"• Step {step_num} [{s_data['role_title']}] already completed and approved. Skipping.")
                continue

            print(f"\n[>] Launching autonomous agent: {s_data['role_title']} (Step {step_num})...")
            ok = self.run_step(step_num, log_callback=log_callback or print)
            if not ok:
                print(f"[!] Step {step_num} failed. Halting stage execution.")
                return False

        print(f"\n================================================================================")
        print(f"  MAJOR STAGE {stage_number} COMPLETED — AWAITING USER SIGN-OFF GATE")
        print(f"================================================================================")
        print(f"Sign-off Gate: {target_stage['gate']}")
        print(f"Review your deliverables in deliverables/, then sign off with:")
        print(f"  python3 orchestration/pipeline_runner.py --approve-stage {stage_number}\n")
        return True


def main():
    parser = argparse.ArgumentParser(description="GameDevTeam Background Pipeline Runner")
    parser.add_argument("--init", action="store_true", help="Initialize the pipeline and populate deliverables from templates")
    parser.add_argument("--pitch", nargs="?", const="", default=None, help="Optional pitch idea for the pipeline")
    parser.add_argument("--status", action="store_true", help="View current production status and step deliverables")
    parser.add_argument("--watch", nargs="?", const=2, type=int, default=None, help="Watch live dashboard in real-time (default refresh: 2s)")
    parser.add_argument("--cat", action="store_true", help="Print the raw markdown dashboard to stdout")
    parser.add_argument("--run-stage", type=int, help="Execute autonomous agents for a Major Stage (1-4)")
    parser.add_argument("--run-step", type=int, help="Execute autonomous agent for an individual step (1-8)")
    parser.add_argument("--approve-step", type=int, help="Approve and mark a step deliverable as reviewed")
    parser.add_argument("--approve-stage", type=int, help="Approve an entire Major Stage (1-4) and unlock next stage")
    parser.add_argument("--complete-step", type=int, help="Mark a step as completed")

    args = parser.parse_args()
    runner = PipelineRunner()

    if args.init:
        runner.init_pipeline(args.pitch)
        return

    if args.run_stage:
        runner.run_stage(args.run_stage)
        return

    if args.run_step:
        runner.run_step(args.run_step)
        return

    if args.watch is not None:
        runner.watch_dashboard(interval=args.watch)
        return

    if args.cat:
        runner.print_raw_dashboard()
        return

    if args.approve_stage:
        runner.approve_stage(args.approve_stage)
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

    if args.status or len(sys.argv) == 1:
        runner.print_status()
        return


if __name__ == "__main__":
    main()
