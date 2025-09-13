SPDX-FileCopyrightText: 2025 João Soares
SPDX-License-Identifier: CC-BY-4.0

# skleton-tree

A tiny utility to:
- Print a visual directory tree to the console and optionally save it to a text file (src/tree_gen.py)
- Recreate a directory and file structure from a previously saved tree layout file (src/dir_gen.py)

This is handy for documenting project structures and for quickly scaffolding skeleton directories for demos, tutorials, or tests.

## Requirements
- Python 3.12+

## Installation
You can run the scripts directly from the cloned repository; no installation is required.

Optional: create and activate a virtual environment first.

## Usage

### 1) Generate a directory tree (tree_gen.py)
Print the directory tree for a given path. You can limit depth, include files, ignore patterns, and save the output to a file.

Examples (PowerShell):
- Print a tree of the current directory, directories only:
  - `python .\src\tree_gen.py`
- Print up to 5 levels, including files:
  - `python .\src\tree_gen.py . -L 5 --files`
- Ignore common folders and save to a file:
  - `python .\src\tree_gen.py . --files --ignore ".git" --ignore "node_modules" --output tree.txt`

Key options:
- `path` (positional): root directory to start from; defaults to `.`
- `-L`, `--level` N: max depth to display (default 99)
- `--files`: include files in the tree (by default only directories are shown)
- `--ignore PATTERN`: glob ignore patterns (repeatable)
- `--output FILE`: save the tree to FILE (.txt)

The output format is compatible with the companion generator below.

### 2) Recreate a structure from a tree layout (dir_gen.py)
Given a text file produced by tree_gen.py (or a similarly formatted file), create the corresponding directory and file structure.

Examples (PowerShell):
- Create under the current directory:
  - `python .\src\dir_gen.py .\tree.txt .`
- Dry‑run (show what would be created without touching the filesystem):
  - `python .\src\dir_gen.py .\tree.txt . --dry-run`

Key options:
- `layout` (positional): path to a tree layout .txt file
- `root` (positional, optional): target root folder where the structure will be created; defaults to `.`
- `--dry-run`: preview actions only

Notes:
- Directory lines in the layout must end with a trailing `/`.
- Indentation uses blocks of 4 characters made of `│   ` or spaces `    `.
- Connectors should be `├── ` for intermediate and `└── ` for last entries at a level.

## Example
A minimal example of a saved tree (tree.txt):
```
my_project/
├── src/
│   └── main.py
└── tests/
    └── test_main.py
```
Recreate it under `./output`:
```
python .\src\dir_gen.py .\tree.txt .\output
```

## Development
- Format: black
- Tests: pytest (a helper script tools/pc_pytest.py runs pytest only if tests exist)

Run tests (PowerShell):
- `python .\tools\pc_pytest.py`

## License
- Code: MIT License (see LICENSE)
- Documentation: CC BY 4.0 (see LICENSE.docs)

## Acknowledgements
Copyright (c) 2025 João Soares
