"""Generate the figures for Lecture 10 — Advanced sorting.

Run it from the repository root:

    python tools/figures_l10.py                          # uses YOUR dsa/sorting.py
    python tools/with_solutions.py tools/figures_l10.py  # uses solutions/

Same conventions as `tools/figures.py`. Every diagram is drawn from a trace
that the script computes by running `dsa/sorting.py` itself — the merge tree,
the partitions, the heap and the stability rows are the real states of the real
code, not a drawing of what they ought to be. So the script needs a working
implementation: the lecture's copy was made from the instructor's reference
solution. The measured figure counts comparisons with a value class that adds
one to a counter in every `<`, `<=`, `>` and `>=`.
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

import figures as base  # palette, rcParams, save()

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "10-sorting-advanced" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
PURPLE = "#7A5195"
PIVOT = "#E3D3EE"
GREY = "#D6D6D6"

M = [38, 27, 43, 3, 9, 82, 10, 19]          # the merge-sort example
Q = [6, 3, 9, 1, 8, 2, 7, 4]                # the quicksort example
H = [4, 10, 3, 5, 1, 8, 2, 7]               # the heap-sort example
CARDS = [(3, "a"), (1, "b"), (3, "c"), (2, "d"), (1, "e"), (2, "f")]


def box(ax, x, y, text, fill=FILL, w=1.0, h=0.6, fontsize=11, colour=SLATE,
        edge=SLATE, lw=1.2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, linewidth=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=colour)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.2):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def row(ax, y, values, fills, w=1.0, h=0.6, fontsize=11, index=True, x0=0.0,
        edges=None):
    for i, v in enumerate(values):
        edge = edges[i] if edges else SLATE
        box(ax, x0 + i * w, y, str(v), fill=fills[i], w=w, h=h, fontsize=fontsize,
            edge=edge, lw=2.2 if edges and edge != SLATE else 1.2)
        if index:
            ax.text(x0 + i * w + w / 2, y - 0.08, str(i), ha="center", va="top",
                    fontsize=7, color=MUTED)


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text):
    ax.set_title(text, fontsize=12.5, fontweight="bold", color=SLATE, pad=6)


def sorting_module():
    from dsa import sorting
    try:
        sorting.merge_sort([2, 1])
        sorting.quick_sort([2, 1])
        sorting.heap_sort([2, 1])
    except NotImplementedError:
        return None
    return sorting


# -- merge sort ---------------------------------------------------------------


def figure_divide(sorting):
    """The split-and-merge tree of merge_sort(M), merges taken from the real frames."""
    merged = {}
    for state, highlight in sorting.merge_sort_steps(M):
        if highlight:
            lo, hi = min(highlight), max(highlight) + 1
            merged[(lo, hi)] = state[lo:hi]

    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    w, h = 0.62, 0.5
    gap = 0.55

    def segments(size):
        return [(lo, lo + size) for lo in range(0, len(M), size)]

    levels = [8, 4, 2, 1, 2, 4, 8]
    pos = {}
    for r, size in enumerate(levels):
        y = -r * 0.95
        n_seg = len(M) // size
        span = len(M) * w + (n_seg - 1) * gap
        x0 = (len(M) * w + 7 * gap - span) / 2
        for k, (lo, hi) in enumerate(segments(size)):
            x = x0 + k * (size * w + gap)
            if r <= 3:
                values = M[lo:hi]
                fill = HILITE if size == 1 else FILL
            else:
                values = merged[(lo, hi)]
                fill = DONE
            for i, v in enumerate(values):
                box(ax, x + i * w, y, str(v), fill=fill, w=w, h=h, fontsize=10)
            pos[(r, lo)] = (x + size * w / 2, y)
    for r in range(1, len(levels)):
        size, above = levels[r], levels[r - 1]
        for lo, hi in segments(size):
            if r <= 3:                                  # split: one parent above
                px, py = pos[(r - 1, (lo // above) * above)]
                cx, cy = pos[(r, lo)]
                arrow(ax, (px, py - 0.02), (cx, cy + h + 0.02), colour=MUTED, lw=1.0)
            else:                                       # merge: two runs above
                for child in (lo, lo + above):
                    cx, cy = pos[(r - 1, child)]
                    px, py = pos[(r, lo)]
                    arrow(ax, (cx, cy - 0.02), (px, py + h + 0.02), colour=GREEN, lw=1.0)
    right = len(M) * w + 7 * gap + 0.4
    ax.text(right, -0.95 * 1.5 + 0.25, "divide:\nsplit in the\nmiddle, no work", va="center",
            fontsize=9.5, color=SLATE)
    ax.text(right, -0.95 * 3 + 0.25, "base case:\none element\nis sorted", va="center",
            fontsize=9.5, color=AMBER)
    ax.text(right, -0.95 * 5 + 0.25, "combine:\nmerge two\nsorted runs", va="center",
            fontsize=9.5, color=GREEN)
    clean(ax, (-0.2, right + 1.9), (-0.95 * 6 - 0.2, h + 0.15))
    title(ax, "Merge sort: split until trivial, then merge on the way back up")
    return base.save(fig, "divide")


def figure_merge_step():
    """One moment inside _merge(a, 0, 4, 8, scratch): four values already taken."""
    a = [3, 27, 38, 43, 9, 10, 19, 82]
    scratch = [3, 9, 10, 19, "", "", "", ""]
    i, j, k = 1, 7, 4
    fig, ax = plt.subplots(figsize=(10.4, 3.7))
    w, h = 0.8, 0.55
    fills = []
    for idx in range(8):
        if idx < 4:
            fills.append(GREY if idx < i else FILL)
        else:
            fills.append(GREY if idx < j else HILITE)
    row(ax, 1.6, a, fills, w=w, h=h, fontsize=11)
    row(ax, 0, scratch, [DONE] * 4 + ["white"] * 4, w=w, h=h, fontsize=11)
    ax.text(-0.25, 1.6 + h / 2, "a", ha="right", va="center", fontsize=11,
            fontweight="bold")
    ax.text(-0.25, h / 2, "scratch", ha="right", va="center", fontsize=11,
            fontweight="bold")
    ax.plot([4 * w, 4 * w], [1.45, 2.3], color=SLATE, linewidth=2.2)
    ax.text(2 * w, 2.45, "left run a[lo:mid]", ha="center", fontsize=9.5, color=SLATE)
    ax.text(6 * w, 2.45, "right run a[mid:hi]", ha="center", fontsize=9.5, color=SLATE)
    for name, idx, y0, col in (("i", i, 1.6, SLATE), ("j", j, 1.6, SLATE),
                               ("k", k, 0.0, GREEN)):
        x = idx * w + w / 2
        ax.annotate(name, xy=(x, y0 - 0.2), xytext=(x, y0 - 0.62), ha="center",
                    fontsize=11, fontweight="bold", color=col,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.3))
    ax.text(8 * w + 0.5, 1.2,
            "a[i] = 27  <=  a[j] = 82\n→ scratch[k] = 27;  i += 1;  k += 1\n\n"
            "on a tie, take from the LEFT:\nthat one  <=  makes merge sort stable\n\n"
            "grey = already copied to scratch",
            va="center", fontsize=9.8, color=SLATE)
    clean(ax, (-1.4, 8 * w + 5.2), (-0.8, 2.75))
    title(ax, "Merging two sorted runs: compare the fronts, copy the smaller")
    return base.save(fig, "merge-step")


def figure_recursion_tree():
    n = 16
    fig, ax = plt.subplots(figsize=(10.4, 4.0))
    unit = 0.52
    gap = 0.12
    levels = int(math.log2(n))
    for d in range(levels + 1):
        size = n >> d
        count = 1 << d
        y = -d * 0.8
        total = n * unit + (count - 1) * gap
        x = (n * unit + (n - 1) * gap - total) / 2
        for c in range(count):
            fill = HILITE if size == 1 else (FILL if d < levels else DONE)
            box(ax, x, y, str(size), fill=fill, w=size * unit, h=0.5,
                fontsize=9.5 if size > 1 else 8)
            x += size * unit + gap
        label = (f"{count} × merge of {size}  =  {n} steps" if size > 1
                 else f"{count} × one element: nothing to merge")
        ax.text(n * unit + (n - 1) * gap + 0.5, y + 0.25, label, va="center",
                fontsize=9.8, color=GREEN if size > 1 else AMBER)
    ax.annotate("", xy=(-0.45, -levels * 0.8 + 0.5), xytext=(-0.45, 0.5),
                arrowprops=dict(arrowstyle="<->", color=SLATE, lw=1.2))
    ax.text(-0.6, -levels * 0.8 / 2 + 0.25, f"log₂ {n} = {levels}\nlevels that\nmerge",
            ha="right", va="center", fontsize=9.5, color=SLATE)
    ax.text((n * unit) / 2 + 1.4, -levels * 0.8 - 0.7,
            "T(n) = 2T(n/2) + n   →   n work per level × log₂ n levels  =  n log₂ n",
            ha="center", fontsize=11, color=SLATE, fontweight="bold")
    clean(ax, (-2.9, n * unit + (n - 1) * gap + 6.5), (-levels * 0.8 - 1.0, 0.75))
    title(ax, "The recursion tree of merge sort, n = 16: every level does n work")
    return base.save(fig, "recursion-tree")


# -- quicksort ----------------------------------------------------------------


def figure_partition(sorting):
    """Lomuto's partition of Q around its last element, row by row."""
    from dsa.array import Array
    a = Array.from_values(Q)
    lo, hi = 0, len(Q) - 1
    pivot = a[hi]
    boundary = lo
    rows = [(list(a), boundary, lo, "start: pivot = a[hi] = 4")]
    for j in range(lo, hi):
        if a[j] < pivot:
            note = f"j={j}: {a[j]} < 4 → swap a[{boundary}], a[{j}]; boundary={boundary + 1}"
            a[boundary], a[j] = a[j], a[boundary]
            boundary += 1
        else:
            note = f"j={j}: {a[j]} ≥ 4 → leave it"
        rows.append((list(a), boundary, j + 1, note))
    a[boundary], a[hi] = a[hi], a[boundary]
    rows.append((list(a), boundary, hi, f"swap the pivot into a[{boundary}]: done"))
    assert boundary == sorting._partition(Array.from_values(Q), 0, hi)

    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    w, h = 0.62, 0.46
    for r, (values, b, seen, note) in enumerate(rows):
        y = -r * 0.66
        final = r == len(rows) - 1
        fills = []
        for idx in range(len(values)):
            if final:
                fills.append(PIVOT if idx == b else (DONE if idx < b else HILITE))
            elif idx == hi:
                fills.append(PIVOT)
            elif idx < b:
                fills.append(DONE)
            elif idx < seen:
                fills.append(HILITE)
            else:
                fills.append("white")
        row(ax, y, values, fills, w=w, h=h, fontsize=10, index=False)
        if r == 0:
            for idx in range(len(values)):
                ax.text(idx * w + w / 2, h + 0.06, str(idx), ha="center", va="bottom",
                        fontsize=7, color=MUTED)
        ax.text(len(values) * w + 0.3, y + h / 2, note, va="center", fontsize=9.3,
                color=SLATE, family="monospace")
    y = -len(rows) * 0.66 - 0.1
    for k, (fill, text) in enumerate([(DONE, "< pivot"), (HILITE, "≥ pivot"),
                                      ("white", "not yet seen"), (PIVOT, "pivot")]):
        box(ax, k * 2.5, y, "", fill=fill, w=0.4, h=0.3)
        ax.text(k * 2.5 + 0.55, y + 0.15, text, va="center", fontsize=9.5, color=SLATE)
    clean(ax, (-0.2, len(Q) * w + 8.6), (y - 0.2, h + 0.45))
    title(ax, "Lomuto partition: a[lo:boundary] < pivot ≤ a[boundary:j], in one pass")
    return base.save(fig, "partition")


