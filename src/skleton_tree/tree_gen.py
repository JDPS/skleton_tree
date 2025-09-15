# SPDX-License-Identifier: MIT
# Copyright (c) 2025 João Soares

"""A simple script to print and write a directory tree structure.

Refactors:
- Use explicit connector/guide constants (Unicode or ASCII) for clarity.
- Fix connector selection (distinguish middle vs last entries).
- Add ``--ascii`` flag to output ASCII-only trees for broad terminal support.
"""

import argparse
import fnmatch
from pathlib import Path


class TreeChars:
    """Holds the characters used to draw the tree."""

    def __init__(self, guide: str, space: str, branch: str, last: str) -> None:
        self.GUIDE = guide  # e.g., "│   " or "|   "
        self.SPACE = space  # "    "
        self.BRANCH = branch  # e.g., "├── " or "|-- "
        self.LAST = last  # e.g., "└── " or "\\-- "


UNICODE_CHARS = TreeChars(guide="│   ", space="    ", branch="├── ", last="└── ")
ASCII_CHARS = TreeChars(guide="|   ", space="    ", branch="|-- ", last="\\-- ")


def matches_ignores(name: str, patterns: list[str]) -> bool:
    """Check if a name matches any of the ignored patterns."""
    return any(fnmatch.fnmatch(name, pat) for pat in patterns)


def list_entries(path: Path, show_files: bool, ignores: list[str]) -> list[Path]:
    """List directory entries, filtering by show_files and ignores."""
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
    path: Path,
    level: int,
    show_files: bool,
    ignores: list[str],
    chars: TreeChars,
    prefix: str = "",
) -> list[str]:
    """Recursively build the directory tree structure as a list of strings."""
    lines: list[str] = []
    entries = list_entries(path, show_files, ignores)
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = chars.LAST if is_last else chars.BRANCH
        name = entry.name + ("/" if entry.is_dir() else "")
        lines.append(prefix + connector + name)
        if entry.is_dir() and level > 1:
            extension = chars.SPACE if is_last else chars.GUIDE
            lines.extend(
                build_tree(
                    entry, level - 1, show_files, ignores, chars, prefix + extension
                )
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
    parser.add_argument(
        "--ascii",
        action="store_true",
        help="Use ASCII connectors instead of Unicode",
    )
    parser.add_argument("--output", type=str, help="Save tree to a .txt file")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    root_name = root.name or str(root)
    chars = ASCII_CHARS if args.ascii else UNICODE_CHARS
    tree_lines = [root_name + "/"] + build_tree(
        root, args.level, args.files, args.ignore, chars
    )

    print_tree(tree_lines)
    if args.output:
        save_tree(tree_lines, Path(args.output))
        print(f"Tree saved to {args.output}")


if __name__ == "__main__":
    main()
