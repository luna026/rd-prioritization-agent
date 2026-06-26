"""
app.py — Full multi-agent pipeline for the R&D Experiment Prioritization Agent.

This is the main entry point for the Kaggle capstone demonstration.
It chains 4 agents: Intake → Context → Prioritization → Report.

Course concepts demonstrated:
1. Multi-agent system (ADK-style orchestration)
2. MCP server (src/tools/mcp_server.py exposes tools)
3. Security features (guardrails.py, input validation, output sanitization)

Run:
    python app.py
    python app.py --goal "what should we run next to improve alignment"
"""
import argparse
from rich.console import Console
from rich.rule import Rule
from rich.panel import Panel

from src.agents.intake_agent import run_intake_agent
from src.agents.context_agent import run_context_agent
from src.agents.prioritization_agent import run_prioritization_agent
from src.agents.report_agent import run_report_agent

console = Console()

DEFAULT_GOAL = "recommend the next best experiments to improve particle alignment while keeping stability above threshold"


def run_pipeline(user_goal: str):
    console.print(Panel.fit(
        "[bold cyan]R&D Experiment Prioritization Agent[/bold cyan]\n"
        "[dim]Agents for Business — Kaggle Capstone[/dim]",
        border_style="cyan"
    ))

    # ── Agent 1: Intake ────────────────────────────────────────────────
    console.print(Rule("[bold]Agent 1: Intake[/bold] — Validating request"))
    intake_result = run_intake_agent(user_goal)

    if not intake_result.get("valid", False):
        console.print(f"[red]Request rejected:[/red] {intake_result.get('rejection_reason')}")
        return

    goal = intake_result["goal_rephrased"]
    console.print(f"[green]✓ Valid request[/green] | Intent: [bold]{intake_result['intent']}[/bold]")
    console.print(f"[dim]Rephrased goal:[/dim] {goal}\n")

    # ── Agent 2: Context ───────────────────────────────────────────────
    console.print(Rule("[bold]Agent 2: Context[/bold] — Loading project knowledge"))
    context = run_context_agent(goal)
    console.print("[green]✓ Context built[/green]")
    console.print(f"\n[bold]LLM context analysis:[/bold]\n{context['llm_analysis']}\n")

    # ── Agent 3: Prioritization ────────────────────────────────────────
    console.print(Rule("[bold]Agent 3: Prioritization[/bold] — Ranking next experiments"))
    prioritization = run_prioritization_agent(context)
    console.print("[green]✓ Experiments ranked[/green]")
    console.print(f"\n[bold]Ranking explanation:[/bold]\n{prioritization['ranking_explanation']}\n")

    # ── Agent 4: Report ────────────────────────────────────────────────
    console.print(Rule("[bold]Agent 4: Report[/bold] — Writing decision memo"))
    memo = run_report_agent(context, prioritization)
    console.print("[green]✓ Memo generated[/green]\n")

    console.print(Panel(memo, title="[bold]Decision Memo[/bold]", border_style="green"))
    console.print("\n[dim]Outputs saved to output/sample_report.md and output/sample_ranked_experiments.json[/dim]")
    console.print(Rule("[bold green]Pipeline complete[/bold green]"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the R&D Experiment Prioritization Agent")
    parser.add_argument("--goal", type=str, default=DEFAULT_GOAL, help="Planning goal text")
    args = parser.parse_args()
    run_pipeline(args.goal)
