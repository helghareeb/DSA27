"""Generate the figures for Lecture 08 — Searching.

Run it from the repository root:

    python tools/figures_l08.py

Same conventions as `tools/figures.py`. The diagrams are drawn from fixed,
hand-checked traces. The timing figure measures **your** `dsa/searching.py`, so
it needs a working implementation: it is the plot the `08-searching` notebook
asks you to make, and the lecture's copy was made from the instructor's
reference solution. Run it without one and every other figure is still drawn.
"""

from __future__ import annotations

import random
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

base.OUT = ROOT / "docs" / "lectures" / "08-searching" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
OUT_OF_RANGE = "#D6D6D6"
PURPLE = "#7A5195"


def box(ax, x, y, text, fill=FILL, w=1.0, h=0.6, fontsize=11, colour=SLATE):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=SLATE, linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=colour)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.4):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def row(ax, y, values, fills, w=1.0, h=0.6, fontsize=11, index=True, x0=0.0):
    for i, v in enumerate(values):
        box(ax, x0 + i * w, y, str(v), fill=fills[i], w=w, h=h, fontsize=fontsize)
        if index:
            ax.text(x0 + i * w + w / 2, y - 0.1, str(i), ha="center", va="top",
                    fontsize=7.5, color=MUTED)


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text):
    ax.set_title(text, fontsize=12.5, fontweight="bold", color=SLATE, pad=6)


# -- linear and binary --------------------------------------------------------


def figure_linear():
    fig, ax = plt.subplots(figsize=(9.6, 2.6))
    values = [7, 3, 9, 1, 8, 4, 6, 2]
    fills = [FILL] * 4 + [DONE] + ["white"] * 3
    row(ax, 0, values, fills)
    for i in range(4):
        ax.text(i + 0.5, 0.85, "≠", ha="center", fontsize=13, color=RED)
    ax.text(4.5, 0.85, "=", ha="center", fontsize=13, color=GREEN, fontweight="bold")
    arrow(ax, (-0.6, 1.25), (4.3, 1.25), colour=AMBER, lw=1.6)
    ax.text(-0.6, 1.45, "look at each element in turn", fontsize=10, color=AMBER)
    ax.text(8.4, 0.3, "linear_search(values, 8) → 4\n5 comparisons here; "
            "n when the\ntarget is last or missing", va="center", fontsize=10,
            color=SLATE)
    clean(ax, (-0.8, 13.6), (-0.5, 1.9))
    title(ax, "Linear search: no order needed, and no shortcut — O(n)")
    return base.save(fig, "linear")


def figure_halving():
    """Verified trace of binary_search(V, 41) on 16 values."""
    values = [3, 6, 8, 12, 15, 19, 21, 24, 27, 31, 34, 38, 41, 45, 48, 52]
    steps = [(0, 15, 7, "24 < 41  →  lo = 8"),
             (8, 15, 11, "38 < 41  →  lo = 12"),
             (12, 15, 13, "45 > 41  →  hi = 12"),
             (12, 12, 12, "41 = 41  →  found at 12")]
    fig, ax = plt.subplots(figsize=(10.4, 4.6))
    w = 0.62
    for r, (lo, hi, mid, note) in enumerate(steps):
        y = -r * 1.05
        fills = []
        for i in range(len(values)):
            if i == mid:
                fills.append(DONE if r == len(steps) - 1 else HILITE)
            elif lo <= i <= hi:
                fills.append(FILL)
            else:
                fills.append(OUT_OF_RANGE)
        row(ax, y, values, fills, w=w, h=0.55, fontsize=9.5)
        ax.text(-0.3, y + 0.27, f"step {r + 1}\n{hi - lo + 1} left", ha="right",
                va="center", fontsize=9, color=SLATE)
        ax.text(len(values) * w + 0.3, y + 0.27, f"lo={lo} hi={hi} mid={mid}   {note}",
                va="center", fontsize=9.5, color=SLATE, family="monospace")
    clean(ax, (-1.6, 21.8), (-3.5, 0.9))
    title(ax, "Binary search for 41: each comparison discards half of what is left")
    return base.save(fig, "halving")


def figure_bounds():
    fig, ax = plt.subplots(figsize=(9.2, 3.4))
    values = [1, 2, 2, 2, 5, 7]
    fills = [FILL, HILITE, HILITE, HILITE, FILL, FILL]
    row(ax, 0, values, fills)

    def mark(x, text, colour, above=True, dy=0.0):
        if above:
            ax.annotate(text, xy=(x, 0.62), xytext=(x, 1.35 + dy), ha="center",
                        color=colour, fontsize=10, fontweight="bold",
                        arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.4))
        else:
            ax.annotate(text, xy=(x, -0.3), xytext=(x, -1.05 - dy), ha="center",
                        va="top", color=colour, fontsize=10, fontweight="bold",
                        arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.4))

    mark(1.0, "lower_bound(2) = 1", GREEN)
    mark(4.0, "upper_bound(2) = 4", AMBER)
    mark(4.0, "lower_bound(3) = upper_bound(3) = 4\n(3 is absent: insert it here)",
         PURPLE, above=False)
    ax.text(6.5, 0.3, "count of 2 = 4 − 1 = 3", va="center", fontsize=10.5,
            color=SLATE)
    clean(ax, (-0.8, 10.2), (-2.3, 2.0))
    title(ax, "Bounds are positions between elements: where x would be inserted")
    return base.save(fig, "bounds")


