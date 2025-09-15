# SPDX-License-Identifier: MIT
# Copyright (c) 2025 João Soares

from pathlib import Path  # noqa: I001

from skleton_tree.dir_gen import create_structure, parse_tree_layout
from skleton_tree.tree_gen import UNICODE_CHARS, build_tree


def collect_rel_paths(root: Path) -> set[str]:
    items: set[str] = set()
    for p in root.rglob("*"):
        rel = p.relative_to(root).as_posix()
        if p.is_dir():
            items.add(rel + "/")
        else:
            items.add(rel)
    return items


def test_roundtrip_unicode(tmp_path: Path):
    # Build original structure
    src_root = tmp_path / "src_proj"
    (src_root / "pkg").mkdir(parents=True)
    (src_root / "pkg" / "mod.py").write_text("x=1\n", encoding="utf-8")
    (src_root / "data").mkdir(parents=True)
    (src_root / "data" / "info.txt").write_text("ok\n", encoding="utf-8")

    expected = collect_rel_paths(src_root)

    # Generate tree
    lines = [src_root.name + "/"] + build_tree(
        src_root, level=99, show_files=True, ignores=[], chars=UNICODE_CHARS
    )
    layout_file = tmp_path / "layout.txt"
    layout_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Recreate under new root
    out_root = tmp_path / "out_proj"
    layout = parse_tree_layout(layout_file)
    create_structure(layout, out_root, dry_run=False)

    actual = collect_rel_paths(out_root)

    assert expected == actual
