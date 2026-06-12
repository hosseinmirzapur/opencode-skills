"""Install, uninstall, and update orchestrator."""

import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich import box

from osk.assets import Theme
from osk.config import add_plugin, remove_plugin
from osk.registry import Component, ComponentGroup, REPO_URL
from osk.sync import (
    check_outdated,
    component_installed,
    copy_component,
    copy_dir,
    remove_component,
)
from osk.ui import (
    make_progress,
    status_panel,
    success_panel,
    error_panel,
    console,
)

REPO_CACHE = Path.home() / ".cache" / "opencode-skills"
CONFIG_DIR = Path.home() / ".config" / "opencode"
PROJECT_DIR = Path.home() / ".opencode"


# ── Repository management ────────────────────────────────────────────────

def find_repo_root() -> Optional[Path]:
    """Detect if running from within the cloned repo."""
    script = Path(__file__).resolve()

    candidates = [
        script.parent,          # scripts/osk/
        script.parent.parent,   # scripts/
        script.parent.parent.parent,  # repo root
        Path.cwd(),
        Path.cwd().parent,
    ]
    for parent in candidates:
        skills_dir = parent / "skills"
        setup_py = parent / "scripts" / "setup.py"
        if skills_dir.is_dir() and setup_py.is_file():
            return parent

    return None


def ensure_repo() -> Path:
    """Locate or clone the repo. Returns repo root."""
    root = find_repo_root()
    if root:
        return root

    console.print()
    with console.status("[bold]⟳[/] Cloning repository...", spinner="dots12"):
        if not shutil_which("git"):
            console.print(error_panel(
                "Git is required but not installed.",
                f"Clone manually:\n  git clone {REPO_URL}",
            ))
            sys.exit(1)
        REPO_CACHE.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["git", "clone", "--depth=1", REPO_URL, str(REPO_CACHE)],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            console.print(f"[red]✗[/] Clone failed: {result.stderr.strip()}")
            sys.exit(1)
    return REPO_CACHE


def update_repo(repo_root: Path) -> bool:
    """Pull latest changes. Returns True if updated."""
    if repo_root == REPO_CACHE:
        with console.status("[bold]⟳[/] Updating repository...", spinner="dots12"):
            result = subprocess.run(
                ["git", "-C", str(repo_root), "pull", "--ff-only"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode != 0:
                console.print(f"[yellow]![/] Update issue: {result.stderr.strip()}")
                return False
            return "Already up to date" not in result.stdout
    return True


# ── Graphify management ─────────────────────────────────────────────────

def is_graphify_installed() -> bool:
    return shutil_which("graphify") is not None


def install_graphify() -> bool:
    """Install graphify via uv, pipx, or pip."""
    if is_graphify_installed():
        return True

    def _run(cmd: list[str]) -> bool:
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=True)
            return True
        except Exception:
            return False

    installers = [
        ["uv", "tool", "install", "graphifyy", "-q"],
        ["pipx", "install", "graphifyy"],
        [sys.executable, "-m", "pip", "install", "graphifyy", "--user", "-q"],
        [sys.executable, "-m", "pip", "install", "graphifyy", "-q"],
    ]

    for installer in installers:
        if shutil_which(installer[0]):
            if _run(installer):
                return True
    return False


def register_graphify() -> bool:
    """Register graphify with opencode platform."""
    if not is_graphify_installed():
        return False
    try:
        subprocess.run(
            ["graphify", "install", "--platform", "opencode"],
            capture_output=True, text=True, timeout=30, check=True,
        )
        return True
    except Exception:
        return False


# ── npm dependencies ────────────────────────────────────────────────────

def install_npm_deps() -> bool:
    """Install npm dependencies in config dir if package.json exists."""
    pkg = CONFIG_DIR / "package.json"
    if not pkg.exists() or not shutil_which("node"):
        return False
    try:
        subprocess.run(
            ["npm", "install"],
            cwd=str(CONFIG_DIR),
            capture_output=True, text=True, timeout=60, check=True,
        )
        return True
    except Exception:
        return False


# ── Component operations ────────────────────────────────────────────────

def install_all(repo_root: Path, groups: list[ComponentGroup]) -> None:
    """Install all components with progress tracking."""
    progress = make_progress()

    total = sum(len(g.components) for g in groups)
    task = progress.add_task("[bold]Installing components...", total=total)

    counts: dict[str, int] = {}
    errors: list[str] = []

    with progress:
        for group in groups:
            for comp in group.components:
                progress.update(task, description=f"[bold]{comp.label}")
                try:
                    if not component_installed(comp):
                        if copy_component(comp, repo_root):
                            counts[group.kind] = counts.get(group.kind, 0) + 1
                            # Register plugin references
                            if comp.kind == "plugin":
                                add_plugin(f".opencode/plugins/{comp.dest.name}")
                        else:
                            errors.append(f"Failed: {comp.label}")
                    else:
                        counts[group.kind] = counts.get(group.kind, 0)
                except Exception as e:
                    errors.append(f"{comp.label}: {e}")
                progress.advance(task)

    # Also sync top-level dirs
    with console.status("[bold]Syncing skill directories...", spinner="dots"):
        copy_dir(repo_root / "skills", CONFIG_DIR / "skills")
        copy_dir(repo_root / "agents", CONFIG_DIR / "agents")
        copy_dir(repo_root / "plugins", PROJECT_DIR / "plugins")

    # Summary
    parts = [f"[green]✓[/] {v} {k}" for k, v in counts.items()]
    summary = " · ".join(parts) if parts else "[yellow]Nothing new to install[/]"
    console.print(success_panel(summary, detail=f"{total} total components in catalog"))

    if errors:
        for e in errors:
            console.print(f"  [red]✗[/] {e}")


def install_graphify_flow() -> None:
    """Install graphify and register it."""
    if is_graphify_installed():
        console.print(f"  [green]✓[/] graphify already installed [dim]({get_cmd_version('graphify')})[/]")
    else:
        with console.status("[bold]Installing graphify...", spinner="dots12"):
            if install_graphify():
                console.print("  [green]✓[/] graphify installed")
            else:
                console.print("  [red]✗[/] graphify installation failed")
                return

    if register_graphify():
        console.print("  [green]✓[/] graphify registered with opencode")
    else:
        console.print("  [yellow]~[/] graphify registration skipped (run manually: graphify install --platform opencode)")


def uninstall_component(comp: Component) -> bool:
    """Uninstall a single component."""
    if not component_installed(comp):
        return False
    remove_component(comp)
    if comp.kind == "plugin":
        remove_plugin(f".opencode/plugins/{comp.dest.name}")
    return True


# ── Helpers ──────────────────────────────────────────────────────────────

def shutil_which(name: str) -> Optional[str]:
    from shutil import which
    return which(name)


def get_cmd_version(name: str) -> str:
    try:
        r = subprocess.run([name, "--version"], capture_output=True, text=True, timeout=10)
        return (r.stdout or r.stderr).strip()
    except Exception:
        return ""


def get_installed_count(groups: list[ComponentGroup]) -> dict[str, int]:
    """Count installed vs total components."""
    result = {}
    for g in groups:
        installed = sum(1 for c in g.components if component_installed(c))
        result[g.kind] = installed
    return result