def partition_tree(sorting, values, strategy):
    """(depth, lo, hi, q) for every partition, by plain recursion on the real helpers."""
    from dsa.array import Array
    a = Array.from_values(values)
    out = []

    def go(lo, hi, depth):
        if lo >= hi:
            if lo == hi:
                out.append((depth, lo, hi, lo))
            return
        p = sorting._choose_pivot(a, lo, hi, strategy, random.Random(0))
        a[p], a[hi] = a[hi], a[p]
        q = sorting._partition(a, lo, hi)
        out.append((depth, lo, hi, q))
        go(lo, q - 1, depth + 1)
        go(q + 1, hi, depth + 1)

    go(0, len(values) - 1, 0)
    return out


def figure_pivot_shapes(sorting):
    n = 15
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.7),
                             gridspec_kw={"width_ratios": [1, 1]})
    for ax, strategy, name in [
        (axes[0], "median3", 'pivot="median3": halves, depth 4'),
        (axes[1], "first", 'pivot="first": one element per level, depth 15'),
    ]:
        parts = partition_tree(sorting, list(range(n)), strategy)
        depth = max(d for d, *_ in parts) + 1
        for d, lo, hi, q in parts:
            ax.add_patch(Rectangle((lo, -d), hi - lo + 1, 0.8, facecolor=FILL,
                                   edgecolor=SLATE, linewidth=0.9))
            ax.add_patch(Rectangle((q, -d), 1, 0.8, facecolor=AMBER, edgecolor=SLATE,
                                   linewidth=0.9))
        ax.set_xlim(-0.5, n + 0.5)
        ax.set_ylim(-depth - 0.3, 1.1)
        ax.set_title(name, fontsize=11, color=SLATE)
        ax.set_xlabel("index")
        ax.set_yticks([-d + 0.4 for d in range(depth)])
        ax.set_yticklabels([str(d) for d in range(depth)], fontsize=7.5)
        ax.set_ylabel("level of recursion")
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    fig.suptitle("Quicksort on the sorted list 0..14: the pivot decides the shape "
                 "(amber = pivot's final place)", fontsize=12, fontweight="bold",
                 color=SLATE)
    fig.tight_layout()
    return base.save(fig, "pivot-shapes")


