# SPDX-License-Identifier: MIT
# Copyright (c) 2025 João Soares

from pathlib import Path

from skleton_tree.tree_gen import ASCII_CHARS, UNICODE_CHARS, build_tree


def _make_sample(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    (root / "src").mkdir(parents=True)
    (root / "src" / "main.py").write_text("print('hi')\n", encoding="utf-8")
    (root / "tests").mkdir(parents=True)
    (root / "tests" / "test_main.py").write_text(
        "def test_ok(): pass\n", encoding="utf-8"
    )
    return root


def test_unicode_connectors(tmp_path: Path):
    root = _make_sample(tmp_path)
    lines = [root.name + "/"] + build_tree(
        root, level=10, show_files=True, ignores=[], chars=UNICODE_CHARS
    )
    # Expect at least one branch and one last connector in output
    assert any("├── " in ln for ln in lines)
    assert any("└── " in ln for ln in lines)
    # Guides should exist for continued branches
    assert any("│   " in ln for ln in lines)


def test_ascii_connectors(tmp_path: Path):
    root = _make_sample(tmp_path)
    lines = [root.name + "/"] + build_tree(
        root, level=10, show_files=True, ignores=[], chars=ASCII_CHARS
    )
    assert any("|-- " in ln for ln in lines)
    assert any("\\-- " in ln for ln in lines)
    assert any("|   " in ln for ln in lines)
