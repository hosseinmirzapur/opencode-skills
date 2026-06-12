#!/usr/bin/env python3
"""Click-based CLI for osk — OpenCode Skills Manager."""

import sys
from pathlib import Path

import click
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Confirm

from osk import __version__
from osk.assets import Theme, LOGO_SMALL, ICON_OK, ICON_WARN, ICON_ERROR, ICON_SKIP, ICON_BULLET
from osk.config import load_user_config, load_project_config
from osk.installer import (
    ensure_repo,
    update_repo,
    install_all,
    install_graphify_flow,
    install_npm_deps,
    register_graphify,
    uninstall_component,
    find_repo_root,
    get_cmd_version,
    get_installed_count,
    is_graphify_installed,
    shutil_which,
)
from osk.providers import run_provider_wizard, show_providers
from osk.registry import get_components, search_components, ComponentGroup
from osk.sync import component_installed, check_outdated
from osk.ui import (
    console,
    status_panel,
    section_header,
    component_table,
    success_panel,
    error_panel,
    wizard_header,
)


def _bootstrap_rich():
    """Ensure rich is available before anything else."""
    try:
        from rich.console import Console
        return
    except ImportError:
        pass
    import subprocess
    for cmd in [
        [sys.executable, "-m", "pip", "install", "rich", "--user", "-q"],
        [sys.executable, "-m", "pip", "install", "rich", "-q"],
    ]:
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=30)
            break
        except Exception:
            continue


_bootstrap_rich()


def _repo() -> Path:
    """Get the repo root, cloning if necessary."""
    root = find_repo_root()
    if root:
        return root
    return ensure_repo()


def _print_logo():
    console.print(LOGO_SMALL)


# ── Main group ──────────────────────────────────────────────────────────

