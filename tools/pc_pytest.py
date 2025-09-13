# SPDX-FileCopyrightText: 2025 João Soares
# SPDX-License-Identifier: MIT

"""
A utility script to determine the existence of test cases and execute pytest.

This script checks for the presence of test files within the "tests"
directory or other Python files matching "*test*.py" patterns in the
project. If no test files are found, pytest execution is skipped.
Otherwise, it runs pytest with specified configurations including limiting
warnings and setting a failure threshold. The script ensures the appropriate
exit code is returned based on the outcome of the pytest execution.

"""

import glob
import os
import sys

import pytest


def has_tests() -> bool:
    """Determine if the project has any test cases."""

    if os.path.isdir("tests") and list(glob.iglob("tests/**/*.py", recursive=True)):
        return True
    return bool(list(glob.iglob("*test*.py")))


if not has_tests():
    print("No tests detected; skipping pytest.")
    sys.exit(0)

ret = pytest.main(["-q", "--maxfail=1", "--disable-warnings"])
# pytest 5 = no tests collected (treat as OK)
sys.exit(0 if ret in (0, 5) else ret)
