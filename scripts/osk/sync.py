"""Repository-to-local file syncing engine."""

import shutil
from pathlib import Path
from typing import Optional

from osk.registry import Component


def ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_component(component: Component, repo_root: Path, dry_run: bool = False) -> bool:
    """Copy a component from the repo to its destination. Returns True on success."""
    src = repo_root / component.source_rel
    dst = component.dest

    if not src.exists():
        return False

    if dry_run:
        return True

    dst.parent.mkdir(parents=True, exist_ok=True)

    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)

    return True


def copy_dir(src: Path, dst: Path) -> int:
    """Copy all top-level items from src to dst. Returns count of items copied."""
    if not src.is_dir():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.iterdir():
        dest = dst / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
            count += 1
        elif item.is_file():
            shutil.copy2(item, dest)
            count += 1
    return count


def remove_component(component: Component) -> bool:
    """Remove a component from its destination. Returns True on success."""
    dst = component.dest
    if not dst.exists():
        return False
    if dst.is_dir():
        shutil.rmtree(dst)
    else:
        dst.unlink()
    return True


def component_installed(component: Component) -> bool:
    """Check if a component is already installed."""
    return component.dest.exists()


def check_outdated(component: Component, repo_root: Path) -> bool:
    """Check if a component's source is newer than its installed version."""
    src = repo_root / component.source_rel
    dst = component.dest
    if not dst.exists():
        return True
    if not src.exists():
        return False
    src_mtime = src.stat().st_mtime
    dst_mtime = dst.stat().st_mtime
    return src_mtime > dst_mtime
