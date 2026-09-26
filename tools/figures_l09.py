"""Generate the figures for Lecture 09 — Basic sorting.

Run it from the repository root:

    python tools/figures_l09.py                       # measures YOUR dsa/sorting.py
    python tools/with_solutions.py tools/figures_l09.py   # measures solutions/

Same conventions as `tools/figures.py`. The pass-by-pass diagrams are drawn from
traces computed here on plain lists and checked against Python's `sorted`, so
they need nothing from `dsa/`. The frames figure runs `bubble_sort_steps`, and
the three measured figures time and count **your** `dsa/sorting.py`: they need a
working implementation (the lecture's copies were made from the instructor's
reference solution). Without one, every other figure is still drawn.
"""

from __future__ import annotations

import inspect
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import figures as base  # palette, rcParams, save()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "09-sorting-basic" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
PURPLE = "#7A5195"
BLUE = "#3A5A8C"
PINK = "#F6C9C4"

A = [5, 2, 9, 1, 7, 3]          # the lecture's running example


def box(ax, x, y, text, fill=FILL, w=1.0, h=0.6, fontsize=11, colour=SLATE, edge=SLATE):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=colour)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.4):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def row(ax, y, values, fills, w=1.0, h=0.6, fontsize=11, index=False, x0=0.0):
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


# -- traces on plain lists, checked against sorted() ---------------------------


def bubble_passes(values):
    """[(state after the pass, comparisons, swaps)], with the early exit."""
    a, out = list(values), []
    for end in range(len(a) - 1, 0, -1):
        comps = swaps = 0
        for j in range(end):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
        out.append((list(a), comps, swaps))
        if swaps == 0:
            break
    assert a == sorted(values)
    return out


def selection_rounds(values):
    """[(state after round i, i, index of the minimum, comparisons)]."""
    a, out = list(values), []
    for i in range(len(a) - 1):
        smallest, comps = i, 0
        for j in range(i + 1, len(a)):
            comps += 1
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
        out.append((list(a), i, smallest, comps))
    assert a == sorted(values)
    return out


def insertion_rounds(values):
    """[(state after inserting a[i], i, final index of the inserted value, shifts)]."""
    a, out = list(values), []
    for i in range(1, len(a)):
        current, j = a[i], i - 1
        while j >= 0 and a[j] > current:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = current
        out.append((list(a), i, j + 1, i - (j + 1)))
    assert a == sorted(values)
    return out


# -- the diagrams ---------------------------------------------------------------


def figure_stability():
    """Sort four records by grade: a stable sort keeps Omar before Laila."""
    records = [("B", "Omar"), ("A", "Sara"), ("B", "Laila"), ("A", "Ali")]

    def by_grade_insertion(items):
        a = list(items)
        for i in range(1, len(a)):
            cur, j = a[i], i - 1
            while j >= 0 and a[j][0] > cur[0]:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = cur
        return a

    def by_grade_selection(items):
        a = list(items)
        for i in range(len(a) - 1):
            m = i
            for j in range(i + 1, len(a)):
                if a[j][0] < a[m][0]:
                    m = j
            a[i], a[m] = a[m], a[i]
        return a

    stable = by_grade_insertion(records)
    unstable = by_grade_selection(records)
    assert stable == [("A", "Sara"), ("A", "Ali"), ("B", "Omar"), ("B", "Laila")]
    assert unstable == [("A", "Sara"), ("A", "Ali"), ("B", "Laila"), ("B", "Omar")]

    colour_of = {"Omar": HILITE, "Laila": "#F9D9A0", "Sara": FILL, "Ali": "#D5E0F0"}
    fig, ax = plt.subplots(figsize=(10.2, 3.9))
    w = 1.55
    rows = [(records, "input (arrival order)", 2.2),
            (stable, "insertion sort by grade: STABLE", 1.0),
            (unstable, "selection sort by grade: NOT stable", -0.2)]
    for items, label, y in rows:
        for i, (g, name) in enumerate(items):
            box(ax, i * w, y, f"{g} · {name}", fill=colour_of[name], w=w, h=0.62,
                fontsize=10.5)
        ax.text(4 * w + 0.25, y + 0.31, label, va="center", fontsize=10.5,
                color=GREEN if "STABLE" in label else (RED if "NOT" in label else SLATE),
                fontweight="bold" if label != rows[0][1] else "normal")
    ax.text(2 * w + 0.1, 0.8, "Omar still before Laila", ha="left", va="center",
            fontsize=9, color=GREEN)
    ax.text(2 * w + 0.1, -0.4, "Laila jumped over Omar", ha="left", va="center",
            fontsize=9, color=RED)
    clean(ax, (-0.2, 11.4), (-0.7, 3.1))
    title(ax, "Stability: equal keys keep the order they arrived in")
    return base.save(fig, "stability")


