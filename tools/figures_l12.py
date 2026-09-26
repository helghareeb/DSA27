"""Generate the figures for Lecture 12 — Heaps and priority queues.

Run it from the repository root:

    python tools/figures_l12.py                       # uses YOUR dsa/heap.py
    python tools/with_solutions.py tools/figures_l12.py   # uses solutions/

Same conventions as `tools/figures.py`. The trace figures are not typed in by
hand: each one is produced by running the heap operation on a small instrumented
heap and drawing the states it passes through, so a figure cannot disagree with
the code. They, and the measured figure, therefore need a working
`dsa/heap.py`; the lecture's copies were made from the instructor's reference
solution. Without one, only the figures that need no heap are drawn.
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import figures as base  # palette, rcParams, save(), save_dot()

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "12-heaps" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
PURPLE = "#7A5195"
BAD = "#F6C9C4"
GHOST = "#EEEEEE"

# The running example of the lecture: a valid min-heap of nine values.
H = [2, 4, 3, 9, 7, 8, 5, 12, 10]
# The values `tests/test_heap.py::test_heapify_from_arbitrary_order` uses.
RAW = [9, 4, 7, 1, 8, 2, 6, 3, 5]


# -- drawing helpers ----------------------------------------------------------


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text, size=12.5):
    ax.set_title(text, fontsize=size, fontweight="bold", color=SLATE, pad=6)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.4):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def box(ax, x, y, text, fill=FILL, w=1.0, h=0.6, fontsize=11, colour=SLATE):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=SLATE, linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=colour)


def position(i, width=8.0, dy=1.25):
    """Centre of node i in a complete-tree layout: level by level, left to right."""
    level = int(math.log2(i + 1))
    first = 2 ** level - 1
    slot = i - first
    return (slot + 0.5) * width / 2 ** level, -level * dy


def tree(ax, values, fills=None, width=8.0, dy=1.25, r=0.34, fontsize=11,
         show_index=True, ghost=(), edge_colours=None, x0=0.0, y0=0.0):
    """Draw `values` as the complete binary tree it encodes.

    fills: per-index face colours. ghost: indices drawn as dashed empty places.
    edge_colours: {child_index: colour} for the edge from a child to its parent.
    """
    n = len(values)
    fills = fills or [FILL] * n
    edge_colours = edge_colours or {}
    for i in range(1, n):
        (x1, y1), (x2, y2) = position(i, width, dy), position((i - 1) // 2, width, dy)
        colour = edge_colours.get(i, MUTED)
        ax.plot([x0 + x1, x0 + x2], [y0 + y1, y0 + y2], color=colour,
                linewidth=2.2 if i in edge_colours else 1.2, zorder=1)
    for i, v in enumerate(values):
        x, y = position(i, width, dy)
        if i in ghost:
            ax.add_patch(Circle((x0 + x, y0 + y), r, facecolor="white", edgecolor=MUTED,
                                linewidth=1.1, linestyle="--", zorder=2))
            continue
        ax.add_patch(Circle((x0 + x, y0 + y), r, facecolor=fills[i], edgecolor=SLATE,
                            linewidth=1.3, zorder=2))
        ax.text(x0 + x, y0 + y, str(v), ha="center", va="center", fontsize=fontsize,
                color=SLATE, zorder=3)
        if show_index:
            ax.text(x0 + x + r * 0.75, y0 + y - r * 0.75, str(i), ha="left",
                    va="top", fontsize=7.5, color=MUTED, zorder=3)


def array_row(ax, values, fills=None, y=0.0, x0=0.0, w=0.8, h=0.5, fontsize=10):
    fills = fills or [FILL] * len(values)
    for i, v in enumerate(values):
        box(ax, x0 + i * w, y, str(v), fill=fills[i], w=w, h=h, fontsize=fontsize)
        ax.text(x0 + i * w + w / 2, y - 0.08, str(i), ha="center", va="top",
                fontsize=7.5, color=MUTED)


# -- recording what a heap operation does -------------------------------------


def working_heap():
    """The student's (or, with with_solutions.py, the reference) heap classes,
    or None when dsa/heap.py is still a skeleton."""
    from dsa.heap import MaxHeap, MinHeap, PriorityQueue

    try:
        probe = MinHeap([3, 1, 2])
        probe.push(0)
        probe.pop()
        PriorityQueue().enqueue("x", 1)
    except NotImplementedError:
        return None
    return MinHeap, MaxHeap, PriorityQueue


def recorder(cls):
    """A subclass of `cls` that snapshots the array after every swap.

    It watches `_items` through a thin wrapper, so it records whatever the
    implementation really does — the figures are drawn from these snapshots.
    """

    class Recording(cls):
        def __init__(self, values=()):
            self.frames = []
            self.comparisons = 0
            super().__init__(values)

        def _beats(self, child, parent):
            self.comparisons += 1
            return super()._beats(child, parent)

        def _sift_up(self, index):
            self.frames.append(("start", index, list(self._items)))
            super()._sift_up(index)

        def _sift_down(self, index):
            self.frames.append(("start", index, list(self._items)))
            super()._sift_down(index)

    return Recording


def swaps_between(before, after):
    """Indices whose values differ: after one swap, exactly two."""
    return [i for i, (a, b) in enumerate(zip(before, after)) if a != b]


def sift_up_states(values, pushed):
    """Every state of push(pushed) on the heap `values`, one per swap."""
    states = [list(values) + [pushed]]
    i = len(values)
    current = list(states[0])
    while i > 0 and current[i] < current[(i - 1) // 2]:
        p = (i - 1) // 2
        current[i], current[p] = current[p], current[i]
        states.append(list(current))
        i = p
    return states


def sift_down_states(values, index=0, better=min):
    """Every state of a sift-down from `index`, one per swap (min-heap)."""
    current = list(values)
    states = [list(current)]
    n = len(current)
    while True:
        kids = [c for c in (2 * index + 1, 2 * index + 2) if c < n]
        if not kids:
            break
        best = better(kids, key=lambda c: current[c])
        if current[best] >= current[index]:
            break
        current[index], current[best] = current[best], current[index]
        states.append(list(current))
        index = best
    return states


# -- 1. shape ----------------------------------------------------------------


def figure_shape():
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.3))
    cases = [
        (list("ABCDEFGHIJ"), (), GREEN, "complete: every level full,\nthe last one filled from the left"),
        (list("ABCDEFGHIJ"), (7,), RED, "not complete: a hole in the\nlast level (index 7)"),
        (list("ABCDEFG"), (5,), RED, "not complete: a missing node\n(index 5) before the last"),
    ]
    for ax, (vals, holes, colour, label) in zip(axes, cases):
        tree(ax, vals, ghost=holes, width=6.0, dy=1.1, r=0.3, show_index=False,
             fontsize=10)
        ax.text(3.0, -4.25, label, ha="center", va="center", fontsize=9.5, color=colour)
        clean(ax, (-0.1, 6.1), (-4.8, 0.5))
    fig.suptitle("A heap's shape: a complete binary tree — so the array has no holes",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "shape")


# -- 2. order ----------------------------------------------------------------


def figure_property():
    fig, axes = plt.subplots(1, 3, figsize=(11.6, 3.4))
    minh = H
    maxh = [12, 10, 8, 9, 7, 3, 5, 2, 4]
    bst = [8, 4, 12, 2, 5, 10, 14]
    for ax, vals, label, colour in [
        (axes[0], minh, "min-heap: every parent ≤ its children", GREEN),
        (axes[1], maxh, "max-heap: every parent ≥ its children", GREEN),
        (axes[2], bst, "a BST (Week 11): left < parent < right\n— a stronger, different order", PURPLE),
    ]:
        fills = [HILITE] + [FILL] * (len(vals) - 1)
        tree(ax, vals, fills=fills, width=6.0, dy=1.1, r=0.32, fontsize=10.5,
             show_index=False)
        ax.text(3.0, -4.2, label, ha="center", va="center", fontsize=9.5, color=colour)
        clean(ax, (-0.1, 6.1), (-4.8, 0.5))
    axes[0].annotate("siblings: no order\n(4 is left of 3)", xy=(4.5, -1.1),
                     xytext=(5.35, -0.15), fontsize=8.5, color=AMBER, ha="left",
                     arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.1))
    fig.suptitle("The heap property: each parent beats its children — nothing more",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "property")


# -- 3. the array is the tree ------------------------------------------------


def figure_array_is_tree():
    fig, ax = plt.subplots(figsize=(10.4, 5.4))
    fills = [FILL] * len(H)
    fills[1] = HILITE
    fills[3] = DONE
    fills[4] = DONE
    fills[0] = "#F3E3F7"
    tree(ax, H, fills=fills, width=9.0, dy=1.15, r=0.36, x0=0.4, y0=0,
         edge_colours={3: GREEN, 4: GREEN, 1: PURPLE})
    y = -4.9
    w = 0.95
    x0 = 0.5
    array_row(ax, H, fills=fills, y=y, x0=x0, w=w, h=0.55, fontsize=11)
    ax.text(x0 - 0.2, y + 0.27, "_items", ha="right", va="center", fontsize=10,
            color=SLATE, family="monospace")
    arrow(ax, (x0 + 1 * w + w / 2, y + 0.6), (x0 + 3 * w + w / 2, y + 0.6),
          colour=GREEN, rad=-0.5)
    arrow(ax, (x0 + 1 * w + w / 2, y + 0.6), (x0 + 4 * w + w / 2, y + 0.6),
          colour=GREEN, rad=-0.6)
    arrow(ax, (x0 + 1 * w + w / 2, y + 0.6), (x0 + 0 * w + w / 2, y + 0.6),
          colour=PURPLE, rad=0.6)
    ax.text(10.0, -1.0, "i = 1 (value 4)\n\nparent  (i − 1) // 2 = 0\n"
            "left     2i + 1      = 3\nright    2i + 2      = 4",
            fontsize=10.5, color=SLATE, family="monospace", va="top")
    ax.text(10.0, -3.25, "level k holds indices\n2^k − 1 … 2^(k+1) − 2",
            fontsize=9.5, color=MUTED, va="top")
    clean(ax, (-0.2, 14.4), (-5.6, 0.6))
    title(ax, "The array is the tree: no nodes, no pointers — the shape is arithmetic")
    return base.save(fig, "array-is-tree")


def figure_viz_tree():
    """The same heap as `viz.draw.draw_array_as_tree` shows it (graphviz)."""
    from viz.draw import draw_array_as_tree

    dot = draw_array_as_tree(H, highlight=0)
    return base.save_dot(dot, "viz-tree")


# -- 4. sift up ---------------------------------------------------------------


def trace_panels(states, moving_positions, notes, name, heading, width=6.0):
    k = len(states)
    fig, axes = plt.subplots(1, k, figsize=(3.05 * k, 3.9))
    for ax, st, mv, note in zip(axes, states, moving_positions, notes):
        fills = [FILL] * len(st)
        if mv is not None:
            fills[mv] = HILITE
        tree(ax, st, fills=fills, width=width, dy=1.1, r=0.33, fontsize=10)
        ax.text(width / 2, -4.15, note, ha="center", va="center", fontsize=9,
                color=SLATE)
        clean(ax, (-0.1, width + 0.1), (-4.7, 0.5))
    fig.suptitle(heading, fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, name)


def figure_sift_up(MinHeap):
    R = recorder(MinHeap)
    h = R(H)
    h.frames.clear()
    h.push(1)
    final = list(h._items)
    states = sift_up_states(H, 1)
    assert states[-1] == final, (states[-1], final)
    positions, notes = [], []
    for s in states:
        positions.append(s.index(1))
    notes = ["append 1 at index 9\nparent (9−1)//2 = 4: 7",
             "1 < 7: swap\nnow at 4, parent 1: 4",
             "1 < 4: swap\nnow at 1, parent 0: 2",
             "1 < 2: swap\nat the root: stop"]
    return trace_panels(states, positions, notes, "sift-up",
                        "push(1): append at the end, then sift up — 3 swaps, one per level")


# -- 5. sift down -------------------------------------------------------------


def figure_sift_down(MinHeap):
    h = MinHeap(H)
    returned = h.pop()
    final = list(h._items)
    start = [H[-1]] + H[1:-1]
    states = sift_down_states(start)
    assert returned == 2 and states[-1] == final, (returned, states[-1], final)
    k = len(states) + 1
    fig, axes = plt.subplots(1, k, figsize=(3.05 * k, 3.9))
    width = 6.0
    # panel 0: the root leaves, the last leaf is picked up
    fills = [FILL] * len(H)
    fills[0] = BAD
    fills[-1] = HILITE
    tree(axes[0], H, fills=fills, width=width, dy=1.1, r=0.33, fontsize=10)
    axes[0].text(width / 2, -4.15, "pop() returns the root, 2;\nthe last leaf, 10, "
                 "will fill the hole", ha="center", va="center", fontsize=9, color=SLATE)
    notes = ["10 at the root; children 4, 3\nbetter child: 3 → swap",
             "10 at 2; children 8, 5\nbetter child: 5 → swap",
             "10 at 6: no children\nstop — valid again"]
    for ax, st, note in zip(axes[1:], states, notes):
        fills = [FILL] * len(st)
        fills[st.index(10)] = HILITE
        tree(ax, st, fills=fills, width=width, dy=1.1, r=0.33, fontsize=10,
             ghost=())
        ax.text(width / 2, -4.15, note, ha="center", va="center", fontsize=9,
                color=SLATE)
    for ax in axes:
        clean(ax, (-0.1, width + 0.1), (-4.7, 0.5))
    fig.suptitle("pop(): move the last leaf to the root, then sift down past the "
                 "better child", fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "sift-down")


def figure_wrong_child():
    start = [10, 4, 3, 9, 7, 8, 5, 12]
    wrong = [4, 10, 3, 9, 7, 8, 5, 12]
    right = [3, 4, 10, 9, 7, 8, 5, 12]
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.9))
    width = 6.0
    f0 = [FILL] * 8
    f0[0] = HILITE
    tree(axes[0], start, fills=f0, width=width, dy=1.1, r=0.33, fontsize=10)
    axes[0].text(width / 2, -4.15, "10 must go down.\nWhich child goes up?",
                 ha="center", fontsize=9.5, color=SLATE)
    f1 = [FILL] * 8
    f1[0] = BAD
    f1[2] = BAD
    tree(axes[1], wrong, fills=f1, width=width, dy=1.1, r=0.33, fontsize=10,
         edge_colours={2: RED})
    axes[1].text(width / 2, -4.15, "swap with the LEFT child, 4:\n"
                 "4 > 3 — broken at the root", ha="center", fontsize=9.5, color=RED)
    f2 = [FILL] * 8
    f2[0] = DONE
    f2[2] = HILITE
    tree(axes[2], right, fills=f2, width=width, dy=1.1, r=0.33, fontsize=10,
         edge_colours={1: GREEN, 2: GREEN})
    axes[2].text(width / 2, -4.15, "swap with the BETTER child, 3:\n"
                 "3 beats both 4 and 10", ha="center", fontsize=9.5, color=GREEN)
    for ax in axes:
        clean(ax, (-0.1, width + 0.1), (-4.7, 0.5))
    fig.suptitle("The sift-down trap: the child that moves up becomes the parent "
                 "of its sibling", fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "wrong-child")


# -- 6. heapify ---------------------------------------------------------------


def figure_heapify(MinHeap):
    R = recorder(MinHeap)
    h = R(RAW)
    final = list(h._items)
    starts = [f for f in h.frames if f[0] == "start"]
    # Rebuild each stage: the state before sift_down(i), for i = 3, 2, 1, 0,
    # and the final heap.
    stages = [(idx, st) for _, idx, st in starts]
    assert [i for i, _ in stages] == [3, 2, 1, 0], stages
    panels = stages + [(None, final)]
    width = 6.0
    fig, axes = plt.subplots(1, len(panels), figsize=(3.0 * len(panels), 4.05))
    n = len(RAW)
    for ax, (idx, st) in zip(axes, panels):
        fills = [FILL] * n
        if idx is None:
            fills = [DONE] * n
            note = "done: a valid min-heap\n14 comparisons in all"
        else:
            fills[idx] = HILITE
            for j in range(idx + 1, n):
                fills[j] = DONE
            after = sift_down_states(st, idx)
            moved = len(after) - 1
            note = f"sift_down({idx}): {st[idx]} " + (
                f"moves down {moved}" if moved else "stays") + (
                " level" if moved == 1 else " levels" if moved else "")
        tree(ax, st, fills=fills, width=width, dy=1.1, r=0.33, fontsize=10)
        ax.text(width / 2, -4.15, note, ha="center", va="center", fontsize=9,
                color=SLATE)
        clean(ax, (-0.1, width + 0.1), (-4.7, 0.5))
    assert h.comparisons == 14, h.comparisons
    fig.suptitle("heapify([9, 4, 7, 1, 8, 2, 6, 3, 5]): sift down from the last "
                 "parent, index 3, back to the root", fontsize=12.5,
                 fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "heapify")


# -- 7. why build-heap is O(n) ------------------------------------------------


def figure_build_sum():
    n = 2 ** 15 - 1                                  # a perfect tree of height 14
    height = 14
    levels = list(range(height + 1))                 # depth d
    nodes = [2 ** d for d in levels]
    down = [height - d for d in levels]              # sift_down: levels below
    up = levels                                      # sift_up: levels above
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.3), sharey=True)
    for ax, cost, label, colour in [
        (axes[0], down, "heapify: sift DOWN — at most (height below) swaps", GREEN),
        (axes[1], up, "n pushes: sift UP — at most (depth) swaps", RED),
    ]:
        work = [c * k for c, k in zip(cost, nodes)]
        ax.barh(levels, work, color=colour, alpha=0.85)
        for d, wk, c in zip(levels, work, cost):
            ax.text(wk + 1500, d, f"{nodes[d]:,} × {c}", va="center", fontsize=7.8,
                    color=SLATE)
        total = sum(work)
        ax.set_title(f"{label}\ntotal at most {total:,} swaps  "
                     f"= {total / n:.2f} n", fontsize=10.5, color=SLATE)
        ax.set_xlabel("worst-case swaps at this level  (nodes × swaps each)")
        ax.set_xlim(0, 260_000)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    axes[0].set_ylabel("depth (0 = root)")
    axes[0].invert_yaxis()
    fig.suptitle(f"A perfect heap of n = {n:,}: most nodes are near the bottom — "
                 "so let them do the least work", fontsize=12.5, fontweight="bold",
                 color=SLATE)
    fig.tight_layout()
    return base.save(fig, "build-sum")


# -- 8. heap sort, revisited -------------------------------------------------


def figure_heap_sort():
    from dsa.sorting import heap_sort_steps

    values = [5, 2, 9, 1, 7, 3]
    try:
        frames = list(heap_sort_steps(values))
    except NotImplementedError:
        print("  (skipped heap-sort.png: dsa/sorting.py heap_sort is not implemented yet)")
        return None
    states = [f[0] for f in frames]
    # frames: input, heap built, then one per extraction, then the final state
    show = [states[0], states[1]] + states[2:-1]
    labels = ["input", "after heapify:\na max-heap"] + [
        f"swap root ↔ slot {len(values) - k}, then sift down in slots 0..{len(values) - k - 1}"
        for k in range(1, len(show) - 1)]
    fig, ax = plt.subplots(figsize=(10.6, 0.78 * len(show) + 0.8))
    w = 0.9
    for r, (st, lab) in enumerate(zip(show, labels)):
        y = -r * 0.78
        sorted_from = len(values) - (r - 1) if r >= 2 else len(values)
        fills = []
        for i in range(len(values)):
            if r == 0:
                fills.append("white")
            elif r == len(show) - 1:
                fills.append(DONE)
            elif i >= sorted_from:
                fills.append(DONE)
            else:
                fills.append(HILITE if i == 0 else FILL)
        for i, v in enumerate(st):
            box(ax, i * w, y, str(v), fill=fills[i], w=w, h=0.55, fontsize=10.5)
        ax.text(len(values) * w + 0.3, y + 0.27, lab.replace("\n", " "), va="center",
                fontsize=9, color=SLATE)
    for i in range(len(values)):
        ax.text(i * w + w / 2, -(len(show) - 1) * 0.78 - 0.12, str(i), ha="center",
                va="top", fontsize=7.5, color=MUTED)
    assert show[-1] == sorted(values), show[-1]
    clean(ax, (-0.2, 12.8), (-(len(show) - 1) * 0.78 - 0.5, 0.75))
    title(ax, "heap_sort (Week 10): heapify a max-heap, then pop the maximum to the "
              "back, n − 1 times")
    return base.save(fig, "heap-sort")


# -- 9. measured --------------------------------------------------------------


def figure_measured(MinHeap):
    from viz.complexity import measure

    class Counting(MinHeap):
        count = 0

        def _beats(self, child, parent):
            Counting.count += 1
            return child < parent

    def by_heapify(values):
        MinHeap(values)

    def by_pushes(values):
        h = MinHeap()
        for v in values:
            h.push(v)

    rng = random.Random(12)

    def shuffled(n):
        values = list(range(n))
        rng.shuffle(values)
        return values

    def descending(n):                               # worst case for pushes
        return list(range(n, 0, -1))

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.7))

    ax = axes[0]
    sizes = [2 ** k for k in range(10, 17)]
    series = {}
    for label, func, make, colour, style in [
        ("n pushes, descending input", by_pushes, descending, RED, "o-"),
        ("n pushes, random input", by_pushes, shuffled, AMBER, "o--"),
        ("heapify, descending input", by_heapify, descending, GREEN, "o-"),
        ("heapify, random input", by_heapify, shuffled, PURPLE, "o--"),
    ]:
        measured, seconds = measure(func, sizes, make, repeat=3)
        series[label] = seconds
        ax.plot(measured, [s * 1e3 for s in seconds], style, color=colour, label=label,
                linewidth=2.0, markersize=4.5)
    ax.set_xlabel("n (log scale)")
    ax.set_ylabel("milliseconds to build the heap (log scale)")
    ax.set_title("time", fontsize=11.5, color=SLATE)

    ax = axes[1]
    sizes = [2 ** k for k in range(4, 17)]
    counts = {}
    for label, build, make, colour, style in [
        ("n pushes, descending input", by_pushes, descending, RED, "o-"),
        ("n pushes, random input", by_pushes, shuffled, AMBER, "o--"),
        ("heapify, descending input", by_heapify, descending, GREEN, "o-"),
        ("heapify, random input", by_heapify, shuffled, PURPLE, "o--"),
    ]:
        per = []
        for n in sizes:
            values = make(n)
            Counting.count = 0
            if build is by_heapify:
                Counting(values)
            else:
                h = Counting()
                for v in values:
                    h.push(v)
            per.append(Counting.count / n)
        counts[label] = per
        ax.plot(sizes, per, style, color=colour, label=label, linewidth=2.0,
                markersize=4.5)
    ax.plot(sizes, [math.log2(n) for n in sizes], ":", color=MUTED, linewidth=1.3,
            label="log₂ n, for reference")
    ax.set_xlabel("n (log scale)")
    ax.set_ylabel("comparisons per element")
    ax.set_title("work: comparisons (_beats calls) per element", fontsize=11.5,
                 color=SLATE)
    ax.set_xscale("log", base=2)
    ax.set_ylim(0, 19)

    axes[0].set_xscale("log", base=2)
    axes[0].set_yscale("log")
    for ax in axes:
        ax.grid(True, alpha=0.25, linewidth=0.7)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
        ax.legend(frameon=False, fontsize=8.3, loc="upper left")
    fig.suptitle("Measured: heapify against n pushes", fontsize=12.5,
                 fontweight="bold", color=SLATE)
    fig.tight_layout()
    for label, seconds in series.items():
        print(f"    {label:28s} ms:", [round(s * 1e3, 1) for s in seconds])
    for label, per in counts.items():
        print(f"    {label:28s} cmp/n:", [round(v, 2) for v in per])
    return base.save(fig, "measured")


def main():
    print(f"Generating figures into {base.OUT.relative_to(ROOT)}")
    figure_shape()
    figure_property()
    figure_array_is_tree()
    figure_viz_tree()
    figure_wrong_child()
    figure_build_sum()
    heaps = working_heap()
    if heaps is None:
        print("  (skipped sift-up, sift-down, heapify and measured: "
              "dsa/heap.py is not implemented yet)")
    else:
        MinHeap = heaps[0]
        figure_sift_up(MinHeap)
        figure_sift_down(MinHeap)
        figure_heapify(MinHeap)
        figure_measured(MinHeap)
    figure_heap_sort()
    print("Done.")


if __name__ == "__main__":
    main()
