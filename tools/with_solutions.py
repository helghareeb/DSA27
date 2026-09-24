"""Run a script with the worked solutions in place of your own code.

    python tools/with_solutions.py tools/figures_l08.py

Useful for the tools whose figures time a finished `dsa/` module, and for
comparing your output with the reference. See `solutions/__init__.py`.
"""

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import solutions  # noqa: E402

solutions.activate()

if len(sys.argv) < 2:
    sys.exit(__doc__)
script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name="__main__")
