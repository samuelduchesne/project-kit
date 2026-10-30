#!/usr/bin/env python3
"""Consistency checks that `claude plugin validate` does not cover.

Checks the marketplace at the repository root against its single plugin:
the entry and manifest names match, the source path is a contained ./ path
that holds a plugin manifest, the entry sets no version, and the plugin
folder contains nothing it must not ship.

Read-only. Exit 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
FORBIDDEN = ("bin", "CLAUDE.md", "hooks", ".mcp.json")


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: file not found")
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
    return None


def check() -> list[str]:
    errors: list[str] = []
    marketplace = load_json(MARKETPLACE, errors)
    if marketplace is None:
        return errors

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        count = len(plugins) if isinstance(plugins, list) else "no"
        errors.append(
            f"marketplace.json: expected exactly one plugin entry, found {count}"
        )
        return errors

    entry = plugins[0]
    entry_name = entry.get("name")
    if "version" in entry:
        errors.append(
            "marketplace.json: the plugin entry must not set 'version' (set it in plugin.json only)"
        )

    source = entry.get("source")
    if (
        not isinstance(source, str)
        or not source.startswith("./")
        or ".." in source.split("/")
    ):
        errors.append(
            f"marketplace.json: source must be a './' path inside the repository, got {source!r}"
        )
        return errors

    plugin_dir = (ROOT / source).resolve()
    if not plugin_dir.is_relative_to(ROOT):
        errors.append(
            f"marketplace.json: source {source!r} resolves outside the repository"
        )
        return errors

    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.is_file():
        errors.append(
            f"marketplace.json: source {source!r} has no .claude-plugin/plugin.json"
        )
        return errors

    manifest = load_json(manifest_path, errors)
    if manifest is None:
        return errors

    if manifest.get("name") != entry_name:
        errors.append(
            f"name mismatch: marketplace entry is {entry_name!r} but plugin.json is {manifest.get('name')!r}"
        )

    for name in FORBIDDEN:
        if (plugin_dir / name).exists():
            errors.append(f"{source}/{name}: not allowed in the plugin folder")

    return errors


def main() -> int:
    errors = check()
    if errors:
        for error in errors:
            print(f"FAIL  {error}")
        return 1
    print("OK    marketplace and plugin manifests are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