# -- heap sort ----------------------------------------------------------------


def draw_heap(ax, values, x0, y0, width, highlight=(), done=()):
    n = len(values)
    levels = max(1, math.floor(math.log2(n)) + 1) if n else 1
    coords = {}
    for i in range(n):
        d = math.floor(math.log2(i + 1))
        k = i + 1 - (1 << d)
        slots = 1 << d
        coords[i] = (x0 + width * (k + 0.5) / slots, y0 - d * 1.05)
    for i in range(n):
        for c in (2 * i + 1, 2 * i + 2):
            if c < n:
                (x1, y1), (x2, y2) = coords[i], coords[c]
                ax.plot([x1, x2], [y1, y2], color=MUTED, linewidth=1.1, zorder=1)
    for i, (x, y) in coords.items():
        fill = HILITE if i in highlight else (DONE if i in done else FILL)
        ax.add_patch(Circle((x, y), 0.3, facecolor=fill, edgecolor=SLATE,
                            linewidth=1.2, zorder=2))
        ax.text(x, y, str(values[i]), ha="center", va="center", fontsize=10.5, zorder=3)
        ax.text(x + 0.36, y + 0.22, str(i), fontsize=7, color=MUTED, zorder=3)
    return levels


def figure_heap(sorting):
    frames = list(sorting.heap_sort_steps(H))
    heap = frames[1][0]                       # the state after build-heap
    fig, ax = plt.subplots(figsize=(10.8, 4.2))
    draw_heap(ax, heap, 0, 3.2, 6.0)
    row(ax, -0.35, heap, [FILL] * len(heap), w=0.62, h=0.5, fontsize=10, x0=6.9)
    x = lambda i: 6.9 + i * 0.62 + 0.31
    for parent, colour, rad in ((0, AMBER, -0.55), (1, GREEN, -0.5), (2, PURPLE, -0.45)):
        for child in (2 * parent + 1, 2 * parent + 2):
            arrow(ax, (x(parent), 0.2), (x(child), 0.2), colour=colour, rad=rad, lw=1.1)
    ax.text(6.9, 2.6, "the same eight values, as the Array holds them:\n"
            "children of i are at 2i + 1 and 2i + 2,\nthe parent of i is at (i − 1) // 2",
            fontsize=9.8, color=SLATE, va="center")
    ax.text(6.9, 1.35, f"build-heap turned {H}\ninto this max-heap: every parent ≥ its children",
            fontsize=9.3, color=MUTED, va="center")
    clean(ax, (-0.3, 12.2), (-0.75, 3.6))
    title(ax, "The array is the tree: no pointers, only index arithmetic")
    return base.save(fig, "heap")


