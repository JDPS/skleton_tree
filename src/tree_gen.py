# SPDX-License-Identifier: MIT
# Copyright (c) 2025 João Soares

"""A simple script to print and write a directory tree structure."""

import argparse
import fnmatch
from pathlib import Path


def matches_ignores(name: str, patterns: list[str]) -> bool:
    """Check if a name matches any of the ignored patterns."""
    return any(fnmatch.fnmatch(name, pat) for pat in patterns)


def list_entries(path: Path, show_files: bool, ignores: list[str]) -> list[Path]:
    """list directory entries, filtering by show_files and ignores."""
    try:
        entries = list(path.iterdir())
    except (PermissionError, FileNotFoundError):
        return []
    return sorted(
        [
            e
            for e in entries
            if (show_files or e.is_dir()) and not matches_ignores(e.name, ignores)
        ],
        key=lambda e: (not e.is_dir(), e.name.lower()),
    )


def build_tree(
    path: Path, level: int, show_files: bool, ignores: list[str], prefix: str = ""
) -> list[str]:
    """Recursively build the directory tree structure as a list of strings."""
    lines = []
    entries = list_entries(path, show_files, ignores)
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        name = entry.name + ("/" if entry.is_dir() else "")
        lines.append(prefix + connector + name)
        if entry.is_dir() and level > 1:
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.extend(
                build_tree(entry, level - 1, show_files, ignores, prefix + extension)
            )
    return lines


def print_tree(lines: list[str]) -> None:
    """Print the tree lines to stdout."""
    for line in lines:
        print(line)


def save_tree(lines: list[str], output_file: Path) -> None:
    """Save the tree lines to a text file."""

    output_file.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a directory tree.")
    parser.add_argument("path", nargs="?", default=".", help="Root directory")
    parser.add_argument(
        "-L", "--level", type=int, default=99, help="Max depth (default: 99)"
    )
    parser.add_argument("--files", action="store_true", help="Include files")
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="Glob patterns to ignore (repeatable)",
    )
    parser.add_argument("--output", type=str, help="Save tree to a .txt file")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    root_name = root.name or str(root)
    tree_lines = [root_name + "/"] + build_tree(
        root, args.level, args.files, args.ignore
    )

    print_tree(tree_lines)
    if args.output:
        save_tree(tree_lines, Path(args.output))
        print(f"Tree saved to {args.output}")


if __name__ == "__main__":
    main()

# Usage examples:
# python tree_gen.py abc -L 5 --files
# python tree_gen.py abc -L 5 --files --ignore ".git" --ignore "node_modules"
# python tree_gen.py abc -L 5 --files --output tree.txt
