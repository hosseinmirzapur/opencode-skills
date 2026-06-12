"""Interactive LLM provider configuration wizard."""

import getpass
import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

from osk.config import load_user_config, save_user_config

console = Console()


def run_provider_wizard() -> dict:
    """Interactive wizard to add LLM API providers."""
    cfg = load_user_config()

    console.print()
    console.print(Panel.fit(
        "[bold]🔑 API Provider Configuration[/]\n"
        "[dim]Add the LLM providers opencode will use for skills and agents.[/dim]\n"
        "[dim]You can always add more later with [bold]osk config providers[/][/dim]",
        box=box.ROUNDED,
        border_style="bright_magenta",
    ))

    if "provider" not in cfg:
        cfg["provider"] = {}

    while True:
        console.print()
        name = Prompt.ask("  [bold]Provider identifier[/]", default="my-provider")
        label = Prompt.ask("  [bold]Display name[/]", default=name.title().replace("-", " "))
        base_url = Prompt.ask("  [bold]API base URL[/]", default="https://api.openai.com/v1")

        console.print("  [dim]Enter API key (input will be masked)[/]")
        console.print("  [bold yellow]?[/] API key:", end=" ")
        api_key = getpass.getpass("")

        console.print()
        model_id = Prompt.ask("  [bold]Model ID[/]", default="gpt-4o-mini")
        model_label = Prompt.ask("  [bold]Model label[/]", default="GPT-4o Mini")

        provider_id = name.lower().replace(" ", "-")

        opts = {"baseURL": base_url}
        if api_key:
            opts["apiKey"] = api_key

        cfg["provider"][provider_id] = {
            "name": label,
            "npm": "@ai-sdk/openai-compatible",
            "options": opts,
            "models": {
                model_id: {"name": model_label},
            },
        }

        console.print(f"  [bold green]✓[/] Provider [bold]{label}[/] added")

        if not Confirm.ask("  [bold]Add another provider?[/]", default=False):
            break

    save_user_config(cfg)
    console.print()
    console.print(Panel(
        f"[bold green]✓[/] {len(cfg['provider'])} provider(s) configured\n"
        f"[dim]Edit anytime: ~/.config/opencode/opencode.json[/]",
        box=box.ROUNDED,
        border_style="green",
    ))
    return cfg["provider"]


def show_providers() -> None:
    """Display currently configured providers."""
    from osk.config import get_providers
    providers = get_providers()

    if not providers:
        console.print("[yellow]No providers configured yet.[/]")
        console.print("[dim]Run [bold]osk config providers[/] to add one.[/]")
        return

    from rich.table import Table
    table = Table(
        box=box.ROUNDED,
        border_style="bright_magenta",
        title="Configured Providers",
        title_style="bold",
    )
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Base URL", style="dim")
    table.add_column("Models", style="green")

    for pid, p in providers.items():
        models = ", ".join(p.get("models", {}).keys()) or "—"
        base = p.get("options", {}).get("baseURL", "—")
        table.add_row(pid, p.get("name", pid), base, models)

    console.print(table)
