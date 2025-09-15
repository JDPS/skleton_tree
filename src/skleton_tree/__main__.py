# SPDX-License-Identifier: MIT
# Copyright (c) 2025 João Soares

import sys
from collections.abc import Sequence

from .dir_gen import main as dir_main
from .tree_gen import main as tree_main


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    if not args or args[0] in {"-h", "--help"}:
        print(
            "skleton-tree CLI\n\n"
            "Usage:\n"
            "  python -m skleton_tree tree [tree_gen options]\n"
            "  python -m skleton_tree dir  [dir_gen options]\n\n"
            "Examples:\n"
            "  python -m skleton_tree tree . -L 3 --files\n"
            "  python -m skleton_tree dir  .\\tree.txt . --dry-run\n"
        )
        return 0

    cmd, *rest = args
    if cmd in {"tree", "t"}:
        sys.argv = ["tree_gen.py", *rest]
        tree_main()
        return 0
    if cmd in {"dir", "gen", "g"}:
        sys.argv = ["dir_gen.py", *rest]
        dir_main()
        return 0

    print(f"Unknown command: {cmd}. Use 'tree' or 'dir'.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
