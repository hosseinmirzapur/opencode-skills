"""Component registry — catalogs all installable items in the repo."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


REPO_URL = "https://github.com/hosseinmirzapur/opencode-skills.git"
GITHUB_RAW = "https://raw.githubusercontent.com/hosseinmirzapur/opencode-skills/main"


@dataclass
class Component:
    id: str
    label: str
    description: str
    kind: str  # "skill" | "plugin" | "agent" | "tool" | "config"
    source_rel: str  # relative path inside the repo
    dest: Path  # destination path
    required: bool = False
    version: Optional[str] = None


@dataclass
class ComponentGroup:
    kind: str
    label: str
    icon: str
    components: list[Component] = field(default_factory=list)


def get_components(repo_root: Path) -> list[ComponentGroup]:
    """Build the full catalog from the repo on disk."""
    config_dir = Path.home() / ".config" / "opencode"
    project_dir = Path.home() / ".opencode"

    groups: list[ComponentGroup] = []

    # ── Skills ──────────────────────────────────────────────────────────
    skill_dir = repo_root / "skills"
    skills = []
    if skill_dir.is_dir():
        for d in sorted(skill_dir.iterdir()):
            if d.is_dir() and not d.name.startswith("_"):
                skills.append(Component(
                    id=f"skill/{d.name}",
                    label=d.name,
                    description=_read_skill_description(d),
                    kind="skill",
                    source_rel=f"skills/{d.name}",
                    dest=config_dir / "skills" / d.name,
                ))
    groups.append(ComponentGroup(
        kind="skills",
        label=f"Skills ({len(skills)})",
        icon="🧩",
        components=skills,
    ))

    # ── Plugins ─────────────────────────────────────────────────────────
    plugin_dir = repo_root / "plugins"
    plugins = []
    if plugin_dir.is_dir():
        for f in sorted(plugin_dir.iterdir()):
            if f.is_file() and f.suffix in (".js", ".ts", ".mjs"):
                plugins.append(Component(
                    id=f"plugin/{f.stem}",
                    label=f.stem,
                    description=f"Plugin: {f.name}",
                    kind="plugin",
                    source_rel=f"plugins/{f.name}",
                    dest=project_dir / "plugins" / f.name,
                ))
    groups.append(ComponentGroup(
        kind="plugins",
        label=f"Plugins ({len(plugins)})",
        icon="🧩",
        components=plugins,
    ))

    # ── Agents ──────────────────────────────────────────────────────────
    agent_dir = repo_root / "agents"
    agents = []
    if agent_dir.is_dir():
        for f in sorted(agent_dir.iterdir()):
            if f.is_file() and f.suffix == ".md":
                agents.append(Component(
                    id=f"agent/{f.stem}",
                    label=f.stem,
                    description=f"Agent definition: {f.stem}",
                    kind="agent",
                    source_rel=f"agents/{f.name}",
                    dest=config_dir / "agents" / f.name,
                ))
    groups.append(ComponentGroup(
        kind="agents",
        label=f"Agents ({len(agents)})",
        icon="🤖",
        components=agents,
    ))

    # ── Config ──────────────────────────────────────────────────────────
    configs = []
    project_config = repo_root / "config" / "opencode.project.json"
    if project_config.is_file():
        configs.append(Component(
            id="config/project",
            label="Project config",
            description="Project-level .opencode/opencode.json",
            kind="config",
            source_rel="config/opencode.project.json",
            dest=project_dir / "opencode.json",
        ))
    example_config = repo_root / "config" / "opencode.example.json"
    if example_config.is_file():
        configs.append(Component(
            id="config/user",
            label="User config template",
            description="User-level .config/opencode/opencode.json",
            kind="config",
            source_rel="config/opencode.example.json",
            dest=config_dir / "opencode.json",
        ))
    groups.append(ComponentGroup(
        kind="config",
        label="Config",
        icon="⚙️",
        components=configs,
    ))

    return groups


def _read_skill_description(skill_dir: Path) -> str:
    """Extract a one-line description from a skill SKILL.md or directory name."""
    skill_md = skill_dir / "SKILL.md"
    if skill_md.is_file():
        for line in skill_md.read_text().splitlines():
            line = line.strip()
            if line.startswith("description:") or line.startswith("description >"):
                desc = line.split(":", 1)[-1].strip()
                if desc:
                    return desc
    return skill_dir.name.replace("-", " ").title()


def search_components(groups: list[ComponentGroup], query: str) -> list[Component]:
    """Search all components by label or description."""
    q = query.lower()
    results = []
    for group in groups:
        for c in group.components:
            if q in c.label.lower() or q in c.description.lower():
                results.append(c)
    return results