def figure_bubble():
    passes = bubble_passes(A)
    n = len(A)
    fig, ax = plt.subplots(figsize=(10.0, 4.3))
    rows = [(list(A), None, None)] + [(s, c, k) for s, c, k in passes]
    for r, (state, comps, swaps) in enumerate(rows):
        y = -r * 0.95
        placed = n if r == len(rows) - 1 else r            # last row: all in place
        fills = [DONE if i >= n - placed else FILL for i in range(n)]
        row(ax, y, state, fills, w=0.8, h=0.58)
        label = "start" if r == 0 else f"after pass {r}"
        ax.text(-0.25, y + 0.29, label, ha="right", va="center", fontsize=9.5, color=SLATE)
        if comps is not None:
            note = f"{comps} comparisons, {swaps} swaps"
            if swaps == 0:
                note += "  →  no swap: stop early"
            ax.text(n * 0.8 + 0.3, y + 0.29, note, va="center", fontsize=9.5,
                    color=RED if swaps == 0 else SLATE)
    clean(ax, (-2.2, 10.6), (-(len(rows) - 1) * 0.95 - 0.2, 0.8))
    title(ax, "Bubble sort: each pass carries the largest remaining value to the end")
    return base.save(fig, "bubble")


def figure_selection():
    rounds = selection_rounds(A)
    n = len(A)
    fig, ax = plt.subplots(figsize=(10.0, 4.6))
    row(ax, 0, A, [FILL] * n, w=0.8, h=0.58)
    ax.text(-0.25, 0.29, "start", ha="right", va="center", fontsize=9.5, color=SLATE)
    for r, (state, i, smallest, comps) in enumerate(rounds, start=1):
        y = -r * 0.95
        fills = [DONE if k <= i else FILL for k in range(n)]
        if r == len(rounds):
            fills = [DONE] * n
        row(ax, y, state, fills, w=0.8, h=0.58)
        ax.text(-0.25, y + 0.29, f"i = {i}", ha="right", va="center", fontsize=9.5,
                color=SLATE)
        if smallest != i:
            x1, x2 = i * 0.8 + 0.4, smallest * 0.8 + 0.4
            arrow(ax, (x2, y + 0.62), (x1, y + 0.62), colour=AMBER, rad=0.35)
            note = f"{comps} comparison{'s' * (comps != 1)}; min at {smallest}: swap with {i}"
        else:
            note = f"{comps} comparison{'s' * (comps != 1)}; min already at {i}: no swap"
        ax.text(n * 0.8 + 0.3, y + 0.29, note, va="center", fontsize=9.5, color=SLATE)
    clean(ax, (-1.5, 11.6), (-len(rounds) * 0.95 - 0.2, 0.8))
    title(ax, "Selection sort: find the minimum of the rest, swap it into place")
    return base.save(fig, "selection")


