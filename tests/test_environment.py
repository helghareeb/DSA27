"""Environment check — these must pass on a correctly set-up machine.

Run just these with:

    pytest tests/test_environment.py -v

If they all pass, your Python, plotting, Graphviz and notebook stack are
working and any remaining failure is in your own code, not your setup. Have
students run this first; it turns "it doesn't work" into a specific line.
"""

import shutil
import subprocess
import sys

import pytest


def test_python_version_is_at_least_3_10():
    assert sys.version_info >= (3, 10), f"found {sys.version}"


def test_running_inside_the_project_venv():
    """Catches the classic error: packages installed, but the wrong interpreter."""
    assert sys.prefix != sys.base_prefix, (
        "not running in a virtual environment — in VS Code, select the "
        "interpreter at .venv\\Scripts\\python.exe"
    )


@pytest.mark.parametrize(
    "module",
    ["numpy", "matplotlib", "networkx", "graphviz", "pydot", "IPython", "ipywidgets", "jupyterlab"],
)
def test_required_package_imports(module):
    __import__(module)


def test_graphviz_dot_binary_is_on_path():
    """The `graphviz` pip package is only a wrapper; it shells out to `dot`."""
    assert shutil.which("dot") is not None, (
        "Graphviz's `dot` binary is not on PATH. The pip package alone cannot "
        "render — install Graphviz and add its bin directory to PATH."
    )
    result = subprocess.run(["dot", "-V"], capture_output=True, text=True)
    assert result.returncode == 0


def test_matplotlib_can_render_without_a_display():
    """Rendering must work headless, or notebooks fail on some machines."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    fig.canvas.draw()
    plt.close(fig)


def test_viz_helpers_import_and_draw():
    """The course's own drawing helpers work end to end."""
    import matplotlib

    matplotlib.use("Agg")
    from viz.draw import draw_array, draw_linked_list

    draw_array([5, 2, 9, 1], highlight=2, done=[0])
    draw_linked_list(["a", "b", "c"], highlight=1)


def test_viz_frame_normalisation():
    """Both frame forms are accepted, and frames are copied not aliased."""
    from viz.animate import normalise_frames

    shared = [3, 1, 2]
    frames = normalise_frames([shared, (shared, (0, 1)), (shared, 2)])

    assert [values for values, _ in frames] == [[3, 1, 2]] * 3
    assert [highlight for _, highlight in frames] == [set(), {0, 1}, {2}]

    shared[0] = 999
    assert frames[0][0] == [3, 1, 2], "frames must snapshot, not alias, the list"


def test_complexity_measure_returns_timings():
    from viz.complexity import measure

    sizes, timings = measure(lambda n: sum(range(n)), [100, 200], lambda n: n, repeat=2)
    assert sizes == [100, 200]
    assert len(timings) == 2
    assert all(t >= 0 for t in timings)
