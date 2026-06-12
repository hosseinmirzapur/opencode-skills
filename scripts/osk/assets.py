"""Visual assets — ASCII art, color theme, banners."""

from rich.style import Style
from rich.color import Color
from rich.text import Text

# ── Color palette -----------------------------------------------------------

class Theme:
    bg: str = "#0f0f1a"
    surface: str = "#1a1a2e"
    border: str = "#4a4a7a"
    primary: str = "#a855f7"
    secondary: str = "#22d3ee"
    accent: str = "#f59e0b"
    success: str = "#22c55e"
    error: str = "#ef4444"
    warn: str = "#f59e0b"
    info: str = "#3b82f6"
    text: str = "#e2e8f0"
    muted: str = "#64748b"

    @classmethod
    def primary_style(cls) -> Style:
        return Style(color=cls.primary, bold=True)

    @classmethod
    def secondary_style(cls) -> Style:
        return Style(color=cls.secondary, bold=True)

    @classmethod
    def success_style(cls) -> Style:
        return Style(color=cls.success)

    @classmethod
    def error_style(cls) -> Style:
        return Style(color=cls.error, bold=True)

    @classmethod
    def warn_style(cls) -> Style:
        return Style(color=cls.warn)

    @classmethod
    def muted_style(cls) -> Style:
        return Style(color=cls.muted)

    @classmethod
    def header_gradient(cls) -> list[tuple[str, str]]:
        return [
            (cls.primary, "  "),
            (cls.secondary, "  "),
            (cls.primary, "  "),
        ]

    @classmethod
    def title_text(cls, label: str) -> Text:
        t = Text(label)
        t.stylize(Style(color=cls.primary, bold=True))
        return t


# ── ASCII art logo ----------------------------------------------------------

LOGO = """
[bold magenta]  ███████[/][bold cyan]╗[/][bold magenta]███████[/][bold cyan]╗[/][bold magenta]██╗[/][bold cyan]  [/][bold magenta]██╗[/][bold cyan]  [/][bold magenta]███████[/][bold cyan]╗[/][bold magenta]██╗[/][bold cyan]  [/][bold magenta]██╗[/][bold cyan]██╗[/][bold cyan]███████[/][bold cyan]╗[/][bold cyan]
[bold magenta]  ██╔════╝[/][bold cyan]╚══[/][bold magenta]███[/][bold cyan]╔╝[/][bold magenta]██║[/][bold cyan]  [/][bold magenta]██║[/][bold cyan]  [/][bold magenta]██╔════╝[/][bold cyan]╚██╗[/][bold cyan]████╔╝[/][bold cyan]██╔════╝[/][bold cyan]
[bold magenta]  ███████╗[/][bold cyan]  [/][bold magenta]███╔╝[/][bold cyan] [/][bold magenta]███████║[/][bold cyan]  [/][bold magenta]███████╗[/][bold cyan] ╚███╔╝[/][bold cyan] ███████╗[/][bold cyan]
[bold magenta]  ╚════██║[/][bold cyan]  [/][bold magenta]███╔╝[/][bold cyan]  [/][bold magenta]██╔══██║[/][bold cyan]  ╚════██║[/][bold cyan] ██╔██╗[/][bold cyan] ╚════██║[/][bold cyan]
[bold magenta]  ███████║[/][bold cyan]  [/][bold magenta]███████╗[/][bold cyan] [/][bold magenta]██║[/][bold cyan]  [/][bold magenta]██║[/][bold cyan]  [/][bold magenta]███████║[/][bold cyan]██╔╝[/][bold cyan] ██╗[/][bold cyan]███████║[/][bold cyan]
[bold magenta]  ╚══════╝[/][bold cyan]  ╚══════╝╚═╝  ╚═╝  ╚══════╝╚═╝  ╚═╝╚══════╝[/][bold cyan]
"""

LOGO_SMALL = """
[bold magenta]  ███████╗[/][bold cyan]██╗[/][bold cyan]  [bold magenta]██╗[/][bold cyan][bold magenta]██╗[/][bold cyan]
[bold magenta]  ██╔════╝[/][bold cyan]██║[/][bold cyan]  [bold magenta]██║[/][bold cyan][bold magenta]██║[/][bold cyan]
[bold magenta]  ███████╗[/][bold cyan]███████║[/][bold cyan][bold magenta]██║[/][bold cyan]
[bold magenta]  ╚════██║[/][bold cyan]██╔══██║[/][bold cyan][bold magenta]╚═╝[/][bold cyan]
[bold magenta]  ███████║[/][bold cyan]██║[/][bold cyan]  [bold magenta]██║[/][bold cyan][bold magenta]██╗[/][bold cyan]
[bold magenta]  ╚══════╝[/][bold cyan]╚═╝[/][bold cyan]  [bold magenta]╚═╝[/][bold cyan][bold magenta]╚═╝[/][bold cyan]
"""

# ── Status icons ------------------------------------------------------------

ICON_OK = "[bold green]✓[/]"
ICON_WARN = "[bold yellow]◷[/]"
ICON_ERROR = "[bold red]✗[/]"
ICON_SKIP = "[dim]─[/]"
ICON_LINK = "[dim]→[/]"
ICON_BULLET = "[dim]•[/]"
ICON_STAR = "[yellow]★[/]"
ICON_ROCKET = "[bold magenta]⚡[/]"

# ── Progress styles ---------------------------------------------------------

PROGRESS_BAR = "{task.percentage:>3.0f}%"
PROGRESS_BAR_STYLE = "bright_magenta"
PROGRESS_COMPLETED_STYLE = "cyan"
PROGRESS_SPINNER = "dots12"
