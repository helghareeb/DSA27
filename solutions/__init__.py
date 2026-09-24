"""Worked solutions — read them only after you have tried.

`solutions/` mirrors the repository: `solutions/dsa/` holds the finished
modules of `dsa/`, `solutions/practice/` the question-bank problems, and
`solutions/labs/` the lab exercises. A module that is not here yet (a week not
yet taught) falls back to the skeleton in the repository.

Run the ordinary tests against the solutions instead of your own code:

    pytest --solutions tests/test_stack_queue.py -v

Run any script or tool with the solutions in place of your code:

    python tools/with_solutions.py tools/figures_l08.py

Nothing here changes your own files. See `solutions/README.md` for how to use
the solutions without wasting them.
"""

from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGES = ("dsa", "practice", "labs")


def activate():
    """Make `import dsa.x`, `practice.x` and `labs.x` find the solutions first.

    Each package's search path gets the matching `solutions/` folder in front
    of it, so a solved module shadows its skeleton and an unsolved one falls
    back to the repository. Call this before anything imports the modules.
    """
    import importlib

    for name in PACKAGES:
        package = importlib.import_module(name)
        folder = str(HERE / name)
        if folder not in package.__path__:
            package.__path__.insert(0, folder)
