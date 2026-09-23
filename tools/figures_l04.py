"""Generate the figures for Lecture 04 — Dynamic arrays.

Run it from the repository root:

    python tools/figures_l04.py

Same conventions as `tools/figures.py`. The cost charts are **counted** (element
copies), so they are identical on every machine; the CPython chart is **read
from the running interpreter** with `sys.getsizeof`, so it shows what your
Python actually does.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import figures as base  # palette, rcParams, save()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "04-dynamic-arrays" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"


def _cells(ax, x0, y0, values, fills, w=1.0, h=0.8, fontsize=12):
    for i, (value, colour) in enumerate(zip(values, fills)):
        ax.add_patch(Rectangle((x0 + i * w, y0), w, h, facecolor=colour,
                               edgecolor=SLATE, linewidth=1.3))
        ax.text(x0 + i * w + w / 2, y0 + h / 2, value, ha="center", va="center",
                fontsize=fontsize, color=SLATE)


def _clean(ax):
    ax.set_aspect("equal")
    ax.axis("off")


# -- the idea -----------------------------------------------------------------


def figure_size_capacity():
    fig, ax = plt.subplots(figsize=(9.2, 2.9))
    values = ["7", "3", "9", "4", "1", "", "", ""]
    fills = [FILL] * 5 + ["white"] * 3
    _cells(ax, 0, 0.6, values, fills)
    for i in range(8):
        ax.text(i + 0.5, 1.55, str(i), ha="center", fontsize=10, color=MUTED)
    ax.annotate("", xy=(5, 0.35), xytext=(0, 0.35),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.6))
    ax.text(2.5, 0.05, "size = 5   (slots in use)", ha="center", fontsize=11,
            color=SLATE)
    ax.annotate("", xy=(8, -0.35), xytext=(0, -0.35),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.4))
    ax.text(4, -0.7, "capacity = 8   (len of the Array underneath)", ha="center",
            fontsize=11, color=SLATE)
    ax.text(8.3, 1.0, "append writes\nhere: O(1)", fontsize=10, color=GREEN,
            va="center")
    ax.annotate("", xy=(5.5, 1.45), xytext=(8.25, 1.25),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.3,
                                connectionstyle="arc3,rad=0.3"))
    ax.set_xlim(-0.3, 10.2)
    ax.set_ylim(-1.0, 1.9)
    _clean(ax)
    ax.set_title("A dynamic array is an Array plus a count of how much of it is used",
                 fontsize=12.5, fontweight="bold", color=SLATE, pad=6)
    return base.save(fig, "size-capacity")


def figure_resize():
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    # 1: full
    _cells(ax, 0, 3.2, ["a", "b", "c", "d"], [FILL] * 4)
    ax.text(-0.2, 3.6, "1. full", ha="right", va="center", fontsize=11, color=SLATE)
    ax.text(4.3, 3.6, "size 4 = capacity 4:  append('e') has nowhere to go",
            va="center", fontsize=10, color=RED)
    # 2: new block, copy
    _cells(ax, 0, 1.6, ["a", "b", "c", "d", "", "", "", ""],
           [HILITE] * 4 + ["white"] * 4)
    ax.text(-0.2, 2.0, "2. new block\n    and copy", ha="right", va="center",
            fontsize=11, color=SLATE)
    for i in range(4):
        ax.add_patch(FancyArrowPatch((i + 0.5, 3.15), (i + 0.5, 2.45),
                                     arrowstyle="-|>", mutation_scale=11,
                                     color=AMBER, linewidth=1.3))
    ax.text(8.3, 2.0, "Array(8), then 4 copies:\nO(size)", va="center",
            fontsize=10, color=SLATE)
    # 3: switch and write
    _cells(ax, 0, 0.0, ["a", "b", "c", "d", "e", "", "", ""],
           [FILL] * 4 + [DONE] + ["white"] * 3)
    ax.text(-0.2, 0.4, "3. switch,\n    then write", ha="right", va="center",
            fontsize=11, color=SLATE)
    ax.text(8.3, 0.4, "size 5, capacity 8:\nthe next 3 appends are O(1)",
            va="center", fontsize=10, color=SLATE)
    ax.set_xlim(-2.4, 11.8)
    ax.set_ylim(-0.3, 4.3)
    _clean(ax)
    ax.set_title("Growing: allocate a bigger Array, copy everything, switch",
                 fontsize=12.5, fontweight="bold", color=SLATE, pad=6)
    return base.save(fig, "resize")


# -- counted ------------------------------------------------------------------


def _copies_per_append(n, grow):
    """Cost of each append: 1 write, plus `size` copies if it triggered a resize."""
    cap, size, costs = 1, 0, []
    for _ in range(n):
        cost = 1
        if size == cap:
            cost += size
            cap = grow(cap)
        size += 1
        costs.append(cost)
    return costs


def figure_total_copies():
    import itertools

    ns = list(range(1, 20001))
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    for label, grow, colour in [
        ("grow by 1:  capacity + 1", lambda c: c + 1, RED),
        ("grow by 100:  capacity + 100", lambda c: c + 100, AMBER),
        ("double:  capacity × 2", lambda c: 2 * c, GREEN),
    ]:
        costs = _copies_per_append(ns[-1], grow)
        total = list(itertools.accumulate(costs))
        ax.plot(ns, total, color=colour, linewidth=2.2, label=label)
    ax.plot(ns, [3 * n for n in ns], color=MUTED, linestyle=":", linewidth=1.4,
            label="3n  (the bound for doubling)")
    ax.set_yscale("log")
    ax.set_xlabel("number of appends  n")
    ax.set_ylabel("total work: writes + copies (log scale)")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("Total cost of n appends: O(n²) for any constant step, O(n) for doubling",
                 fontsize=12, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "total-copies")


def figure_append_cost():
    n = 70
    costs = _copies_per_append(n, lambda c: 2 * c)
    running = []
    total = 0
    for i, c in enumerate(costs, start=1):
        total += c
        running.append(total / i)
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    xs = list(range(1, n + 1))
    ax.bar(xs, costs, color=[RED if c > 1 else FILL for c in costs],
           edgecolor=MUTED, linewidth=0.4, label="cost of this append")
    ax.plot(xs, running, color=GREEN, linewidth=2.4,
            label="average cost so far (amortised)")
    ax.axhline(3, color=MUTED, linestyle=":", linewidth=1.2)
    ax.text(n + 0.5, 3.4, "3", color=MUTED, fontsize=10)
    for i, c in enumerate(costs, start=1):
        if c > 1 and i >= 5:
            ax.text(i, c + 0.8, f"#{i}", ha="center", fontsize=8.5, color=RED)
    ax.set_xlabel("append number")
    ax.set_ylabel("writes + copies")
    ax.set_xlim(0, n + 2)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("Doubling: a few expensive appends, spread thinly over many cheap ones",
                 fontsize=12, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "append-cost")


# -- measured from the running interpreter ------------------------------------


def figure_cpython_list():
    empty = sys.getsizeof([])
    slot = 8 if sys.maxsize > 2**32 else 4
    values, lengths, caps = [], [], []
    for i in range(1, 201):
        values.append(i)
        lengths.append(i)
        caps.append((sys.getsizeof(values) - empty) // slot)
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.step(lengths, caps, where="post", color=AMBER, linewidth=2.2,
            label="capacity (slots reserved)")
    ax.plot(lengths, lengths, color=SLATE, linewidth=1.6, label="len(list)")
    ax.set_xlabel("len(list) after each append")
    ax.set_ylabel("slots")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax.text(195, 25, f"Python {sys.version_info.major}.{sys.version_info.minor}, "
            "read with sys.getsizeof", ha="right", fontsize=9, color=MUTED)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("Python's own list grows the same way — by about 1/8 each time",
                 fontsize=12, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "cpython-list")


FIGURES = [figure_size_capacity, figure_resize, figure_total_copies,
           figure_append_cost, figure_cpython_list]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