def figure_heap_sort(sorting):
    frames = list(sorting.heap_sort_steps(H))
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    w, h = 0.62, 0.46
    n = len(H)
    shown = [(frames[0][0], n, "input"), (frames[1][0], n, "build-heap: O(n)")]
    for e, (state, _) in enumerate(frames[2:-1]):
        end = n - 1 - e
        shown.append((state, end, f"swap a[0] ↔ a[{end}], sift down in a[0:{end}]"))
    for r, (values, heap_size, note) in enumerate(shown):
        y = -r * 0.62
        fills = []
        for i in range(n):
            if r == 0:
                fills.append("white")
            elif i < heap_size:
                fills.append(HILITE if i == 0 else FILL)
            else:
                fills.append(DONE)
        row(ax, y, values, fills, w=w, h=h, fontsize=10, index=False)
        if r == 0:
            for idx in range(n):
                ax.text(idx * w + w / 2, h + 0.06, str(idx), ha="center", va="bottom",
                        fontsize=7, color=MUTED)
        ax.text(n * w + 0.3, y + h / 2, note, va="center", fontsize=9.3, color=SLATE,
                family="monospace")
    y = -len(shown) * 0.62 - 0.05
    for k, (fill, text) in enumerate([(FILL, "the heap"), (HILITE, "its root: the max"),
                                      (DONE, "sorted, final")]):
        box(ax, k * 3.0, y, "", fill=fill, w=0.4, h=0.3)
        ax.text(k * 3.0 + 0.55, y + 0.15, text, va="center", fontsize=9.5, color=SLATE)
    clean(ax, (-0.2, n * w + 7.4), (y - 0.2, h + 0.45))
    title(ax, "Heap sort: the max goes to the back, the heap shrinks by one")
    return base.save(fig, "heap-sort")