def figure_insertion():
    rounds = insertion_rounds(A)
    n = len(A)
    fig, ax = plt.subplots(figsize=(10.0, 4.6))
    fills = [DONE] + [FILL] * (n - 1)
    row(ax, 0, A, fills, w=0.8, h=0.58)
    ax.text(-0.25, 0.29, "start", ha="right", va="center", fontsize=9.5, color=SLATE)
    for r, (state, i, where, shifts) in enumerate(rounds, start=1):
        y = -r * 0.95
        fills = [DONE if k <= i else FILL for k in range(n)]
        fills[where] = HILITE
        row(ax, y, state, fills, w=0.8, h=0.58)
        ax.text(-0.25, y + 0.29, f"i = {i}", ha="right", va="center", fontsize=9.5,
                color=SLATE)
        if shifts:
            arrow(ax, (i * 0.8 + 0.4, y + 0.62), (where * 0.8 + 0.4, y + 0.62),
                  colour=AMBER, rad=0.35)
        note = (f"insert {state[where]}: {shifts} shift" + ("" if shifts == 1 else "s"))
        ax.text(n * 0.8 + 0.3, y + 0.29, note, va="center", fontsize=9.5, color=SLATE)
    total = sum(s for *_, s in rounds)
    ax.text(n * 0.8 + 0.3, -len(rounds) * 0.95 - 0.55,
            f"{total} shifts in all = the number of inversions of the input",
            fontsize=9.5, color=GREEN)
    clean(ax, (-1.5, 11.0), (-len(rounds) * 0.95 - 0.8, 0.8))
    title(ax, "Insertion sort: grow a sorted prefix, one value at a time")
    return base.save(fig, "insertion")


def figure_frames():
    """Every frame of bubble_sort_steps([5, 2, 9, 1, 7]), as the animation shows it."""
    from dsa import sorting

    try:
        frames = list(sorting.bubble_sort_steps([5, 2, 9, 1, 7]))
    except NotImplementedError:
        print("  (skipped frames.png: dsa/sorting.py is not implemented yet)")
        return None
    from viz.style import as_index_set, colours

    cols = 6
    rows_ = (len(frames) + cols - 1) // cols
    fig, axes = plt.subplots(rows_, cols, figsize=(11.0, 1.9 * rows_ + 0.4))
    for k, ax in enumerate(axes.flat):
        ax.axis("off")
        if k >= len(frames):
            continue
        values, highlight = frames[k]
        highlight = as_index_set(highlight)
        for i, v in enumerate(values):
            fill, edge = colours(i, highlight)
            ax.bar(i, v, color=fill, edgecolor=edge, linewidth=1.0, width=0.8)
            ax.text(i, v + 0.3, str(v), ha="center", fontsize=7.5, color=SLATE)
        ax.set_ylim(0, 11)
        label = f"frame {k + 1}"
        if highlight:
            label += f"  {tuple(sorted(highlight))}"
        ax.set_title(label, fontsize=8.5, color=SLATE)
    fig.suptitle(f"bubble_sort_steps([5, 2, 9, 1, 7]): {len(frames)} yields, "
                 f"{len(frames)} frames — highlighted: the pair about to be compared",
                 fontsize=11.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "frames")


