#!/usr/bin/env python3
"""Consistency checks that `claude plugin validate` does not cover.

Checks the Claude marketplace at the repository root against every plugin it
lists: each entry and manifest name match, each source path is a contained ./
path that holds a plugin manifest, no entry sets a version, no plugin folder
contains anything it must not ship, and no skill or agent frontmatter has a
plain value that a strict YAML parser rejects. Checks the Codex manifest of
sci-review against its Claude manifest (same name and version, skills path,
interface block) and that the Codex marketplace lists sci-review only, since
project-kit has no Codex manifest.

Read-only. Exit 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CODEX_PLUGINS = ("sci-review",)
FORBIDDEN = ("bin", "CLAUDE.md", "hooks", ".mcp.json")


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: file not found")
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
    return None


def check_frontmatter(plugin_dir: Path, errors: list[str]) -> None:
    paths = [*plugin_dir.glob("skills/*/SKILL.md"), *plugin_dir.glob("agents/*.md")]
    for path in paths:
        name = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"{name}: no frontmatter")
            continue
        for line in text.split("---", 2)[1].splitlines():
            _, separator, value = line.partition(": ")
            if line[:1].isspace() or not separator or value[:1] in ("'", '"', ">", "|"):
                continue
            if ": " in value:
                errors.append(f"{name}: quote or fold this value, strict YAML rejects its ': ' ({line[:40]!r})")


def check_entry(entry: dict, errors: list[str]) -> Path | None:
    """Check one Claude marketplace entry; return its plugin directory when it is usable."""
    entry_name = entry.get("name")
    if "version" in entry:
        errors.append(f"marketplace.json: entry {entry_name!r} must not set 'version' (set it in plugin.json only)")

    source = entry.get("source")
    if not isinstance(source, str) or not source.startswith("./") or ".." in source.split("/"):
        errors.append(
            f"marketplace.json: source of {entry_name!r} must be a './' path inside the repository, got {source!r}"
        )
        return None

    plugin_dir = (ROOT / source).resolve()
    if not plugin_dir.is_relative_to(ROOT):
        errors.append(f"marketplace.json: source {source!r} resolves outside the repository")
        return None

    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.is_file():
        errors.append(f"marketplace.json: source {source!r} has no .claude-plugin/plugin.json")
        return None

    manifest = load_json(manifest_path, errors)
    if manifest is None:
        return None

    if manifest.get("name") != entry_name:
        errors.append(f"name mismatch: marketplace entry is {entry_name!r} but plugin.json is {manifest.get('name')!r}")

    for name in FORBIDDEN:
        if (plugin_dir / name).exists():
            errors.append(f"{source}/{name}: not allowed in the plugin folder")

    check_frontmatter(plugin_dir, errors)
    return plugin_dir


def check_codex(plugin_dirs: dict[str, Path], errors: list[str]) -> None:
    """Check the Codex manifests and the Codex marketplace statically (no Codex CLI is called)."""
    for name in CODEX_PLUGINS:
        plugin_dir = plugin_dirs.get(name)
        if plugin_dir is None:
            errors.append(f"{name}: not listed in the Claude marketplace, so its Codex manifest cannot be checked")
            continue
        claude = load_json(plugin_dir / ".claude-plugin" / "plugin.json", errors)
        codex = load_json(plugin_dir / ".codex-plugin" / "plugin.json", errors)
        if claude is None or codex is None:
            continue
        for key in ("name", "version"):
            if codex.get(key) != claude.get(key):
                errors.append(
                    f"{name}: Codex manifest {key} {codex.get(key)!r} differs from Claude {claude.get(key)!r}"
                )
        if codex.get("skills") != "./skills/":
            errors.append(f"{name}: Codex manifest must set skills to './skills/', got {codex.get('skills')!r}")
        if not isinstance(codex.get("interface"), dict) or not codex["interface"].get("displayName"):
            errors.append(f"{name}: Codex manifest needs an interface block with a displayName")

    marketplace = load_json(CODEX_MARKETPLACE, errors)
    if marketplace is None:
        return
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        errors.append(".agents/plugins/marketplace.json: 'plugins' must be a list")
        return
    names = [e.get("name") for e in entries if isinstance(e, dict)]
    if sorted(names) != sorted(CODEX_PLUGINS):
        errors.append(f".agents/plugins/marketplace.json: must list exactly {list(CODEX_PLUGINS)}, found {names}")
    for entry in entries:
        source = entry.get("source") if isinstance(entry, dict) else None
        path = source.get("path") if isinstance(source, dict) else None
        if not isinstance(source, dict) or source.get("source") != "local" or not isinstance(path, str):
            errors.append(f".agents/plugins/marketplace.json: {entry.get('name')!r} needs a local source with a path")
            continue
        target = (ROOT / path).resolve()
        if not path.startswith("./") or not target.is_relative_to(ROOT) or not (target / ".codex-plugin").is_dir():
            errors.append(f".agents/plugins/marketplace.json: {path!r} is not a plugin folder with .codex-plugin/")


def check() -> list[str]:
    errors: list[str] = []
    marketplace = load_json(MARKETPLACE, errors)
    if marketplace is None:
        return errors

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("marketplace.json: expected a non-empty list of plugin entries")
        return errors

    names = [entry.get("name") for entry in plugins]
    duplicates = sorted({n for n in names if names.count(n) > 1})
    if duplicates:
        errors.append(f"marketplace.json: duplicate plugin names {duplicates}")

    plugin_dirs: dict[str, Path] = {}
    for entry in plugins:
        plugin_dir = check_entry(entry, errors)
        if plugin_dir is not None:
            plugin_dirs[entry.get("name")] = plugin_dir

    check_codex(plugin_dirs, errors)
    return errors


def main() -> int:
    errors = check()
    if errors:
        for error in errors:
            print(f"FAIL  {error}")
        return 1
    print("OK    marketplaces and plugin manifests are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
