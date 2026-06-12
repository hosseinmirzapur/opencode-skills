"""Configuration management for opencode config files."""

import json
from pathlib import Path
from typing import Any, Optional

CONFIG_DIR = Path.home() / ".config" / "opencode"
PROJECT_DIR = Path.home() / ".opencode"


def load_user_config() -> dict[str, Any]:
    """Load the user-level opencode config (or return empty dict)."""
    path = CONFIG_DIR / "opencode.json"
    if path.is_file():
        return json.loads(path.read_text())
    return {}


def load_project_config() -> dict[str, Any]:
    """Load the project-level opencode config (or return empty dict)."""
    path = PROJECT_DIR / "opencode.json"
    if path.is_file():
        return json.loads(path.read_text())
    return {}


def save_user_config(cfg: dict[str, Any]) -> None:
    """Write the user-level config."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    path = CONFIG_DIR / "opencode.json"
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")


def save_project_config(cfg: dict[str, Any]) -> None:
    """Write the project-level config."""
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    path = PROJECT_DIR / "opencode.json"
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")


def get_providers() -> dict[str, Any]:
    """Get configured LLM providers."""
    return load_user_config().get("provider", {})


def set_providers(providers: dict[str, Any]) -> None:
    """Set LLM providers in user config."""
    cfg = load_user_config()
    cfg["provider"] = providers
    save_user_config(cfg)


def get_installed_plugins() -> list[str]:
    """Get list of plugin file paths from project config."""
    cfg = load_project_config()
    return cfg.get("plugin", [])


def add_plugin(plugin_rel: str) -> bool:
    """Add a plugin reference to the project config. Returns True if added."""
    cfg = load_project_config()
    plugins = cfg.get("plugin", [])
    if plugin_rel in plugins:
        return False
    plugins.append(plugin_rel)
    cfg["plugin"] = plugins
    save_project_config(cfg)
    return True


def remove_plugin(plugin_rel: str) -> bool:
    """Remove a plugin reference from the project config."""
    cfg = load_project_config()
    plugins = cfg.get("plugin", [])
    if plugin_rel not in plugins:
        return False
    plugins.remove(plugin_rel)
    cfg["plugin"] = plugins
    save_project_config(cfg)
    return True