def figure_counting():
    values = [3, 1, 4, 1, 5, 0, 3]
    k = max(values) + 1
    counts = [0] * k
    for v in values:
        counts[v] += 1
    out = [v for v in range(k) for _ in range(counts[v])]
    assert out == sorted(values)

    fig, ax = plt.subplots(figsize=(10.0, 4.4))
    w = 0.9
    row(ax, 2.4, values, [FILL] * len(values), w=w, h=0.6)
    ax.text(-0.3, 2.7, "values", ha="right", va="center", fontsize=10, color=SLATE)
    x0 = 0.9
    row(ax, 1.0, counts, [HILITE] * k, w=w, h=0.6, x0=x0)
    for v in range(k):
        ax.text(x0 + v * w + w / 2, 1.72, f"{v}", ha="center", fontsize=9, color=AMBER,
                fontweight="bold")
    ax.text(-0.3, 1.3, "counts", ha="right", va="center", fontsize=10, color=SLATE)
    ax.text(x0 + k * w + 0.3, 1.3, "counts[v] = how many times v occurs\n"
            "one pass over values: n writes", va="center", fontsize=9.5, color=SLATE)
    row(ax, -0.4, out, [DONE] * len(out), w=w, h=0.6)
    ax.text(-0.3, -0.1, "output", ha="right", va="center", fontsize=10, color=SLATE)
    ax.text(len(out) * w + 0.3, -0.1, "for v = 0 .. k−1: write v, counts[v] times\n"
            "no two values are ever compared", va="center", fontsize=9.5, color=SLATE)
    arrow(ax, (3.0, 2.3), (3.0, 1.75), colour=MUTED)
    arrow(ax, (3.0, 0.95), (3.0, 0.3), colour=MUTED)
    clean(ax, (-1.4, 11.2), (-0.7, 3.2))
    title(ax, "Counting sort: count each value, then write them out in order — O(n + k)")
    return base.save(fig, "counting")


def figure_decision_tree():
    """Insertion sort's comparisons on three values a, b, c: six leaves, height 3."""
    fig, ax = plt.subplots(figsize=(10.4, 4.8))

    def node(x, y, text, leaf=False):
        fill = DONE if leaf else FILL
        ax.add_patch(FancyBboxPatch((x - 0.62, y - 0.24), 1.24, 0.48,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor=fill, edgecolor=SLATE, linewidth=1.1))
        ax.text(x, y, text, ha="center", va="center", fontsize=10.5, color=SLATE,
                family="monospace" if not leaf else None)

    def edge(x1, y1, x2, y2, label):
        ax.plot([x1, x2], [y1 - 0.24, y2 + 0.24], color=MUTED, linewidth=1.1, zorder=0)
        ax.text((x1 + x2) / 2 + (0.18 if x2 > x1 else -0.18), (y1 + y2) / 2, label,
                ha="left" if x2 > x1 else "right", va="center", fontsize=8.5,
                color=AMBER)

    node(0, 3, "a ≤ b ?")
    node(-3.2, 2, "b ≤ c ?")
    node(3.2, 2, "a ≤ c ?")
    edge(0, 3, -3.2, 2, "yes")
    edge(0, 3, 3.2, 2, "no")
    node(-4.6, 1, "a b c", leaf=True)
    node(-1.8, 1, "a ≤ c ?")
    edge(-3.2, 2, -4.6, 1, "yes")
    edge(-3.2, 2, -1.8, 1, "no")
    node(1.8, 1, "b a c", leaf=True)
    node(4.6, 1, "b ≤ c ?")
    edge(3.2, 2, 1.8, 1, "yes")
    edge(3.2, 2, 4.6, 1, "no")
    node(-2.6, 0, "a c b", leaf=True)
    node(-1.0, 0, "c a b", leaf=True)
    edge(-1.8, 1, -2.6, 0, "yes")
    edge(-1.8, 1, -1.0, 0, "no")
    node(3.8, 0, "b c a", leaf=True)
    node(5.4, 0, "c b a", leaf=True)
    edge(4.6, 1, 3.8, 0, "yes")
    edge(4.6, 1, 5.4, 0, "no")
    ax.text(-6.4, 0.0, "3! = 6 orders\n= 6 leaves\n\nheight ≥ ⌈log₂ 6⌉ = 3",
            fontsize=10, color=SLATE, va="center")
    ax.set_xlim(-7.0, 6.4)
    ax.set_ylim(-0.5, 3.5)
    ax.axis("off")
    title(ax, "A comparison sort is a decision tree: one leaf for every possible order")
    return base.save(fig, "decision_tree")


# -- measured -------------------------------------------------------------------