# -- stability ----------------------------------------------------------------


class Card:
    """A value compared by `key` only, so equal keys can be told apart by `tag`."""

    def __init__(self, key, tag):
        self.key, self.tag = key, tag

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key


def figure_stability(sorting):
    cards = [Card(k, t) for k, t in CARDS]
    runs = [("input", cards),
            ("merge_sort", sorting.merge_sort(cards)),
            ('quick_sort (median3)', sorting.quick_sort(cards)),
            ("heap_sort", sorting.heap_sort(cards))]
    order = {t: i for i, (_, t) in enumerate(CARDS)}
    colours = {1: "#DCE9F7", 2: "#FFE3B0", 3: "#D8EFD8"}
    fig, ax = plt.subplots(figsize=(10.0, 3.6))
    w, h = 0.82, 0.5
    for r, (name, result) in enumerate(runs):
        y = -r * 0.78
        ax.text(-0.25, y + h / 2, name, ha="right", va="center", fontsize=10,
                family="monospace", color=SLATE)
        broken = set()
        if r > 0:
            for i in range(len(result) - 1):
                x, z = result[i], result[i + 1]
                if x.key == z.key and order[x.tag] > order[z.tag]:
                    broken.update((i, i + 1))
        for i, c in enumerate(result):
            box(ax, i * w, y, f"{c.key}{c.tag}", fill=colours[c.key], w=w, h=h,
                fontsize=11, edge=RED if i in broken else SLATE,
                lw=2.4 if i in broken else 1.2)
        if r > 0:
            ok = not broken
            ax.text(len(CARDS) * w + 0.3, y + h / 2,
                    "stable: a before c, b before e, d before f" if ok else
                    "NOT stable: equal keys swapped (red)",
                    va="center", fontsize=9.8, color=GREEN if ok else RED)
    clean(ax, (-3.6, len(CARDS) * w + 6.0), (-len(runs) * 0.78 + 0.6, h + 0.25))
    title(ax, "Stability: equal keys (same number) keep their input order — or not")
    return base.save(fig, "stability")


# -- measured -----------------------------------------------------------------


