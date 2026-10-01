#!/usr/bin/env python3
"""
CLI runner for GameDevTeam Orchestration.
Usage:
    python3 run_orchestration.py --list
    python3 run_orchestration.py --workflows
    python3 run_orchestration.py --role producer
    python3 run_orchestration.py --prompt "We need a player movement controller"
"""

import argparse
import json
import sys
from pathlib import Path
from orchestrator import GameDevOrchestrator

def main():
    parser = argparse.ArgumentParser(description="GameDevTeam Multi-Agent Orchestration CLI")
    parser.add_argument("--list", action="store_true", help="List all 9 team roles and descriptions")
    parser.add_argument("--workflows", action="store_true", help="List predefined multi-agent workflows")
    parser.add_argument("--role", type=str, help="Show detailed spec for a specific role (e.g. producer, lead_programmer)")
    parser.add_argument("--workflow", type=str, help="Show step-by-step breakdown for a workflow (e.g. pitch_to_prototype)")
    parser.add_argument("--prompt", type=str, help="Identify which roles should respond to a given prompt")
    parser.add_argument("--subagent-spec", type=str, help="Generate subagent prompt JSON for a given role ID")

    args = parser.parse_args()
    orchestrator = GameDevOrchestrator()

    if args.list or len(sys.argv) == 1:
        orchestrator.print_team_status()
        return

    if args.workflows:
        print("\nAvailable Predefined Workflows:\n")
        for key, wf in orchestrator.workflows.items():
            print(f"• ID: '{key}' — {wf['name']}")
            print(f"  Description: {wf['description']}")
            print(f"  Total Steps: {len(wf['steps'])}\n")
        return

    if args.role:
        role = orchestrator.get_role(args.role)
        if not role:
            print(f"Error: Unknown role '{args.role}'. Available: {list(orchestrator.roles.keys())}")
            sys.exit(1)
        print(json.dumps(role, indent=2))
        return

    if args.workflow:
        wf = orchestrator.get_workflow(args.workflow)
        if not wf:
            print(f"Error: Unknown workflow '{args.workflow}'. Available: {list(orchestrator.workflows.keys())}")
            sys.exit(1)
        print(f"\nWorkflow: {wf['name']}")
        print(f"Description: {wf['description']}\n")
        for s in wf["steps"]:
            print(f"Step {s['step']}: [{s['role']}] {s['action']}")
            print(f"  Target Output: {s['output']}")
            print(f"  Notes: {s['notes']}\n")
        return

    if args.prompt:
        matches = orchestrator.find_role_by_trigger(args.prompt)
        print(f"Prompt: \"{args.prompt}\"")
        if matches:
            print(f"Triggered Roles: {', '.join(matches)}")
        else:
            print("No specific trigger matched. Producer default escalation recommended.")
        return

    if args.subagent_spec:
        try:
            spec = orchestrator.get_subagent_spec(args.subagent_spec)
            print(json.dumps(spec, indent=2))
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
