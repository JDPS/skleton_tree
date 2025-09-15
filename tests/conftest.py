# SPDX-License-Identifier: MIT
# Copyright (c) 2025 João Soares

import sys
from pathlib import Path

# Ensure src/ is on sys.path for tests (src-layout)
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
