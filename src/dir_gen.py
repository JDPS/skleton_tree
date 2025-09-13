# SPDX-License-Identifier: MIT
# Copyright (c) 2025 João Soares
"""Generate directories and files from a tree layout file."""

import argparse
from pathlib import Path


def parse_tree_layout(layout_file: Path) -> list[tuple[int, str, bool]]:
    """Parse the tree layout file into (indent_level, name, is_dir) tuples."""
    lines = layout_file.read_text(encoding="utf-8").splitlines()
    result = []
    for line in lines:
        if not line.strip():
            continue
        i = 0
        indent = 0
        while i + 4 <= len(line) and line[i : i + 4] in ("│   ", "    "):
            indent += 1
            i += 4
        # After the guide blocks, expect a connector for non-root lines
        name_part = line[i:]
        if name_part.startswith("├── ") or name_part.startswith("└── "):
            name = name_part[4:]
        else:
            # Root line (e.g., "skleton_tree/" without connector)
            name = name_part
            indent = 0
        name = name.rstrip("/")
        is_dir = name_part.endswith("/") or name_part.endswith("/ ")
        result.append((indent, name, is_dir))
    return result


def create_structure(
    layout: list[tuple[int, str, bool]], root: Path, dry_run: bool = False
):
    """Create directories and files from the parsed layout."""
    stack = [root]
    for indent, name, is_dir in layout[1:]:  # skip root line
        while len(stack) > indent + 1:
            stack.pop()
        path = stack[-1] / name
        if is_dir:
            if dry_run:
                print(f"Would create directory: {path}")
            else:
                # Ensure all parent directories are created
                path.mkdir(parents=True, exist_ok=True)
            stack.append(path)
        else:
            if dry_run:
                print(f"Would create file: {path}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch(exist_ok=True)


def main():
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
    # Ensure the root exists (important when creating nested structure)
    if not args.dry_run:
        root.mkdir(parents=True, exist_ok=True)
    layout = parse_tree_layout(layout_file)
    create_structure(layout, root, args.dry_run)


if __name__ == "__main__":
    main()

# Usage examples:
# python dir_gen.py tree.txt ./output_dir
# python dir_gen.py tree.txt ./output_dir --dry-run
