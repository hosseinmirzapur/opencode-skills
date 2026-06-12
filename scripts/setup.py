#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  osk — OpenCode Skills CLI                                  ║
║  One-line: curl -fsSL https://raw.githubusercontent.com/    ║
║  hosseinmirzapur/opencode-skills/main/scripts/setup.py |    ║
║  python3                                                    ║
╚══════════════════════════════════════════════════════════════╝

Thin bootstrap: ensures Python deps are available, then delegates to `osk`.
"""

import os
import sys
import subprocess
from pathlib import Path


def _bootstrap(minimal: bool = False):
    """Ensure `osk` is available — install dependencies and the package."""

    # 1. Install core deps
    deps = ["rich>=13.0.0", "click>=8.1.0", "pyfiglet>=1.0.0"]
    missing = []
    for dep in deps:
        pkg = dep.split(">=")[0].split("==")[0]
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing.append(dep)

    if missing:
        print("\033[1;33m📦 Installing dependencies...\033[0m")
        for cmd in [
            [sys.executable, "-m", "pip", "install", *missing, "--user", "-q"],
            [sys.executable, "-m", "pip", "install", *missing, "-q"],
            ["uv", "pip", "install", *missing, "-q"],
        ]:
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=60)
                break
            except Exception:
                continue

    if minimal:
        return

    # 2. Install osk itself if running from source
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    if (repo_root / "scripts" / "osk" / "cli.py").is_file() and (repo_root / "scripts" / "pyproject.toml").is_file():
        try:
            from osk import cli
            return  # already importable
        except ImportError:
            pass

        # Install in editable mode
        print("\033[1;33m📦 Installing osk CLI...\033[0m")
        for cmd in [
            [sys.executable, "-m", "pip", "install", "-e", str(script_dir), "--user", "-q"],
            [sys.executable, "-m", "pip", "install", "-e", str(script_dir), "-q"],
        ]:
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=60)
                break
            except Exception:
                continue


def main():
    _bootstrap()

    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm
    from rich import box

    console = Console()

    # Welcome
    console.clear()
    console.print(Panel.fit(
        "[bold magenta]⚡  opencode-skills[/]  [dim]v1.0.0[/]",
        box=box.ROUNDED,
        border_style="bright_magenta",
    ))

    # Run init wizard
    from osk.cli import init
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(init)
    if result.output:
        console.print(result.output)

    # Summary
    console.print()
    console.print(Panel(
        "[bold green]✓ Setup complete![/]\n\n"
        "Run [bold]osk[/] for the interactive dashboard\n"
        "Run [bold]osk --help[/] for all commands\n"
        "Run [bold]osk status[/] to check installation\n"
        "Run [bold]osk doctor[/] to diagnose your setup",
        box=box.ROUNDED,
        border_style="green",
    ))


if __name__ == "__main__":
    _bootstrap(minimal=True)
    print()
    print("\033[1;36m╔══════════════════════════════════════════════╗\033[0m")
    print("\033[1;36m║\033[0m  \033[1;35m⚡ opencode-skills\033[0m                    \033[1;36m║\033[0m")
    print("\033[1;36m║\033[0m  \033[2mInstalling osk CLI...\033[0m                  \033[1;36m║\033[0m")
    print("\033[1;36m╚══════════════════════════════════════════════╝\033[0m")
    print()

    # Bootstrap fully, then run
    _bootstrap()

    from osk.cli import entry
    sys.argv = ["osk", "init"] if len(sys.argv) <= 1 else sys.argv
    entry()
