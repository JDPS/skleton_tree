# SPDX-License-Identifier: MIT
# Copyright (c) 2025 João Soares

"""Generate directories and files from a tree layout file.

Refactors:
- Make parsing tolerant to Unicode/ASCII connectors and legacy replacement chars.
- Keep behavior the same for dry-run and creation logic.
"""

import argparse
from pathlib import Path

# Accept both Unicode and ASCII blocks, plus legacy replacement-char blocks
GUIDE_BLOCKS: tuple[str, ...] = (
    "│   ",  # Unicode guide
    "|   ",  # ASCII guide
    "�   ",  # Replacement-char guide seen in some encodings
    "    ",  # Spaces (no guide)
)

CONNECTORS: tuple[str, ...] = (
    "├── ",  # Unicode branch
    "└── ",  # Unicode last
    "|-- ",  # ASCII branch
    "+-- ",  # ASCII alt branch
    "`-- ",  # ASCII alt last
    "��� ",  # Replacement-char sequence seen in legacy files
)


def _find_layout_start(lines):
    for idx, raw in enumerate(lines):
        txt = raw.strip()
        if not txt or txt.startswith("SPDX-"):
            continue
        if txt.endswith("/"):
            return idx
    return 0


def _parse_line(line):
    i = 0
    indent = 0
    while i + 4 <= len(line) and line[i : i + 4] in GUIDE_BLOCKS:
        indent += 1
        i += 4
    name_part = line[i:]
    for conn in CONNECTORS:
        if name_part.startswith(conn):
            name = name_part[len(conn) :]
            break
    else:
        name = name_part
        indent = 0
    is_dir = name.rstrip().endswith("/")
    name = name.rstrip().rstrip("/")
    return indent, name, is_dir


def parse_tree_layout(layout_file: Path) -> list[tuple[int, str, bool]]:
    lines = layout_file.read_text(encoding="utf-8").splitlines()
    result = []
    start = _find_layout_start(lines)
    for raw in lines[start:]:
        line = raw.rstrip("\n\r")
        if not line.strip():
            continue
        result.append(_parse_line(line))
    return result


def _process_entry(stack, indent, name, is_dir, dry_run):
    while len(stack) > indent + 1:
        stack.pop()
    path = stack[-1] / name
    if is_dir:
        if dry_run:
            print(f"Would create directory: {path}")
        else:
            path.mkdir(parents=True, exist_ok=True)
        stack.append(path)
    else:
        if dry_run:
            print(f"Would create file: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)


def create_structure(layout, root: Path, dry_run: bool = False):
    if not layout:
        return
    stack = [root]
    start_index = 1 if layout else 0
    for indent, name, is_dir in layout[start_index:]:
        _process_entry(stack, indent, name, is_dir, dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate directories and files from a tree layout file."
    )
    parser.add_argument("layout", type=str, help="Path to tree layout .txt file")
    parser.add_argument(
        "root", nargs="?", default=".", help="Root directory to create structure"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview actions without creating"
    )
    args = parser.parse_args()

    layout_file = Path(args.layout)
    root = Path(args.root).resolve()
    if not args.dry_run:
        root.mkdir(parents=True, exist_ok=True)
    layout = parse_tree_layout(layout_file)
    create_structure(layout, root, args.dry_run)


if __name__ == "__main__":
    main()
