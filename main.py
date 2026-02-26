#!/usr/bin/env python3
"""
🔴💀 ULTIMATE AUTONOMOUS RED TEAM ARSENAL — CLI Entry Point
python main.py run "your request" --target example.com
"""
import sys
import time
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import box
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(rich_markup_mode="rich")
console = Console()

BANNER = """[bold red]
██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗
██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║
██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
[/bold red]
[dim]🔴💀 Ultimate Autonomous Red Team Arsenal v1.0[/dim]
[dim]Compiled for Rick Jefferson / RJ Business Solutions[/dim]
[dim]Powered by: Infermatic AI · HuggingFace · Cloudflare[/dim]
"""


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print(BANNER)
        console.print("[bold yellow]Commands: run | models | agents | research | serve[/bold yellow]")


@app.command()
def run(
    request: str = typer.Argument(..., help="The red team task to execute"),
    target: Optional[str] = typer.Option(None, "--target", "-t", help="Target IP/domain"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Preferred LLM model ID"),
    cost: str = typer.Option("mid", "--cost", "-c", help="Cost tier: cheap|mid|premium"),
    authorized: bool = typer.Option(False, "--authorized", help="Confirm you own/have permission on target"),
    infinite: bool = typer.Option(False, "--infinite", "-i", help="Infinite loop mode — set and forget until penetration"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Save report to file"),
):
    """🔴💀 Run an autonomous red team task."""
    console.print(BANNER)
    console.print(Panel(
        f"[bold yellow]Request:[/bold yellow] {request}\n[bold cyan]Target:[/bold cyan] {target or 'Not specified'}\n[bold green]Model:[/bold green] {model or 'Auto-select'}\n[bold magenta]Cost:[/bold magenta] {cost}\n[bold red]Authorized:[/bold red] {authorized}",
        title="🔴 Mission Brief", border_style="red",
    ))

    def on_update(event):
        src = event.get("source", "system").upper()
        msg = event.get("message", "")
        colors = {"SYSTEM": "bold white", "PLANNER": "bold cyan", "EXECUTOR": "bold yellow", "ORCHESTRATOR": "bold red", "REPORTER": "bold green", "CLOUDFLARE": "bold blue", "DOCKER": "bold magenta", "SECURITY": "bold orange3"}
        color = colors.get(src, "white")
        console.print(f"  [{color}]▶ [{src}][/{color}] {msg}")

    console.print("\n[bold red]⚡ Launching Orchestrator...[/bold red]\n")
    from core.orchestrator import Orchestrator
    orc = Orchestrator(cost_preference=cost, preferred_model=model, on_update=on_update)

    start = time.time()
    try:
        if infinite:
            from core.continuous_orchestrator import ContinuousOrchestrator
            cont_orc = ContinuousOrchestrator(orc)
            import asyncio
            result = asyncio.run(cont_orc.run_mission(request, target, infinite=True, authorized=authorized))
        else:
            result = orc.run(request, target=target, authorized=authorized)
            
        elapsed = time.time() - start
        console.print(f"\n[bold green]✅ Task complete in {elapsed:.1f}s | Session: {result.get('session_id')}[/bold green]")

        findings = result.get("findings", [])
        if findings:
            table = Table(title="🔍 Findings", box=box.ROUNDED, border_style="red")
            table.add_column("Severity", style="bold")
            table.add_column("Title")
            table.add_column("Agent")
            sev_colors = {"CRITICAL": "red", "HIGH": "orange1", "MEDIUM": "yellow", "LOW": "green", "INFO": "blue"}
            for f in findings:
                sev = f.get("severity", "?")
                table.add_row(f"[{sev_colors.get(sev,'white')}]{sev}[/]", f.get("title", "?"), f.get("agent", "?"))
            console.print(table)

        report = result.get("report", "")
        if output:
            with open(output, "w") as f:
                f.write(report)
            console.print(f"[bold green]📄 Report saved: {output}[/bold green]")
        else:
            console.print("\n[bold]--- REPORT PREVIEW ---[/bold]")
            console.print(Markdown(report[:2000]))
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def models():
    """List all available models."""
    from models.model_catalog import INFERMATIC_MODELS, HUGGINGFACE_MODELS
    console.print(Panel("[bold red]Available Models[/bold red]", border_style="red"))
    table = Table(box=box.SIMPLE)
    table.add_column("Model ID", style="bold cyan")
    table.add_column("Provider")
    table.add_column("Cost Tier")
    table.add_column("Specialties")
    for m in INFERMATIC_MODELS:
        table.add_row(m.model_id, "Infermatic", m.cost_tier, ", ".join(m.specialties[:3]))
    for m in HUGGINGFACE_MODELS[:5]:
        table.add_row(m.model_id, "HuggingFace", m.cost_tier, ", ".join(m.specialties[:3]))
    console.print(table)


@app.command()
def agents():
    """List all available red team agents."""
    from core.team_selector import AGENT_REGISTRY
    table = Table(title="⚔️ Red Team Arsenal", box=box.SIMPLE)
    table.add_column("Agent", style="bold")
    table.add_column("Tier")
    table.add_column("Autonomy")
    table.add_column("Best For")
    for k, v in AGENT_REGISTRY.items():
        tier_badge = {1: "🏆 T1", 2: "🥈 T2", 3: "🥉 T3", 0: "⚙️  INT"}.get(v.get("tier", 0), "?")
        table.add_row(v["name"], tier_badge, "⭐" * v.get("autonomy", 0), ", ".join(v.get("task_types", [])[:2]))
    console.print(table)


@app.command()
def research(query: str, max_results: int = 10):
    """Search academic databases."""
    from knowledge.research_agent import ResearchAgent
    console.print(f"[bold cyan]🔍 Researching:[/bold cyan] {query}\n")
    ra = ResearchAgent()
    results = ra.search_all(query, max_results=max_results)
    for r in results[:10]:
        console.print(f"[bold]{r.get('title', '?')}[/bold]")
        console.print(f"  [dim]{r.get('source')} | {r.get('published','?')[:10]}[/dim]")
        console.print(f"  {r.get('summary','')[:150]}...\n")


@app.command()
def serve(port: int = 8888):
    """Start the REST API server for the dashboard."""
    import uvicorn
    console.print(f"[bold green]🚀 API server on port {port}...[/bold green]")
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    app()
