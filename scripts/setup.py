#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  opencode-skills installer                                  ║
║  One-line: curl -fsSL https://git.io/... | python3          ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, json, shutil, subprocess, urllib.request, getpass
from pathlib import Path

# ── Bootstrap rich (before any imports that depend on it) ──
def _bootstrap_rich():
    try:
        from rich.console import Console
        return True
    except ImportError:
        pass
    print("\033[1;33m📦 Installing rich (terminal UI library)...\033[0m")
    for cmd in [
        [sys.executable, "-m", "pip", "install", "rich", "--user", "-q"],
        [sys.executable, "-m", "pip", "install", "rich", "-q"],
        ["uv", "pip", "install", "rich", "-q"],
    ]:
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=30)
            break
        except Exception:
            continue
    from rich.console import Console
    return True

_bootstrap_rich()

# ── Rich imports ───────────────────────────────────────────
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich import box
from rich.columns import Columns

console = Console()

# ── Constants ──────────────────────────────────────────────
CONFIG_DIR = Path.home() / ".config" / "opencode"
PROJECT_DIR = Path.home() / ".opencode"
REPO_CACHE = Path.home() / ".cache" / "opencode-skills"
REPO_URL = "https://github.com/hosseinmirzapur/opencode-skills.git"
GITHUB_RAW = "https://raw.githubusercontent.com/hosseinmirzapur/opencode-skills/main"


def find_repo_root() -> Path | None:
    """Detect if we're running from within the cloned repo."""
    script = Path(__file__).resolve()
    for parent in [script.parent, script.parent.parent, Path.cwd()]:
        if (parent / "skills").is_dir() and (parent / "scripts" / "setup.py").is_file():
            return parent
    return None


