from __future__ import annotations

import argparse
import sys

from .agent import ClosiraAgent
from .config import load_settings
from .formatting import format_summary, format_turn
from .openai_client import OpenAIWorkflowClient
from .scenarios import SCENARIOS, scenario_choices
from .sop import load_sop


def build_agent() -> ClosiraAgent:
    sop = load_sop()
    settings = load_settings()
    if not settings.api_key_present:
        raise RuntimeError("OPENAI_API_KEY is not set. Export it or create a .env file.")
    return ClosiraAgent(sop=sop, workflow_client=OpenAIWorkflowClient(model=settings.model))


def chat(args: argparse.Namespace) -> int:
    agent = build_agent()
    print("Closira AI support workflow. Type /summary to end and summarize, or /exit to quit.")
    while True:
        try:
            message = input("Customer: ").strip()
        except EOFError:
            message = "/summary"
        if not message:
            continue
        if message == "/exit":
            return 0
        if message == "/summary":
            print(format_summary(agent.summarize()))
            return 0
        result = agent.handle_customer_message(message)
        print(format_turn(result))


def run_scenario(args: argparse.Namespace) -> int:
    scenario = SCENARIOS[args.name]
    agent = build_agent()
    print(render_scenario(scenario.title, scenario.messages, agent))
    return 0


def render_scenario(title: str, messages: list[str], agent: ClosiraAgent) -> str:
    lines = [f"# {title}", ""]
    for message in messages:
        lines.append(f"Customer: {message}")
        result = agent.handle_customer_message(message)
        lines.append(format_turn(result))
        lines.append("")
    lines.append(format_summary(agent.summarize()))
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Closira AI support workflow")
    subparsers = parser.add_subparsers(dest="command", required=True)

    chat_parser = subparsers.add_parser("chat", help="Run an interactive customer conversation")
    chat_parser.set_defaults(func=chat)

    scenario_parser = subparsers.add_parser("run-scenario", help="Run a scripted assignment scenario")
    scenario_parser.add_argument("name", choices=sorted(SCENARIOS), help=f"Scenario name: {scenario_choices()}")
    scenario_parser.set_defaults(func=run_scenario)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        return args.func(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
