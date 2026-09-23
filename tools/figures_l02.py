"""Generate the figures for Lecture 02 — Complexity, and the Array.

Run it from the repository root:

    python tools/figures_l02.py

Same conventions as `tools/figures.py`: PNG at 300 DPI, the course palette,
nothing borrowed. The two measured figures are real timings on the course
`Array` (`dsa/array.py`), taken with `viz.complexity.measure`.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import figures as base  # palette, rcParams and save() from tools/figures.py

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "02-complexity-and-arrays" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"


def _cells(ax, x0, y0, values, width=1.0, height=0.8, fills=None, fontsize=13):
    for i, value in enumerate(values):
        colour = fills[i] if fills else FILL
        ax.add_patch(Rectangle((x0 + i * width, y0), width, height,
                               facecolor=colour, edgecolor=SLATE, linewidth=1.4))
        ax.text(x0 + i * width + width / 2, y0 + height / 2, value,
                ha="center", va="center", fontsize=fontsize, color=SLATE)


def _clean(ax):
    ax.set_aspect("equal")
    ax.axis("off")


def _arrow(ax, start, end, colour=MUTED, style="-|>", rad=0.0, lw=1.4):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=12,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


# -- the array in memory ------------------------------------------------------


def figure_array_memory():
    fig, ax = plt.subplots(figsize=(9.2, 3.4))
    values = ["17", "4", "42", "8", "15", "23"]
    _cells(ax, 0, 1.0, values, width=1.4, height=0.9,
           fills=[FILL, FILL, HILITE, FILL, FILL, FILL])
    for i in range(len(values)):
        x = i * 1.4 + 0.7
        ax.text(x, 2.15, f"[{i}]", ha="center", fontsize=11, color=MUTED)
        ax.text(x, 0.65, f"{1000 + 8 * i}", ha="center", fontsize=10, color=MUTED,
                family="monospace")
    ax.text(-0.2, 0.65, "address", ha="right", fontsize=10, color=MUTED)
    ax.text(-0.2, 2.15, "index", ha="right", fontsize=10, color=MUTED)
    ax.text(4.2, -0.15, "address of a[i]  =  base  +  i × slot size"
            "       a[2]  =  1000 + 2 × 8  =  1016",
            ha="center", fontsize=12, color=SLATE, family="monospace")
    _arrow(ax, (3.5, -0.0), (3.5, 0.55), colour=AMBER)
    ax.set_xlim(-1.6, 8.8)
    ax.set_ylim(-0.5, 2.5)
    _clean(ax)
    ax.set_title("One block, equal slots: any index is one multiplication away",
                 fontsize=13, fontweight="bold", color=SLATE, pad=6)
    return base.save(fig, "array-memory")


def figure_references():
    fig, ax = plt.subplots(figsize=(10.0, 3.6))
    _cells(ax, 0, 2.0, ["•", "•", "•", "•"], width=1.3, height=0.8)
    ax.text(-0.25, 2.4, "Array(4)", ha="right", va="center", fontsize=12,
            color=SLATE, family="monospace")
    objects = [("42", 0.2), ("'hello'", 1.9), ("3.14", 3.6), ("[1, 2]", 5.3)]
    for i, (label, x) in enumerate(objects):
        ax.add_patch(Rectangle((x, 0.2), 1.25, 0.7, facecolor=DONE,
                               edgecolor=MUTED, linewidth=1.1, linestyle="--"))
        ax.text(x + 0.625, 0.55, label, ha="center", va="center", fontsize=11,
                family="monospace", color=SLATE)
        _arrow(ax, (i * 1.3 + 0.65, 2.1), (x + 0.625, 0.92), colour=AMBER, rad=0.08)
    ax.text(7.0, 2.4, "slots: equal size,\nside by side", ha="left", va="center",
            fontsize=10, color=MUTED)
    ax.text(7.0, 0.55, "objects: any size,\nanywhere in memory", ha="left",
            va="center", fontsize=10, color=MUTED)
    ax.set_xlim(-1.6, 9.6)
    ax.set_ylim(0, 3.1)
    _clean(ax)
    ax.set_title("A Python array stores references, so its slots can be equal "
                 "even when the objects are not",
                 fontsize=12, fontweight="bold", color=SLATE, pad=6)
    return base.save(fig, "array-references")


def figure_insert_shift():
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    before = ["a", "b", "c", "d", "e", "", ""]
    after = ["a", "b", "X", "c", "d", "e", ""]
    _cells(ax, 0, 2.6, before, fills=[FILL, FILL, HILITE, HILITE, HILITE, "white", "white"])
    _cells(ax, 0, 0.4, after, fills=[FILL, FILL, AMBER, HILITE, HILITE, HILITE, "white"])
    for i in range(7):
        ax.text(i + 0.5, 3.55, str(i), ha="center", fontsize=10, color=MUTED)
    ax.text(-0.2, 3.0, "before", ha="right", va="center", fontsize=11, color=SLATE)
    ax.text(-0.2, 0.8, "after", ha="right", va="center", fontsize=11, color=SLATE)
    for step, i in enumerate([4, 3, 2]):
        _arrow(ax, (i + 0.5, 2.55), (i + 1.5, 1.25), colour=RED, rad=-0.15)
        ax.text(i + 1.15, 1.85, f"{step + 1}", fontsize=10, color=RED,
                fontweight="bold")
    ax.text(7.3, 3.0, "size 5, capacity 7", va="center", fontsize=10, color=MUTED)
    ax.text(7.3, 0.8, "size 6", va="center", fontsize=10, color=MUTED)
    ax.text(3.5, -0.25, "insert X at index 2: shift 5 − 2 = 3 elements right, "
            "starting from the END",
            ha="center", fontsize=11, color=SLATE)
    ax.set_xlim(-1.4, 9.4)
    ax.set_ylim(-0.6, 3.9)
    _clean(ax)
    ax.set_title("Insertion costs one move per element after the gap",
                 fontsize=13, fontweight="bold", color=SLATE, pad=6)
    return base.save(fig, "insert-shift")


def figure_row_major():
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    grid = [["1", "2", "3"], ["4", "5", "6"]]
    fills = [[FILL, FILL, FILL], [HILITE, HILITE, HILITE]]
    for r in range(2):
        _cells(ax, 0, 2.3 - r * 0.8, grid[r], fills=fills[r])
    ax.text(1.5, 3.35, "2 × 3 matrix  (rows = 2, cols = 3)", ha="center",
            fontsize=11, color=SLATE)
    for c in range(3):
        ax.text(c + 0.5, 3.15, f"c={c}", ha="center", fontsize=9, color=MUTED)
    for r in range(2):
        ax.text(-0.15, 2.7 - r * 0.8, f"r={r}", ha="right", va="center",
                fontsize=9, color=MUTED)
    flat = ["1", "2", "3", "4", "5", "6"]
    _cells(ax, 4.2, 0.4, flat, fills=[FILL] * 3 + [HILITE] * 3)
    for i in range(6):
        ax.text(4.7 + i, 0.15, str(i), ha="center", fontsize=9, color=MUTED)
    ax.text(7.2, 1.55, "flat Array(6), row by row", ha="center", fontsize=11,
            color=SLATE)
    _arrow(ax, (3.1, 2.0), (4.4, 1.3), colour=AMBER, rad=-0.2)
    ax.text(5.2, 2.75, "(r, c)  lives at  r × cols + c\n(1, 2)  →  1 × 3 + 2  =  5",
            fontsize=12, color=SLATE, family="monospace", va="center")
    ax.set_xlim(-0.9, 10.5)
    ax.set_ylim(-0.1, 3.6)
    _clean(ax)
    ax.set_title("Two dimensions, one block: row-major order",
                 fontsize=13, fontweight="bold", color=SLATE, pad=6)
    return base.save(fig, "row-major")


# -- Big-O ------------------------------------------------------------------------


def figure_big_o_definition():
    import numpy as np

    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    n = np.linspace(0, 14, 400)
    f = 3 * n + 5 + 2.2 * np.sin(1.7 * n)
    cg = 4 * n
    ax.plot(n, f, color=SLATE, linewidth=2.2, label="f(n)  — the real cost")
    ax.plot(n, cg, color=AMBER, linewidth=2.2, linestyle="--",
            label="c · g(n) = 4n")
    n0 = 7.0
    ax.axvline(n0, color=MUTED, linewidth=1.0, linestyle=":")
    ax.axvspan(n0, 14, color=DONE, alpha=0.55, linewidth=0)
    ax.text(n0 + 0.15, 3, "n₀", fontsize=13, color=SLATE)
    ax.text(10.5, 8, "from n₀ on,\nf(n) ≤ c · g(n)\nfor ever", ha="center",
            fontsize=11, color=SLATE)
    ax.text(3.2, 40, "below n₀, anything\nmay happen — Big-O\ndoes not care",
            ha="center", fontsize=10, color=MUTED)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 60)
    ax.set_xlabel("input size  n")
    ax.set_ylabel("steps")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.grid(True, alpha=0.25, linewidth=0.7)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("f(n) = O(g(n)): eventually bounded above by a constant times g(n)",
                 fontsize=12.5, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "big-o-definition")


# -- measured on the course Array ---------------------------------------------


def _reference_ops():
    """Reference implementations, so the figure exists before anyone has
    written `dsa/array_ops.py`."""

    def find(arr, target):
        for i in range(len(arr)):
            if arr[i] == target:
                return i
        return -1

    def insert_front(arr, size, value):
        for i in range(size, 0, -1):
            arr[i] = arr[i - 1]
        arr[0] = value

    return find, insert_front


def figure_array_costs():
    from dsa.array import Array
    from viz.complexity import measure

    find, insert_front = _reference_ops()
    sizes = [1000, 2000, 4000, 8000, 16000, 32000]

    def make(n):
        arr = Array(n + 1)
        for i in range(n):
            arr[i] = i
        return arr, n

    accesses = 10_000

    def many_lookups(a):
        arr, n = a
        step = max(1, n // 97)                 # spread over the whole block
        i = 0
        for _ in range(accesses):
            arr[i]
            i = (i + step) % n

    # One O(1) access is a fraction of a microsecond — below what a single
    # timed call can resolve — so time 10,000 of them and plot the average.
    series = [
        (f"a[i]  — one access (average of {accesses:,})", many_lookups, GREEN,
         accesses),
        ("find(a, x)  — a miss, the worst case", lambda a: find(a[0], -1), AMBER, 1),
        ("insert at index 0", lambda a: insert_front(a[0], a[1], -1), RED, 1),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    for label, func, colour, per in series:
        measured, seconds = measure(func, sizes, make, repeat=5)
        ax.plot(measured, [s * 1e6 / per for s in seconds], "o-", color=colour,
                label=label, linewidth=2.1, markersize=5)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("n  (log scale — each step doubles n)")
    ax.set_ylabel("microseconds (log scale)")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=10, loc="center right")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("Measured on the course Array: flat is O(1), a steady climb is O(n)",
                 fontsize=12.5, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "array-costs-measured")


def figure_insert_position():
    """Insert cost depends on WHERE: best case at the end, worst at the front."""
    import time

    from dsa.array import Array

    n = 20000
    positions = [0, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000]
    micro = []
    for pos in positions:
        best = float("inf")
        for _ in range(5):
            arr = Array(n + 1)
            for i in range(n):
                arr[i] = i
            start = time.perf_counter()
            for i in range(n, pos, -1):
                arr[i] = arr[i - 1]
            arr[pos] = -1
            best = min(best, time.perf_counter() - start)
        micro.append(best * 1e6)

    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.plot(positions, micro, "o-", color=RED, linewidth=2.1, markersize=5)
    ax.annotate("worst case: insert at 0,\nshift all n", (0, micro[0]),
                xytext=(3500, micro[0] * 0.92), fontsize=10, color=SLATE,
                arrowprops=dict(arrowstyle="-", color=MUTED))
    ax.annotate("best case: insert at the end,\nshift nothing", (n, micro[-1]),
                xytext=(11000, micro[0] * 0.62), fontsize=10, color=SLATE,
                arrowprops=dict(arrowstyle="-", color=MUTED))
    ax.set_xlabel(f"insertion index   (array of n = {n:,})")
    ax.set_ylabel("microseconds")
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.25, linewidth=0.7)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("Same operation, same n — the cost depends on the input",
                 fontsize=12.5, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "insert-position")


FIGURES = [
    figure_array_memory, figure_references, figure_insert_shift,
    figure_row_major, figure_big_o_definition, figure_array_costs,
    figure_insert_position,
]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