@click.group(invoke_without_command=True)
@click.version_option(__version__, prog_name="osk")
@click.pass_context
def main(ctx: click.Context):
    """⚡ opencode-skills — the ultimate agent skill hub CLI"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(status)


# ── status ──────────────────────────────────────────────────────────────

@main.command()
def status():
    """Show installation status of all components."""
    _print_logo()
    repo = _repo()
    groups = get_components(repo)
    installed = get_installed_count(groups)

    console.print()

    # Environment status
    env_items = [
        ("🐍", "Python  ", f"[green]{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}[/]"),
    ]
    for name, cmd in [("uv", "uv"), ("Node.js", "node"), ("Git", "git")]:
        ver = get_cmd_version(cmd)
        if ver:
            icon, label = ICON_OK, name
            env_items.append((icon, f"{label:<8}", f"[green]{ver.split(chr(10))[0]}[/]"))
        else:
            env_items.append((ICON_WARN, f"{name:<8}", "[yellow]not found[/]"))

    # Graphify
    if is_graphify_installed():
        ver = get_cmd_version("graphify")
        env_items.append((ICON_OK, "Graphify", f"[green]{ver.split(chr(10))[0]}[/]"))
    else:
        env_items.append((ICON_WARN, "Graphify", "[yellow]not installed[/]"))

    console.print(status_panel(env_items, "Environment"))

    # Component status per group
    for group in groups:
        rows = []
        for comp in group.components:
            if component_installed(comp):
                outdated = check_outdated(comp, repo)
                icon = ICON_WARN if outdated else ICON_OK
                status_text = "[yellow]outdated[/]" if outdated else "[green]installed[/]"
            else:
                icon = ICON_SKIP
                status_text = "[dim]not installed[/]"
            rows.append((icon, comp.label, status_text))
        if rows:
            console.print()
            console.print(component_table(rows, title=f"{group.icon}  {group.label}"))

    console.print()


# ── install ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("component", required=False, default="all")
@click.option("--repo-only", is_flag=True, help="Install from cached repo only (no clone)")
def install(component: str, repo_only: bool):
    """Install components: all, skills, plugins, agents, graphify, config."""
    if component == "graphify":
        _print_logo()
        install_graphify_flow()
        return

    repo = _repo()
    groups = get_components(repo)

    if component == "all":
        _print_logo()
        console.print(wizard_header("Installing Components"))
        install_all(repo, groups)
        install_npm_deps()
        install_graphify_flow()
        return

    # Filter by kind
    filtered = [g for g in groups if g.kind == component]
    if not filtered:
        console.print(error_panel(
            f"Unknown component type: '{component}'",
            f"Try: all, skills, plugins, agents, config, graphify",
        ))
        return

    _print_logo()
    console.print(wizard_header(f"Installing {component}"))
    install_all(repo, filtered)


# ── uninstall ───────────────────────────────────────────────────────────

@main.command()
@click.argument("component_id")
def uninstall(component_id: str):
    """Uninstall a component by ID (e.g. skill/ab-testing)."""
    repo = _repo()
    groups = get_components(repo)

    kind, _, name = component_id.partition("/")
    target = None
    for group in groups:
        if group.kind == kind or kind == "":
            for comp in group.components:
                if comp.id == component_id or comp.label == name:
                    target = comp
                    break

    if not target:
        console.print(error_panel(f"Component not found: '{component_id}'"))
        return

    if not component_installed(target):
        console.print(f"[yellow]~[/] {target.label} is not installed")
        return

    if Confirm.ask(f"  Remove [bold]{target.label}[/]?"):
        if uninstall_component(target):
            console.print(f"  [green]✓[/] {target.label} removed")
        else:
            console.print(f"  [red]✗[/] Failed to remove {target.label}")


# ── update ──────────────────────────────────────────────────────────────

@main.command()
def update():
    """Pull the latest repo changes."""
    _print_logo()
    repo = _repo()
    console.print()
    if update_repo(repo):
        console.print("  [green]✓[/] Repository updated")
    else:
        console.print("  [yellow]~[/] Already up to date")


# ── upgrade ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("component", required=False, default="all")
def upgrade(component: str):
    """Upgrade installed components to latest."""
    if component == "graphify":
        _print_logo()
        console.print("[yellow]~[/] Reinstalling graphify...")
        from osk.installer import install_graphify
        if install_graphify():
            console.print("  [green]✓[/] graphify upgraded")
        return

    repo = _repo()
    update_repo(repo)
    groups = get_components(repo)

    _print_logo()
    console.print(wizard_header("Upgrading Components"))

    upgraded = 0
    for group in groups:
        if component != "all" and group.kind != component:
            continue
        for comp in group.components:
            if component_installed(comp) and check_outdated(comp, repo):
                from osk.installer import copy_component
                if copy_component(comp, repo):
                    console.print(f"  [green]✓[/] {comp.label} upgraded")
                    upgraded += 1

    if upgraded == 0:
        console.print("  [yellow]~[/] Everything is up to date")
    else:
        console.print(f"\n  [green]✓[/] {upgraded} component(s) upgraded")


# ── list ────────────────────────────────────────────────────────────────

@main.command()
@click.option("-a", "--available", is_flag=True, help="Show all available components")
def list_cmd(available: bool):
    """List components."""
    repo = _repo()
    groups = get_components(repo)

    _print_logo()
    console.print()

    for group in groups:
        rows = []
        for comp in group.components:
            installed = component_installed(comp)
            if not available and not installed:
                continue
            icon = ICON_OK if installed else ICON_SKIP
            rows.append((icon, comp.label, comp.description))
        if rows:
            console.print(component_table(rows, title=f"{group.icon}  {group.label}"))
            console.print()


# ── search ──────────────────────────────────────────────────────────────

@main.command()
@click.argument("query")
def search(query: str):
    """Search available components."""
    repo = _repo()
    groups = get_components(repo)
    results = search_components(groups, query)

    if not results:
        console.print(f"[yellow]No results for '{query}'[/]")
        return

    _print_logo()
    console.print()
    table = Table(
        box=box.SIMPLE,
        border_style=Theme.muted,
        show_edge=False,
        padding=(0, 1),
    )
    table.add_column("Type", width=10)
    table.add_column("Name", style="bold")
    table.add_column("Description", style=Theme.muted)

    for comp in results:
        installed = ICON_OK if component_installed(comp) else ICON_SKIP
        desc = comp.description[:60] + "…" if len(comp.description) > 60 else comp.description
        table.add_row(f"{installed}{comp.kind}", comp.label, desc)

    console.print(table)


# ── config ──────────────────────────────────────────────────────────────

@main.command()
@click.argument("action", required=False, default="show")
def config(action: str):
    """Manage configuration: show, providers."""
    if action == "providers":
        run_provider_wizard()
    elif action == "show":
        _print_logo()
        console.print()

        user_cfg = load_user_config()
        project_cfg = load_project_config()

        providers = user_cfg.get("provider", {})
        plugins = project_cfg.get("plugin", [])

        items = [
            (ICON_OK if providers else ICON_WARN, "Providers ", f"{'[green]' + str(len(providers)) + ' configured[/]' if providers else '[yellow]none[/]'}"),
            (ICON_OK if plugins else ICON_SKIP, "Plugins   ", f"{'[green]' + str(len(plugins)) + ' registered[/]' if plugins else '[dim]none[/]'}"),
        ]
        console.print(status_panel(items, "Configuration"))

        if providers:
            console.print(section_header("Providers"))
            for pid, p in providers.items():
                console.print(f"  {ICON_BULLET} [cyan]{pid}[/] → {p.get('name', pid)}")
        if plugins:
            console.print(section_header("Plugins"))
            for p in plugins:
                console.print(f"  {ICON_BULLET} [dim]{p}[/]")
    else:
        console.print(error_panel(f"Unknown config action: '{action}'", "Try: show, providers"))


# ── doctor ──────────────────────────────────────────────────────────────

@main.command()
def doctor():
    """Diagnose the environment and installation."""
    _print_logo()
    repo = _repo()
    groups = get_components(repo)
    installed = get_installed_count(groups)

    console.print()
    console.print(wizard_header("System Diagnostics"))

    checks: list[tuple[str, bool, str]] = []

    # Python
    checks.append(("Python 3.10+", True, sys.version.split()[0]))
    checks.append(("Git installed", shutil_which("git") is not None, ""))
    checks.append(("Node.js installed", shutil_which("node") is not None, ""))
    checks.append(("uv available", shutil_which("uv") is not None or shutil_which("pipx") is not None, ""))
    checks.append(("graphify installed", is_graphify_installed(), get_cmd_version("graphify")))

    # Config files
    user_cfg = load_user_config()
    checks.append(("User config exists", bool(user_cfg), ""))
    checks.append(("Providers configured", bool(user_cfg.get("provider", {})), ""))

    proj_cfg = load_project_config()
    checks.append(("Project config exists", bool(proj_cfg), ""))

    # Components
    for g in groups:
        count = installed.get(g.kind, 0)
        total = len(g.components)
        ok = count > 0
        checks.append((f"{g.icon} {g.label}", ok, f"{count}/{total} installed"))

    table = Table(box=box.ROUNDED, border_style=Theme.border, padding=(0, 1))
    table.add_column("", width=4)
    table.add_column("Check", style="bold")
    table.add_column("Status", width=20)
    table.add_column("Detail", style=Theme.muted)

    for label, ok, detail in checks:
        icon = ICON_OK if ok else ICON_ERROR
        status = "[green]PASS[/]" if ok else "[red]FAIL[/]"
        table.add_row(icon, label, status, detail)

    console.print(table)

    # Final verdict
    failures = sum(1 for _, ok, _ in checks if not ok)
    if failures == 0:
        console.print(success_panel("All checks passed"))
    else:
        console.print(error_panel(f"{failures} issue(s) found"))


# ── init ────────────────────────────────────────────────────────────────

@main.command()
def init():
    """First-run setup wizard (interactive)."""
    _print_logo()
    console.print()
    console.print(wizard_header(
        "Welcome to opencode-skills",
        "This wizard will set up everything you need.",
    ))

    repo = _repo()
    groups = get_components(repo)

    # Step 1: Install components
    console.print(section_header("Step 1: Install Components"))
    if Confirm.ask("  Install all skills, plugins, and agents?", default=True):
        install_all(repo, groups)
        install_npm_deps()

    # Step 2: Graphify
    console.print(section_header("Step 2: Graphify"))
    if Confirm.ask("  Install graphify (code knowledge graph)?", default=True):
        install_graphify_flow()

    # Step 3: Providers
    console.print(section_header("Step 3: API Providers"))
    providers = load_user_config().get("provider", {})
    if not providers:
        if Confirm.ask("  Configure an API provider now?", default=True):
            run_provider_wizard()
    else:
        console.print(f"  [green]✓[/] {len(providers)} provider(s) already configured")

    console.print()
    console.print(success_panel(
        "Setup complete!",
        "Run [bold]osk[/] anytime to check status.\n"
        "Run [bold]osk --help[/] for all commands.",
    ))


def entry():
    """Entry point for the CLI."""
    main()


if __name__ == "__main__":
    entry()
