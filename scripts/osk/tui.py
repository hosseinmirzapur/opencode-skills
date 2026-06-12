"""Textual-based interactive TUI for osk — full-screen component manager.

This module is imported lazily only when the user runs `osk` without args
and `textual` is available.
"""

from pathlib import Path
from typing import ClassVar

from rich.text import Text
from rich.style import Style
from rich.table import Table
from rich import box

from osk.assets import Theme
from osk.installer import (
    ensure_repo,
    update_repo,
    install_all,
    install_graphify_flow,
    install_npm_deps,
    get_cmd_version,
    get_installed_count,
    is_graphify_installed,
    copy_component,
)
from osk.config import load_user_config, load_project_config
from osk.registry import get_components, ComponentGroup
from osk.sync import component_installed, check_outdated
from osk.providers import run_provider_wizard


def launch_tui():
    """Launch the Textual TUI (entry point)."""
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
        from textual.widgets import Header, Footer, Static, Button, Label, ListView, ListItem, TabbedContent, TabPane
        from textual.screen import Screen
        from textual.binding import Binding
        from textual.reactive import reactive
        from textual.widgets._toggle_button import ToggleButton
    except ImportError:
        print("Textual TUI requires 'textual' library.")
        print("Install: pip install textual")
        return

    # ── Re-import within the guard ───────────────────────────────────

    class OSKApp(App):
        TITLE = "⚡ opencode-skills"
        SUB_TITLE = f"v1.0.0 · {get_cmd_version('graphify') or 'graphify not installed'}"

        SCREENS: ClassVar[dict[str, type[Screen]]] = {}
        CSS = """
        Screen {
            background: #0f0f1a;
        }

        #dashboard {
            padding: 1;
            height: 100%;
        }

        StatusBar {
            background: #1a1a2e;
            color: #64748b;
            dock: bottom;
            padding: 0 1;
            height: 1;
        }

        DashboardTitle {
            background: #0f0f1a;
            color: #a855f7;
            text-style: bold;
            padding: 1 2;
            height: 3;
        }

        .stat-box {
            background: #1a1a2e;
            border: solid #4a4a7a;
            padding: 1 2;
            margin: 0 1;
            min-width: 20;
        }

        .stat-value {
            color: #22d3ee;
            text-style: bold;
        }

        .stat-label {
            color: #64748b;
        }

        Button {
            background: #a855f7;
            color: #ffffff;
            margin: 0 1;
        }

        Button:hover {
            background: #9333ea;
        }

        Button:focus {
            border: solid #22d3ee;
        }

        #action-panel {
            background: #1a1a2e;
            border: solid #4a4a7a;
            padding: 1;
            margin: 1 0;
        }

        #component-list {
            background: #1a1a2e;
            border: solid #4a4a7a;
            padding: 1;
            margin: 1 0;
            height: 60%;
        }

        ListView {
            background: #1a1a2e;
        }

        ListItem {
            padding: 0 1;
        }

        ListItem:hover {
            background: #2a2a3e;
        }

        ListView:focus .list-item--focused {
            background: #2a2a3e;
        }

        TabbedContent {
            background: #1a1a2e;
            border: solid #4a4a7a;
        }

        TabPane {
            padding: 1;
        }
        """

        def compose(self) -> ComposeResult:
            from textual.widgets import Header, Footer
            yield Header(show_clock=True)
            yield Container(
                ScrollableContainer(
                    DashboardScreen(),
                    id="dashboard",
                ),
            )
            yield Footer()

        def on_mount(self) -> None:
            self.title = "⚡ opencode-skills — Agent Skill Hub"
            self.sub_title = f"v1.0.0"

    # ── Dashboard Screen ─────────────────────────────────────────────

    class DashboardScreen(Static):
        """Main dashboard showing status and actions."""

        def compose(self) -> ComposeResult:
            from textual.containers import Horizontal, Vertical
            from textual.widgets import Static, Button

            yield Static("[bold]📊 Installation Status[/]", id="status-title")
            yield Horizontal(
                Static("", id="stats-skills"),
                Static("", id="stats-plugins"),
                Static("", id="stats-agents"),
                Static("", id="stats-graphify"),
            )
            yield Static("")
            yield Static("[bold]⚡ Quick Actions[/]", id="actions-title")
            yield Horizontal(
                Button("Install All", id="btn-install", variant="primary"),
                Button("Update", id="btn-update"),
                Button("Upgrade", id="btn-upgrade"),
                Button("Providers", id="btn-providers"),
                Button("Doctor", id="btn-doctor"),
                Button("Quit", id="btn-quit", variant="error"),
            )
            yield Static("")
            yield Static("[bold]📦 Component Browser[/]", id="browser-title")
            yield Static("", id="component-list-output")

        def on_mount(self) -> None:
            self.refresh_stats()

        def refresh_stats(self) -> None:
            repo = ensure_repo()
            groups = get_components(repo)
            installed = get_installed_count(groups)

            skills_count = installed.get("skills", 0)
            plugins_count = installed.get("plugins", 0)
            agents_count = installed.get("agents", 0)
            skills_total = sum(len(g.components) for g in groups if g.kind == "skills")
            plugins_total = sum(len(g.components) for g in groups if g.kind == "plugins")
            agents_total = sum(len(g.components) for g in groups if g.kind == "agents")
            graphify_ok = is_graphify_installed()

            # Update stat boxes via Rich render
            skills_box = Table.grid(padding=(0, 2))
            skills_box.add_row(
                Text(f"\n{skills_count}/{skills_total}", style="bold cyan"),
                Text("\nSkills", style="dim"),
            )
            self.query_one("#stats-skills").update(Panel(
                skills_box, box=box.ROUNDED, border_style="bright_magenta",
            ))

            plugins_box = Table.grid(padding=(0, 2))
            plugins_box.add_row(
                Text(f"\n{plugins_count}/{plugins_total}", style="bold cyan"),
                Text("\nPlugins", style="dim"),
            )
            self.query_one("#stats-plugins").update(Panel(
                plugins_box, box=box.ROUNDED, border_style="cyan",
            ))

            agents_box = Table.grid(padding=(0, 2))
            agents_box.add_row(
                Text(f"\n{agents_count}/{agents_total}", style="bold cyan"),
                Text("\nAgents", style="dim"),
            )
            self.query_one("#stats-agents").update(Panel(
                agents_box, box=box.ROUNDED, border_style="green",
            ))

            g_icon = "✓" if graphify_ok else "✗"
            g_color = "green" if graphify_ok else "red"
            g_ver = get_cmd_version("graphify").split("\n")[0] if graphify_ok else "not installed"
            graphify_box = Table.grid(padding=(0, 2))
            graphify_box.add_row(
                Text(f"\n{g_icon} {g_ver}", style=f"bold {g_color}"),
                Text("\nGraphify", style="dim"),
            )
            self.query_one("#stats-graphify").update(Panel(
                graphify_box, box=box.ROUNDED, border_style=g_color,
            ))

            # Component list
            comp_text = Text()
            for group in groups:
                comp_text.append(f"\n{group.icon} {group.label}\n", style="bold magenta")
                for comp in group.components[:8]:  # show first 8
                    installed = component_installed(comp)
                    icon = "✓" if installed else "·"
                    color = "green" if installed else "dim"
                    comp_text.append(f"  [{color}]{icon}[/] {comp.label}\n")
                if len(group.components) > 8:
                    comp_text.append(f"  [dim]... and {len(group.components) - 8} more[/]\n")

            self.query_one("#component-list-output").update(Panel(
                comp_text, box=box.ROUNDED, border_style="bright_magenta",
                title="Components",
            ))

        def on_button_pressed(self, event: Button.Pressed) -> None:
            repo = ensure_repo()
            groups = get_components(repo)

            if event.button.id == "btn-install":
                install_all(repo, groups)
                install_npm_deps()
                install_graphify_flow()
                self.refresh_stats()
            elif event.button.id == "btn-update":
                update_repo(repo)
                self.refresh_stats()
            elif event.button.id == "btn-upgrade":
                updated = 0
                for group in groups:
                    for comp in group.components:
                        if component_installed(comp) and check_outdated(comp, repo):
                            if copy_component(comp, repo):
                                updated += 1
                if updated > 0:
                    self.notify(f"Upgraded {updated} component(s)", severity="information")
                else:
                    self.notify("Everything is up to date", severity="information")
                self.refresh_stats()
            elif event.button.id == "btn-providers":
                run_provider_wizard()
                self.refresh_stats()
            elif event.button.id == "btn-doctor":
                from osk.cli import doctor
                # Run the doctor CLI command
            elif event.button.id == "btn-quit":
                self.app.exit()

    # ── Run ───────────────────────────────────────────────────────────
    app = OSKApp()
    app.run()