class Key:
    """A value that counts every comparison made on it (class-wide counter)."""

    compares = 0
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        Key.compares += 1
        return self.v < other.v

    def __gt__(self, other):
        Key.compares += 1
        return self.v > other.v

    def __le__(self, other):
        Key.compares += 1
        return self.v <= other.v

    def __ge__(self, other):
        Key.compares += 1
        return self.v >= other.v


def inputs(n, rng):
    nearly = list(range(n))
    for _ in range(max(1, n // 100)):          # 1% of positions: swap with a neighbour
        i = rng.randrange(n - 1)
        nearly[i], nearly[i + 1] = nearly[i + 1], nearly[i]
    return {"random": rng.sample(range(n), n), "sorted": list(range(n)),
            "nearly sorted": nearly, "reversed": list(range(n, 0, -1))}


def count_work(sort, values):
    """(comparisons, writes into the course Array) for one call of `sort`."""
    from dsa.array import Array

    writes = [0]
    original = Array.__setitem__

    def counting(self, i, v):
        writes[0] += 1
        original(self, i, v)

    Key.compares = 0
    Array.__setitem__ = counting
    try:
        result = sort([Key(v) for v in values])
    finally:
        Array.__setitem__ = original
    assert [k.v for k in result] == sorted(values)
    return Key.compares, writes[0]


def working(sorting):
    try:
        for f in (sorting.bubble_sort, sorting.selection_sort, sorting.insertion_sort):
            f([2, 1])
        sorting.counting_sort([2, 1])
    except NotImplementedError:
        return False
    return True


def figure_counts():
    from dsa import sorting

    if not working(sorting):
        print("  (skipped counts.png: dsa/sorting.py is not implemented yet)")
        return None
    n = 1000
    data = inputs(n, random.Random(9))
    sorts = [("bubble", sorting.bubble_sort, RED), ("selection", sorting.selection_sort, AMBER),
             ("insertion", sorting.insertion_sort, GREEN)]
    table = {name: {kind: count_work(f, v) for kind, v in data.items()}
             for name, f, _ in sorts}
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.4))
    kinds = list(data)
    width = 0.26
    for panel, (ax, which, label) in enumerate(
            [(axes[0], 0, "comparisons"), (axes[1], 1, "writes into the Array")]):
        for s, (name, _, colour) in enumerate(sorts):
            heights = [max(table[name][k][which], 0.8) for k in kinds]
            xs = [i + (s - 1) * width for i in range(len(kinds))]
            ax.bar(xs, heights, width=width, color=colour, label=name, alpha=0.9)
            for x, k in zip(xs, kinds):
                real = table[name][k][which]
                ax.text(x, max(real, 0.8) * 1.15, f"{real:,}", ha="center", va="bottom",
                        rotation=90, fontsize=7.5, color=SLATE)
        ax.set_yscale("log")
        ax.set_ylim(0.5, 3e8)                 # headroom for the labels and legend
        ax.set_xticks(range(len(kinds)))
        ax.set_xticklabels(kinds, fontsize=9.5)
        ax.set_title(label, fontsize=11.5, color=SLATE)
        ax.grid(True, axis="y", alpha=0.25, linewidth=0.7)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    axes[0].legend(frameon=False, fontsize=9, loc="upper left", ncol=3)
    fig.suptitle(f"Measured on n = {n:,} values: the same O(n²), very different work",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    for name in table:
        print(f"    {name:10s}", {k: table[name][k] for k in kinds})
    return base.save(fig, "counts")


def best_time(func, make, repeat=3):
    best = float("inf")
    for _ in range(repeat):
        payload = make()
        start = time.perf_counter()
        func(payload)
        best = min(best, time.perf_counter() - start)
    return best


def figure_measured():
    from dsa import sorting

    if not working(sorting):
        print("  (skipped measured.png: dsa/sorting.py is not implemented yet)")
        return None
    rng = random.Random(27)
    sizes = [200, 400, 800, 1600]
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.6))

    ax = axes[0]
    for label, func, colour, style in [
        ("bubble_sort", sorting.bubble_sort, RED, "o-"),
        ("selection_sort", sorting.selection_sort, AMBER, "o-"),
        ("insertion_sort", sorting.insertion_sort, GREEN, "o-"),
        ("counting_sort", sorting.counting_sort, PURPLE, "s-"),
        ("Python's sorted (C, for scale)", sorted, MUTED, "^--"),
    ]:
        seconds = [best_time(func, lambda n=n: rng.sample(range(n), n)) for n in sizes]
        ax.plot(sizes, [s * 1e3 for s in seconds], style, color=colour, label=label,
                linewidth=2.0, markersize=5)
        print(f"    random  {label:32s}", [round(s * 1e3, 2) for s in seconds])
    ax.set_title("random input", fontsize=11.5, color=SLATE)

    ax = axes[1]
    for kind, colour, style in [("reversed", RED, "o-"), ("random", AMBER, "o-"),
                                ("nearly sorted", GREEN, "o-"), ("sorted", BLUE, "s-")]:
        seconds = [best_time(sorting.insertion_sort,
                             lambda n=n: inputs(n, random.Random(n))[kind]) for n in sizes]
        ax.plot(sizes, [s * 1e3 for s in seconds], style, color=colour, label=kind,
                linewidth=2.0, markersize=5)
        print(f"    insertion {kind:14s}", [round(s * 1e3, 2) for s in seconds])
    ax.set_title("insertion_sort: the input decides", fontsize=11.5, color=SLATE)

    axes[0].set_ylim(1e-2, 1e6)                   # headroom for the legends
    axes[1].set_ylim(0.3, 1e6)
    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_xlabel("n (log scale)")
        ax.set_ylabel("milliseconds (log scale)")
        ax.set_xticks(sizes)
        ax.set_xticklabels([str(n) for n in sizes])
        ax.grid(True, alpha=0.25, linewidth=0.7)
        ax.legend(frameon=False, fontsize=8.5, loc="upper left")
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    fig.suptitle("Measured: double n, and an O(n²) sort takes four times as long",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "measured")