def ensure_repo() -> Path:
    root = find_repo_root()
    if root:
        return root

    console.print()
    with console.status("[bold yellow]⟳[/] Cloning opencode-skills repository...", spinner="dots12"):
        if not shutil.which("git"):
            console.print()
            console.print(Panel(
                "[red]✗ Git is required but not installed.[/]\n\n"
                "Install it, then clone manually:\n"
                f"  [dim]git clone {REPO_URL}[/]\n"
                "  [dim]cd opencode-skills && python3 scripts/setup.py[/]",
                box=box.ROUNDED, border_style="red",
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


REPO_ROOT = ensure_repo()

# ── Derived paths ──────────────────────────────────────────
SKILLS_SRC = REPO_ROOT / "skills"
SKILLS_DST = CONFIG_DIR / "skills"
AGENTS_SRC = REPO_ROOT / "agents"
AGENTS_DST = CONFIG_DIR / "agents"
PLUGINS_SRC = REPO_ROOT / "plugins"
PLUGINS_DST = PROJECT_DIR / "plugins"
PROJECT_CONFIG_SRC = REPO_ROOT / "config" / "opencode.project.json"
PROJECT_CONFIG_DST = PROJECT_DIR / "opencode.json"
EXAMPLE_CONFIG_SRC = REPO_ROOT / "config" / "opencode.example.json"
USER_CONFIG_DST = CONFIG_DIR / "opencode.json"


# ── Helpers ────────────────────────────────────────────────

def check_cmd(name: str, *args: str) -> bool:
    try:
        subprocess.run([name, *args], capture_output=True, timeout=10)
        return True
    except Exception:
        return False


def run_step(msg: str, fn, success_icon: str = "green") -> bool:
    with console.status(f"[bold]{msg}", spinner="dots"):
        try:
            fn()
            console.print(f"  [[{success_icon}]✓[/{success_icon}]] {msg}")
            return True
        except Exception as e:
            console.print(f"  [[red]✗[/red]] {msg}")
            for line in str(e).split("\n"):
                console.print(f"       [dim]{line}[/]")
            return False


def copy_dir(src: Path, dst: Path) -> int:
    if not src.is_dir():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.iterdir():
        dst_path = dst / item.name
        if item.is_dir():
            shutil.copytree(item, dst_path, dirs_exist_ok=True)
            count += 1
        elif item.is_file():
            shutil.copy2(item, dst_path)
            count += 1
    return count


def get_cmd_version(name: str) -> str:
    try:
        r = subprocess.run([name, "--version"], capture_output=True, text=True, timeout=10)
        return (r.stdout or r.stderr).strip()
    except Exception:
        return ""


def add_providers(cfg: dict):
    """Interactive provider configuration."""
    if "provider" not in cfg:
        cfg["provider"] = {}

    console.print()
    console.print(Panel.fit(
        "[bold]API Provider Configuration[/]\n"
        "[dim]Add the LLM providers opencode will use.[/dim]",
        box=box.ROUNDED,
    ))

    while True:
        console.print()
        name = Prompt.ask("  Provider identifier", default="my-provider")
        label = Prompt.ask("  Display name", default=name.title().replace("-", " "))
        base_url = Prompt.ask("  API base URL", default="https://api.openai.com/v1")

        console.print("  [dim]Enter API key (input will be masked)[/dim]")
        console.print("  [bold yellow]?[/bold yellow] API key:", end=" ")
        api_key = getpass.getpass("")

        console.print()
        model_id = Prompt.ask("  Model ID", default="gpt-4o-mini")
        model_label = Prompt.ask("  Model label", default="GPT-4o Mini")

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

        console.print(f"  [green]✓[/] Provider [bold]{label}[/] added")
        if not Confirm.ask("  Add another provider?", default=False):
            break

    with open(USER_CONFIG_DST, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def write_project_config():
    """Write the project-level .opencode/opencode.json."""
    if not PROJECT_CONFIG_SRC.is_file():
        return
    PROJECT_CONFIG_DST.parent.mkdir(parents=True, exist_ok=True)

    if PROJECT_CONFIG_DST.exists():
        return

    shutil.copy2(PROJECT_CONFIG_SRC, PROJECT_CONFIG_DST)
    console.print(f"  [green]✓[/] Project config → [dim]{PROJECT_CONFIG_DST}[/]")


# ── Welcome ────────────────────────────────────────────────

def show_welcome():
    console.clear()
    width = min(console.width, 62)

    border = Text("─" * (width - 2), style="dim")
    console.print(Text("┌", style="dim") + border + Text("┐", style="dim"))

    content = "⚡  opencode-skills installer  "
    pad = width - 2 - len(content)
    left = pad // 2
    right = pad - left
    line = Text("│", style="dim") + Text(" " * left) + Text(content, style="bold cyan") + Text(" " * right) + Text("│", style="dim")
    console.print(line)

    one_liner = "curl -fsSL https://git.io/... | python3"
    pad2 = width - 2 - len(one_liner)
    left2 = pad2 // 2
    right2 = pad2 - left2
    line2 = Text("│", style="dim") + Text(" " * left2) + Text(one_liner, style="dim") + Text(" " * right2) + Text("│", style="dim")
    console.print(line2)

    console.print(Text("└", style="dim") + border + Text("┘", style="dim"))


# ── Main ───────────────────────────────────────────────────

def main():
    show_welcome()

    # ── Environment check ─────────────────────────────────
    console.print("\n[bold]Environment[/]")
    tbl = Table.grid(padding=(0, 2))
    tbl.add_column()

    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    tbl.add_row(f"  Python  [green]{py_ver}[/]")

    for tool in [("uv", "uv"), ("pipx", "pipx"), ("Node.js", "node"), ("git", "git")]:
        label, cmd = tool
        if check_cmd(cmd, "--version"):
            ver = get_cmd_version(cmd)
            tbl.add_row(f"  {label}  [green]✓[/] [dim]{ver.split(chr(10))[0]}[/]")
        else:
            tbl.add_row(f"  {label}  [yellow]not found[/]")
    console.print(Panel(tbl, box=box.ROUNDED, padding=(1, 2)))

    # ── Install graphify ──────────────────────────────────
    console.print("\n[bold]Installing graphify[/]")
    ver = get_cmd_version("graphify")
    if ver:
        console.print(f"  [green]✓[/] graphify [dim]{ver.split(chr(10))[0]}[/] (already installed)")
    else:
        def _install():
            if check_cmd("uv"):
                r = subprocess.run(
                    ["uv", "tool", "install", "graphifyy", "-q"],
                    capture_output=True, text=True, timeout=120,
                )
                if r.returncode != 0:
                    raise RuntimeError(r.stderr.strip())
            elif check_cmd("pipx"):
                r = subprocess.run(
                    ["pipx", "install", "graphifyy"],
                    capture_output=True, text=True, timeout=120,
                )
                if r.returncode != 0:
                    raise RuntimeError(r.stderr.strip())
            else:
                r = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "graphifyy", "--user", "-q"],
                    capture_output=True, text=True, timeout=120,
                )
                if r.returncode != 0:
                    r = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "graphifyy", "-q"],
                        capture_output=True, text=True, timeout=120,
                    )
                if r.returncode != 0:
                    raise RuntimeError(r.stderr.strip())
        run_step("Installing graphify...", _install)

    # ── npm dependencies ──────────────────────────────────
    console.print("\n[bold]npm dependencies[/]")
    if check_cmd("node", "--version") and (CONFIG_DIR / "package.json").exists():
        def _npm():
            r = subprocess.run(
                ["npm", "install"],
                cwd=str(CONFIG_DIR),
                capture_output=True, text=True, timeout=60,
            )
            if r.returncode != 0:
                raise RuntimeError(r.stderr.strip())
        run_step("Installing @opencode-ai/plugin...", _npm)
    else:
        console.print(f"  [yellow]~[/] Skipping (no package.json in [dim]{CONFIG_DIR}[/])")

    # ── Sync skills ───────────────────────────────────────
    console.print("\n[bold]Syncing skills[/]")
    skill_count = [0]
    def _sync_skills():
        skill_count[0] = copy_dir(SKILLS_SRC, SKILLS_DST)
        if skill_count[0] == 0:
            raise RuntimeError("No skills found in repository")
    ok = run_step("Copying skills...", _sync_skills)
    if ok:
        console.print(f"       [dim]{skill_count[0]} skills in {SKILLS_DST}[/]")

    # ── Sync agents ───────────────────────────────────────
    console.print("\n[bold]Syncing agents[/]")
    agent_count = [0]
    def _sync_agents():
        agent_count[0] = copy_dir(AGENTS_SRC, AGENTS_DST)
    run_step("Copying agents...", _sync_agents)
    if agent_count[0]:
        console.print(f"       [dim]{agent_count[0]} agents in {AGENTS_DST}[/]")

    # ── Sync plugins ──────────────────────────────────────
    console.print("\n[bold]Syncing plugins[/]")
    PLUGINS_DST.mkdir(parents=True, exist_ok=True)
    plugin_count = [0]
    def _sync_plugins():
        for f in PLUGINS_SRC.iterdir():
            if f.is_file():
                shutil.copy2(f, PLUGINS_DST / f.name)
                plugin_count[0] += 1
    run_step("Copying plugins...", _sync_plugins)
    if plugin_count[0]:
        console.print(f"       [dim]{plugin_count[0]} plugins in {PLUGINS_DST}[/]")

    # ── Project config ────────────────────────────────────
    console.print("\n[bold]Project config[/]")
    write_project_config()
    console.print(f"  [green]✓[/] Plugin reference → [dim]{PROJECT_CONFIG_DST}[/]")

    # ── User config ───────────────────────────────────────
    console.print("\n[bold]User config[/]")
    if USER_CONFIG_DST.exists():
        console.print(f"  [green]✓[/] Existing config at [dim]{USER_CONFIG_DST}[/]")
        with open(USER_CONFIG_DST) as f:
            cfg = json.load(f)
        providers = cfg.get("provider", {})
        if providers:
            names = ", ".join(p.get("name", k) for k, p in providers.items())
            console.print(f"  [green]✓[/] Providers: {names}")
        else:
            console.print(f"  [yellow]~[/] No providers configured yet")
            add_providers(cfg)
    else:
        console.print(f"  [yellow]~[/] No config found — creating from template")
        cfg = json.loads(EXAMPLE_CONFIG_SRC.read_text())
        cfg.pop("$comment", None)
        USER_CONFIG_DST.parent.mkdir(parents=True, exist_ok=True)
        with open(USER_CONFIG_DST, "w") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
        console.print(f"  [green]✓[/] Created [dim]{USER_CONFIG_DST}[/]")
        add_providers(cfg)

    # ── Register graphify ─────────────────────────────────
    console.print("\n[bold]Graphify registration[/]")
    if shutil.which("graphify"):
        def _register():
            r = subprocess.run(
                ["graphify", "install", "--platform", "opencode"],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode != 0:
                raise RuntimeError(r.stderr.strip())
        run_step("Registering graphify with opencode...", _register)
    else:
        console.print("  [yellow]~[/] graphify CLI not found on PATH — register manually:")
        console.print("       [dim]graphify install --platform opencode[/]")

    # ── Summary ───────────────────────────────────────────
    console.print()
    summary_lines = [
        "[bold green]✓ Setup complete![/]",
        "",
        "Run [bold]opencode[/] in any project directory and type:",
        "  [bold cyan]/graphify .[/]",
        "",
        f"[dim]To update: cd {REPO_ROOT} && git pull && python3 scripts/setup.py[/]",
    ]
    if REPO_ROOT == REPO_CACHE:
        summary_lines[-1] = f"[dim]To update: git -C {REPO_CACHE} pull && python3 {REPO_CACHE / 'scripts' / 'setup.py'}[/]"

    console.print(Panel(
        "\n".join(summary_lines),
        box=box.ROUNDED,
        border_style="green",
        padding=(1, 2),
    ))


if __name__ == "__main__":
    main()