def figure_jump():
    """Verified trace of jump_search on the 25 odd numbers 1..49, target 37."""
    values = list(range(1, 50, 2))
    w = 0.42
    fills = []
    for i in range(len(values)):
        if i in (4, 9, 14):
            fills.append(HILITE)
        elif i == 19:
            fills.append("#F6C9C4")
        elif i == 18:
            fills.append(DONE)
        elif 15 <= i <= 17:
            fills.append(FILL)
        else:
            fills.append("white")
    fig, ax = plt.subplots(figsize=(10.8, 2.9))
    row(ax, 0, values, fills, w=w, h=0.5, fontsize=8)
    prev = -0.2
    for i in (4, 9, 14, 19):
        x = i * w + w / 2
        arrow(ax, (prev, 0.62), (x, 0.62), colour=AMBER, rad=-0.45)
        prev = x
    ax.text(19 * w + w / 2, 1.5, "39 ≥ 37: stop", ha="center", fontsize=9, color=RED)
    arrow(ax, (15 * w + 0.05, -0.42), (18 * w + w / 2, -0.42), colour=GREEN, lw=1.6)
    ax.text(16.5 * w, -0.95, "walk forward from 15: found 37 at 18", ha="center",
            fontsize=9, color=GREEN)
    ax.text(len(values) * w + 0.3, 0.25, "step = √25 = 5\njumps check 9, 19, 29, 39\n"
            "then walk forward: at most 5 more", va="center", fontsize=9.5,
            color=SLATE)
    clean(ax, (-0.4, 15.4), (-1.3, 1.9))
    title(ax, "Jump search: jump √n at a time, then walk forward inside one block")
    return base.save(fig, "jump")


def figure_exponential():
    """Verified trace of exponential_search on the odd numbers 1..63, target 23."""
    values = list(range(1, 64, 2))
    w = 0.34
    fills = []
    for i in range(len(values)):
        if i in (0, 1, 2, 4, 8):
            fills.append(HILITE)
        elif i == 16:
            fills.append("#F6C9C4")
        elif 8 < i < 16:
            fills.append(FILL)
        else:
            fills.append("white")
    fills[11] = DONE
    fig, ax = plt.subplots(figsize=(10.8, 2.9))
    row(ax, 0, values, fills, w=w, h=0.48, fontsize=7)
    prev = 0 * w + w / 2
    for i in (1, 2, 4, 8, 16):
        x = i * w + w / 2
        arrow(ax, (prev, 0.58), (x, 0.58), colour=AMBER, rad=-0.5)
        prev = x
    ax.text(16 * w + w / 2, 1.55, "33 ≥ 23: stop", ha="center", fontsize=9, color=RED)
    ax.plot([8 * w, 8 * w, 17 * w, 17 * w], [-0.35, -0.5, -0.5, -0.35], color=GREEN,
            linewidth=1.5)
    ax.text(12.5 * w, -0.65, "binary search in slots 8..16: found 23 at 11",
            ha="center", va="top", fontsize=9, color=GREEN)
    ax.text(len(values) * w + 0.3, 0.25, "bounds 1, 2, 4, 8, 16:\nO(log i) steps, where i\n"
            "is the answer's index", va="center", fontsize=9.5, color=SLATE)
    clean(ax, (-0.4, 14.6), (-1.3, 1.95))
    title(ax, "Exponential search: double the bound, then binary search inside it")
    return base.save(fig, "exponential")


def figure_interpolation():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.0))
    n = 64
    uniform = [5 * i + (i * 7) % 4 for i in range(n)]
    skewed = list(range(n - 1)) + [4000]
    for ax, values, name, target in [
        (axes[0], uniform, "evenly spread: the guess lands close", uniform[41]),
        (axes[1], skewed, "skewed: one huge value ruins the guess", 41),
    ]:
        lo, hi = 0, n - 1
        guess = lo + (target - values[lo]) * (hi - lo) // (values[hi] - values[lo])
        where = values.index(target)
        ax.plot(range(n), values, "o", color=SLATE, markersize=3)
        ax.plot([lo, hi], [values[lo], values[hi]], "--", color=AMBER, linewidth=1.4,
                label="the straight line the guess assumes")
        ax.axhline(target, color=MUTED, linewidth=0.8)
        ax.axvline(guess, color=AMBER, linewidth=1.6, label=f"guess: index {guess}")
        ax.axvline(where, color=GREEN, linewidth=1.6, linestyle=":",
                   label=f"target {target} is at index {where}")
        ax.set_xlabel("index")
        ax.set_ylabel("value")
        ax.set_title(name, fontsize=11, color=SLATE)
        ax.legend(frameon=False, fontsize=8.5, loc="upper left")
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    fig.suptitle("Interpolation search guesses where the target should be — "
                 "if the values are evenly spread", fontsize=12, fontweight="bold",
                 color=SLATE)
    fig.tight_layout()
    return base.save(fig, "interpolation")