class Counted:
    """A number that counts every comparison made on it, in a class-wide counter."""

    comparisons = 0
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.comparisons += 1
        return self.value < other.value

    def __le__(self, other):
        Counted.comparisons += 1
        return self.value <= other.value

    def __gt__(self, other):
        Counted.comparisons += 1
        return self.value > other.value

    def __ge__(self, other):
        Counted.comparisons += 1
        return self.value >= other.value


def comparisons(sort, values, *args):
    items = [Counted(v) for v in values]
    Counted.comparisons = 0
    result = sort(items, *args)
    assert [c.value for c in result] == sorted(values)
    return Counted.comparisons


def figure_measured(sorting):
    rng = random.Random(10)
    small = [2 ** k for k in range(4, 10)]            # 16 .. 512
    big = [2 ** k for k in range(4, 13)]              # 16 .. 4096
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.9))

    ax = axes[0]
    series = {}
    random_inputs = {n: rng.sample(range(10 * n), n) for n in big}
    for name, sort, sizes, colour, style in [
        ("bubble_sort", sorting.bubble_sort, small, RED, "o-"),
        ("selection_sort", sorting.selection_sort, small, "#E07B39", "o-"),
        ("insertion_sort", sorting.insertion_sort, small, AMBER, "o-"),
        ("heap_sort", sorting.heap_sort, big, PURPLE, "o-"),
        ("quick_sort (median3)", sorting.quick_sort, big, "#3A6EA5", "o-"),
        ("merge_sort", sorting.merge_sort, big, GREEN, "o-"),
        ("sorted() — Timsort", sorted, big, SLATE, "s--"),
    ]:
        counts = [comparisons(sort, random_inputs[n]) for n in sizes]
        series[name] = dict(zip(sizes, counts))
        ax.plot(sizes, counts, style, color=colour, label=name, linewidth=1.9,
                markersize=4.2)
    bound = [math.lgamma(n + 1) / math.log(2) for n in big]
    ax.plot(big, bound, ":", color=MUTED, linewidth=1.6,
            label="log₂(n!): no comparison sort can do fewer")
    ax.set_xlabel("n, random distinct values (log scale)")
    ax.set_ylabel("comparisons (log scale)")
    ax.set_title("random input", fontsize=11.5, color=SLATE)

    ax = axes[1]
    sizes = [2 ** k for k in range(4, 12)]            # 16 .. 2048
    for name, sort, args, colour, style in [
        ('quick_sort, pivot="first"', sorting.quick_sort, ("first",), RED, "o-"),
        ('quick_sort, pivot="random"', sorting.quick_sort, ("random",), AMBER, "o-"),
        ('quick_sort, pivot="median3"', sorting.quick_sort, ("median3",), "#3A6EA5", "o-"),
        ("heap_sort", sorting.heap_sort, (), PURPLE, "o-"),
        ("merge_sort", sorting.merge_sort, (), GREEN, "o-"),
        ("sorted() — Timsort", sorted, (), SLATE, "s--"),
    ]:
        counts = [comparisons(sort, list(range(n)), *args) for n in sizes]
        series["sorted input: " + name] = dict(zip(sizes, counts))
        ax.plot(sizes, counts, style, color=colour, label=name, linewidth=1.9,
                markersize=4.2)
    ax.set_xlabel("n, input ALREADY SORTED (log scale)")
    ax.set_ylabel("comparisons (log scale)")
    ax.set_title("sorted input", fontsize=11.5, color=SLATE)

    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.grid(True, alpha=0.25, linewidth=0.7)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
        ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle("Measured: comparisons made by the six sorts of dsa/sorting.py",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    for key, values in series.items():
        print(f"    {key:40s}", values)
    return base.save(fig, "measured")


def main():
    sorting = sorting_module()
    print(f"Generating figures into {base.OUT.relative_to(ROOT)}")
    figure_merge_step()
    figure_recursion_tree()
    if sorting is None:
        print("  (skipped the traced and measured figures: dsa/sorting.py is not "
              "implemented yet — try tools/with_solutions.py)")
        return
    for builder in (figure_divide, figure_partition, figure_pivot_shapes, figure_heap,
                    figure_heap_sort, figure_stability, figure_measured):
        builder(sorting)
    print("Done.")


if __name__ == "__main__":
    main()
