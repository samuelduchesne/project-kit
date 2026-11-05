#!/usr/bin/env python3
"""Regenerate the generated section of scripts/scientific-review-panel.js.

Workflow scripts cannot read plugin files at run time, so the protocol, the
role briefs, the dimension documents and the message schemas are embedded in
the script as string and object constants between the `// BEGIN GENERATED`
and `// END GENERATED` markers. This keeps the Claude Workflow runner identical
to the file-based runners (research R6).

Usage:
    build_workflow.py              write the section
    build_workflow.py --dry-run    print the unified diff; write nothing
    build_workflow.py --check      print the unified diff; exit 1 if not empty

Standard library only, Python 3.10 or later. Exit codes: 0 success or no
drift, 1 drift found by --check, 2 usage error, 3 precondition not met.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    print("build_workflow.py requires Python 3.10 or later.", file=sys.stderr)
    sys.exit(3)

PLUGIN_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = PLUGIN_DIR / "skills" / "scientific-review"
WORKFLOW = PLUGIN_DIR / "scripts" / "scientific-review-panel.js"
BEGIN = "// BEGIN GENERATED"
END = "// END GENERATED"


class PreconditionError(Exception):
    """A precondition of the build is not met; main() reports it and exits 3."""


def js_string(text: str) -> str:
    """A JavaScript string literal for `text` (JSON string syntax is valid JavaScript)."""
    return json.dumps(text, ensure_ascii=False)


def js_object(entries: dict[str, str]) -> str:
    lines = ["{"]
    for key, value in entries.items():
        lines.append(f"  {json.dumps(key)}: {value},")
    lines.append("}")
    return "\n".join(lines)


def generated_section() -> str:
    protocol = (SKILL_DIR / "protocol.md").read_text(encoding="utf-8")
    roles = {p.stem: js_string(p.read_text(encoding="utf-8")) for p in sorted((SKILL_DIR / "roles").glob("*.md"))}
    dimensions = {
        p.stem: js_string(p.read_text(encoding="utf-8")) for p in sorted((SKILL_DIR / "dimensions").glob("*.md"))
    }
    schemas = {}
    for path in sorted((SKILL_DIR / "schemas").glob("*.schema.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.name.removesuffix(".schema.json")] = json.dumps(data, indent=2, ensure_ascii=False).replace(
            "\n", "\n  "
        )
    if not roles or not schemas:
        raise PreconditionError(f"no role briefs or schemas found under {SKILL_DIR}")
    parts = [
        BEGIN,
        "// Sources: skills/scientific-review/protocol.md, roles/*.md, dimensions/*.md, schemas/*.schema.json",
        f"const PROTOCOL = {js_string(protocol)}",
        "",
        f"const ROLES = {js_object(roles)}",
        "",
        f"const DIMENSIONS = {js_object(dimensions)}",
        "",
        f"const SCHEMAS = {js_object(schemas)}",
        END,
    ]
    return "\n".join(parts)


def render(current: str) -> str:
    # The last END marker is the real one: an embedded source may quote the marker text inside a string constant.
    start = current.find(BEGIN)
    end = current.rfind(END)
    if start < 0 or end < start:
        raise PreconditionError(f"{WORKFLOW} lacks the {BEGIN!r} and {END!r} markers")
    return current[:start] + generated_section() + current[end + len(END) :]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="print the diff and exit 1 if the section is out of date")
    mode.add_argument("--dry-run", action="store_true", help="print the diff and write nothing")
    args = parser.parse_args(argv)
    print("build_workflow.py " + " ".join(sys.argv[1:] if argv is None else argv), file=sys.stderr)
    if not WORKFLOW.is_file():
        print(f"error: {WORKFLOW} not found", file=sys.stderr)
        return 3
    current = WORKFLOW.read_text(encoding="utf-8")
    try:
        updated = render(current)
    except PreconditionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    diff = "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=f"{WORKFLOW.name} (current)",
            tofile=f"{WORKFLOW.name} (generated)",
        )
    )
    if args.check or args.dry_run:
        if diff:
            print(diff, end="")
        if args.check:
            if diff:
                print(f"{WORKFLOW} is out of date; run build_workflow.py", file=sys.stderr)
                return 1
            print(f"{WORKFLOW} is up to date")
        return 0
    if diff:
        WORKFLOW.write_text(updated, encoding="utf-8")
        print(f"updated {WORKFLOW}")
    else:
        print(f"{WORKFLOW} is up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