# -- measured -----------------------------------------------------------------


class CountingReads:
    """A read-only sequence that counts every values[i]."""

    def __init__(self, values):
        self.values, self.reads = values, 0

    def __len__(self):
        return len(self.values)

    def __getitem__(self, i):
        self.reads += 1
        return self.values[i]


def figure_measured():
    from dsa import searching
    from viz.complexity import measure

    try:
        searching.binary_search([1], 1)
        searching.linear_search([1], 1)
    except NotImplementedError:
        print("  (skipped measured.png: dsa/searching.py is not implemented yet)")
        return None

    rng = random.Random(8)
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.7))

    # left: time per search
    ax = axes[0]
    sizes = [2 ** k for k in range(10, 21, 2)]

    def data(n, k):
        values = list(range(0, 3 * n, 3))
        return values, [rng.choice(values) for _ in range(k)]

    for label, func, k, colour in [
        ("linear_search  (average of 20)", searching.linear_search, 20, RED),
        ("binary_search  (average of 2,000)", searching.binary_search, 2000, GREEN),
    ]:
        def run(payload, func=func):
            values, targets = payload
            for t in targets:
                func(values, t)
        measured, seconds = measure(run, sizes, lambda n, k=k: data(n, k), repeat=5)
        ax.plot(measured, [s * 1e6 / k for s in seconds], "o-", color=colour,
                label=label, linewidth=2.1, markersize=5)
    ax.set_xlabel("n, sorted values (log scale)")
    ax.set_ylabel("microseconds per search (log scale)")
    ax.set_title("time", fontsize=11.5, color=SLATE)

    # right: array reads per search
    ax = axes[1]

    def reads(func, values, targets):
        counted = CountingReads(values)
        for t in targets:
            func(counted, t)
        return counted.reads / len(targets)

    big = [2 ** k for k in range(10, 21, 2)]
    small = [2 ** k for k in range(10, 17, 2)]
    series = {name: [] for name in ("linear", "jump", "exponential", "binary",
                                    "interp", "interp_skew")}
    for n in big:
        values = sorted(rng.sample(range(10 * n), n))
        targets = [rng.choice(values) for _ in range(100)]
        series["binary"].append(reads(searching.binary_search, values, targets))
        series["jump"].append(reads(searching.jump_search, values, targets))
        series["exponential"].append(reads(searching.exponential_search, values, targets))
        series["interp"].append(reads(searching.interpolation_search, values, targets))
    for n in small:
        values = sorted(rng.sample(range(10 * n), n))
        series["linear"].append(reads(searching.linear_search, values,
                                      [rng.choice(values) for _ in range(40)]))
        skewed = list(range(n - 1)) + [n ** 3]
        series["interp_skew"].append(reads(searching.interpolation_search, skewed,
                                           [rng.choice(skewed[:-1]) for _ in range(40)]))
    for key, label, colour, style, xs in [
        ("interp_skew", "interpolation, skewed data", PURPLE, "s--", small),
        ("linear", "linear", RED, "o-", small),
        ("jump", "jump", AMBER, "o-", big),
        ("exponential", "exponential", MUTED, "o-", big),
        ("binary", "binary", GREEN, "o-", big),
        ("interp", "interpolation, even data", PURPLE, "o-", big),
    ]:
        ax.plot(xs, series[key], style, color=colour, label=label, linewidth=2.0,
                markersize=4.5)
    ax.set_xlabel("n (log scale)")
    ax.set_ylabel("array reads per search (log scale)")
    ax.set_title("work: how many elements each search reads", fontsize=11.5,
                 color=SLATE)

    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.grid(True, alpha=0.25, linewidth=0.7)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    axes[0].legend(frameon=False, fontsize=8.5, loc="upper left")
    axes[1].set_ylim(5, 3e6)                  # headroom for the legend
    axes[1].legend(frameon=False, fontsize=8.5, loc="upper right")
    fig.suptitle("Measured: what a sorted invariant buys", fontsize=12.5,
                 fontweight="bold", color=SLATE)
    fig.tight_layout()
    for key in series:
        print(f"    {key:12s}", [round(v, 1) for v in series[key]])
    return base.save(fig, "measured")


FIGURES = [figure_linear, figure_halving, figure_bounds, figure_jump,
           figure_exponential, figure_interpolation, figure_measured]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