def figure_watching():
    """What exhausting a _steps generator costs when every frame is a copy."""
    from dsa import sorting

    if not working(sorting):
        print("  (skipped watching.png: dsa/sorting.py is not implemented yet)")
        return None
    rng = random.Random(3)
    sizes = [50, 100, 200, 400]

    def exhaust_with_copies(values):
        for _ in sorting.bubble_sort_steps(values):
            pass

    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    series = [("exhaust bubble_sort_steps: a list copy per frame", exhaust_with_copies,
               RED)]
    if "snapshot" in inspect.signature(sorting.bubble_sort_steps).parameters:
        series.append(("bubble_sort: snapshot=_live, no copies", sorting.bubble_sort,
                       GREEN))
    for label, func, colour in series:
        seconds = [best_time(func, lambda n=n: rng.sample(range(n), n), repeat=2)
                   for n in sizes]
        ax.plot(sizes, [s * 1e3 for s in seconds], "o-", color=colour, label=label,
                linewidth=2.0, markersize=5)
        ratios = [round(b / a, 1) for a, b in zip(seconds, seconds[1:])]
        print(f"    {label:52s}", [round(s * 1e3, 1) for s in seconds], "ratios", ratios)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_ylim(1, 1e5)
    ax.set_xticks(sizes)
    ax.set_xticklabels([str(n) for n in sizes])
    ax.set_xlabel("n (log scale)")
    ax.set_ylabel("milliseconds (log scale)")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("The price of watching: ×8 per doubling (n³) against ×4 (n²)",
                 fontsize=12, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "watching")


FIGURES = [figure_stability, figure_bubble, figure_selection, figure_insertion,
           figure_frames, figure_counting, figure_decision_tree, figure_counts,
           figure_measured, figure_watching]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
