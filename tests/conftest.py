"""Put the repository root on sys.path so `import dsa` / `import viz` work.

This is what lets students run `pytest` from the repo root without installing
the project as a package.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def pytest_addoption(parser):
    parser.addoption(
        "--solutions",
        action="store_true",
        help="run the tests against solutions/ instead of your own code",
    )


def pytest_configure(config):
    if config.getoption("--solutions"):
        import solutions

        solutions.activate()
