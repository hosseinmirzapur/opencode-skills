"""Shared Rich UI components — consistent visual language across CLI and TUI."""

from typing import Optional

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.style import Style
from rich.table import Table
from rich.text import Text

from osk.assets import Theme, PROGRESS_BAR_STYLE, PROGRESS_COMPLETED_STYLE

console = Console()


def make_progress(transient: bool = False, disable: bool = False) -> Progress:
    """Create a consistently styled progress bar."""
    return Progress(
        SpinnerColumn(spinner_name="dots12", style=PROGRESS_BAR_STYLE),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(
            bar_width=32,
            style=Style(color=Theme.muted),
            completed_style=Style(color=PROGRESS_COMPLETED_STYLE),
            finished_style=Style(color="green"),
        ),
        TextColumn(PROGRESS_BAR_STYLE),
        TimeRemainingColumn(compact=True, style=Style(color=Theme.muted)),
        TimeElapsedColumn(),
        console=console,
        transient=transient,
        disable=disable,
    )


def status_panel(items: list[tuple[str, str, str]], title: str = "Status") -> Panel:
    """Create a status panel with labeled rows.

    Each item: (icon, label, value)
    """
    t = Text()
    for icon, label, value in items:
        t.append(f"\n  {icon} ")
        t.append(label, style=Theme.muted)
        t.append("  ")
        t.append(value, style="bold")
    return Panel(
        t,
        title=Text(title, style=Theme.primary_style()),
        box=box.ROUNDED,
        border_style=Theme.border,
        padding=(1, 2),
    )


def section_header(text: str) -> Text:
    """A styled section header."""
    return Text(f"\n  {text}", style=Theme.secondary_style())


def component_table(rows: list[tuple[str, str, str]], title: str = "") -> Table:
    """Create a component listing table.

    Each row: (status_icon, name, description)
    """
    table = Table(
        box=box.SIMPLE,
        border_style=Theme.muted,
        title=title,
        title_style=Theme.primary_style(),
        show_edge=False,
        padding=(0, 1),
    )
    table.add_column("", width=4)
    table.add_column("Component", style="bold", no_wrap=True)
    table.add_column("Description", style=Theme.muted)
    for status_icon, name, desc in rows:
        table.add_row(status_icon, name, desc)
    return table


def error_panel(msg: str, detail: str = "") -> Panel:
    """A styled error panel."""
    content = f"[bold red]{msg}[/]"
    if detail:
        content += f"\n[dim]{detail}[/]"
    return Panel(content, box=box.ROUNDED, border_style="red", padding=(1, 2))


def success_panel(msg: str, detail: str = "") -> Panel:
    """A styled success panel."""
    content = f"[bold green]{msg}[/]"
    if detail:
        content += f"\n[dim]{detail}[/]"
    return Panel(content, box=box.ROUNDED, border_style="green", padding=(1, 2))


def info_panel(msg: str, title: str = "") -> Panel:
    """A styled info panel."""
    return Panel(
        msg,
        title=title or None,
        box=box.ROUNDED,
        border_style=Theme.info,
        padding=(1, 2),
    )


def banner_text() -> Text:
    """Return the main app logo as styled text."""
    logo = """
███████╗██╗  ██╗██╗
██╔════╝██║  ██║██║
███████╗███████║██║
╚════██║██╔══██║╚═╝
███████║██║  ██║██╗
╚══════╝╚═╝  ╚═╝╚═╝
"""
    t = Text(logo)
    t.stylize(Style(color=Theme.primary))
    return t


def wizard_header(title: str, subtitle: str = "") -> Panel:
    """Header panel for wizard screens."""
    content = Text()
    content.append(f"\n  {title}\n", style=Theme.primary_style())
    if subtitle:
        content.append(f"  {subtitle}", style=Theme.muted_style())
    return Panel(
        content,
        box=box.ROUNDED,
        border_style=Theme.border,
        padding=(1, 2),
    )
