#!/usr/bin/env python3
"""Run the compact public causal-history reference experiment."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    target = Path(__file__).with_name("reference_interchange.py")
    cmd = [sys.executable, str(target), *sys.argv[1:]]
    raise SystemExit(subprocess.call(cmd, env=os.environ.copy()))


if __name__ == "__main__":
    main()
