"""Generate the figures for Lecture 05 — Linked lists.

Run it from the repository root:

    python tools/figures_l05.py

Same conventions as `tools/figures.py`. The diagrams are drawn by hand with
matplotlib; the timing figure is real measurement with `viz.complexity.measure`
on reference implementations, so it exists before anyone has written
`dsa/linked_list.py`.
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

base.OUT = ROOT / "docs" / "lectures" / "05-linked-lists" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
GREY = "#E4E4E4"

NW, NH = 1.5, 0.7          # node width and height; the value part is 1.0 wide


def node(ax, x, y, value, fill=FILL, faded=False):
    """A node: [ value | • ]. Returns the (x, y) of its `next` dot."""
    edge = "#9AA5A7" if faded else SLATE
    text = "#9AA5A7" if faded else SLATE
    ax.add_patch(Rectangle((x, y), 1.0, NH, facecolor=fill, edgecolor=edge,
                           linewidth=1.3))
    ax.add_patch(Rectangle((x + 1.0, y), NW - 1.0, NH, facecolor=fill,
                           edgecolor=edge, linewidth=1.3))
    ax.text(x + 0.5, y + NH / 2, str(value), ha="center", va="center",
            fontsize=13, color=text)
    ax.plot([x + 1.25], [y + NH / 2], "o", color=text, markersize=4)
    return (x + 1.25, y + NH / 2)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.4, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=13,
                                 color=colour, linewidth=lw, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))


def label_pointer(ax, x, y, name, colour=AMBER, below=False):
    """A named reference (head, prev, node…) pointing at a node's left edge."""
    ty = y - 0.75 if below else y + NH + 0.75
    ax.text(x + 0.5, ty, name, ha="center", va="center", fontsize=11,
            color=colour, fontweight="bold")
    start = (x + 0.5, ty + (0.18 if below else -0.18))
    end = (x + 0.5, y - 0.02) if below else (x + 0.5, y + NH + 0.02)
    arrow(ax, start, end, colour=colour)


def none_box(ax, x, y):
    ax.text(x + 0.35, y + NH / 2, "None", ha="center", va="center", fontsize=11,
            color=MUTED, family="monospace")


def chain(ax, x0, y, values, gap=0.7, fills=None, end_none=True):
    """Draw a chain of nodes left to right; returns the x of each node."""
    xs = []
    for i, v in enumerate(values):
        x = x0 + i * (NW + gap)
        xs.append(x)
        dot = node(ax, x, y, v, fill=(fills[i] if fills else FILL))
        nxt = x + NW + gap
        if i < len(values) - 1:
            arrow(ax, dot, (nxt - 0.02, y + NH / 2))
        elif end_none:
            arrow(ax, dot, (nxt - 0.02, y + NH / 2), colour=MUTED)
            none_box(ax, nxt, y)
    return xs


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text):
    ax.set_title(text, fontsize=12.5, fontweight="bold", color=SLATE, pad=6)


# -- the structure ------------------------------------------------------------


def figure_chain():
    fig, ax = plt.subplots(figsize=(9.4, 3.0))
    xs = chain(ax, 0, 0, [3, 7, 1])
    label_pointer(ax, xs[0], 0, "head")
    ax.text(xs[1] + 0.5, -0.75, "value", ha="center", fontsize=10, color=MUTED)
    ax.text(xs[1] + 1.25, -0.75, "next", ha="center", fontsize=10, color=MUTED)
    ax.text(8.2, 1.55, "LinkedList:  head, _size = 3", fontsize=11, color=SLATE,
            family="monospace", ha="right")
    clean(ax, (-0.4, 8.6), (-1.1, 2.0))
    title(ax, "A linked list: nodes, each holding a value and a reference to the next")
    return base.save(fig, "chain")


def figure_memory():
    fig, ax = plt.subplots(figsize=(10.0, 4.4))
    # the array: one contiguous block
    ax.text(-0.2, 3.65, "Array", ha="right", va="center", fontsize=11, color=SLATE,
            fontweight="bold")
    for i, v in enumerate([3, 7, 1, 9]):
        ax.add_patch(Rectangle((i, 3.3), 1, 0.7, facecolor=FILL, edgecolor=SLATE,
                               linewidth=1.3))
        ax.text(i + 0.5, 3.65, str(v), ha="center", va="center", fontsize=12,
                color=SLATE)
        ax.text(i + 0.5, 3.05, f"{1000 + 8 * i}", ha="center", fontsize=8.5,
                color=MUTED, family="monospace")
    ax.text(4.3, 3.65, "one block, side by side: address of item i = base + 8i  ->  O(1)",
            va="center", fontsize=10, color=SLATE)
    # the nodes: scattered
    ax.text(-0.2, 1.1, "Linked\nlist", ha="right", va="center", fontsize=11,
            color=SLATE, fontweight="bold")
    spots = [(0.2, 1.4, 3, 5120), (6.2, 0.1, 7, 2088), (3.1, 0.3, 1, 9344),
             (8.6, 1.5, 9, 4416)]
    dots = []
    for x, y, v, addr in spots:
        dots.append((node(ax, x, y, v), x, y))
        ax.text(x + NW / 2, y - 0.25, f"{addr}", ha="center", fontsize=8.5,
                color=MUTED, family="monospace")
    for (dot, _, _), (_, x2, y2) in zip(dots, dots[1:]):
        arrow(ax, dot, (x2 - 0.02, y2 + NH / 2), rad=-0.25)
    last_dot = dots[-1][0]
    arrow(ax, last_dot, (last_dot[0] + 0.8, last_dot[1]), colour=MUTED)
    none_box(ax, last_dot[0] + 0.8, 1.5)
    ax.text(5.0, -0.55, "nodes anywhere in memory: to reach item i, follow i references  ->  O(n)",
            ha="center", fontsize=10, color=SLATE)
    clean(ax, (-1.6, 11.6), (-0.9, 4.3))
    title(ax, "Same four values, two layouts — and the whole difference in cost")
    return base.save(fig, "memory")


# -- changing the links -------------------------------------------------------


def figure_push_front():
    fig, ax = plt.subplots(figsize=(10.6, 4.4))
    # step 1
    ax.text(-1.0, 3.25, "1.", fontsize=12, color=SLATE, fontweight="bold")
    new_dot = node(ax, 0, 2.9, 5, fill=DONE)
    xs = chain(ax, 2.6, 2.9, [3, 7, 1])
    arrow(ax, new_dot, (2.58, 2.9 + NH / 2), colour=GREEN, lw=1.8)
    label_pointer(ax, xs[0], 2.9, "head")
    ax.text(0.75, 2.4, "new.next = self.head", ha="center", fontsize=10,
            color=GREEN, family="monospace")
    # step 2
    ax.text(-1.0, 0.35, "2.", fontsize=12, color=SLATE, fontweight="bold")
    new_dot = node(ax, 0, 0, 5, fill=DONE)
    chain(ax, 2.6, 0, [3, 7, 1])
    arrow(ax, new_dot, (2.58, NH / 2))
    label_pointer(ax, 0, 0, "head", colour=GREEN)
    ax.text(11.4, 0.35, "self.head = new\nself._size += 1", fontsize=10,
            color=GREEN, family="monospace", va="center")
    ax.text(11.4, 3.25, "no walking, no copying:\nO(1) whatever n is", fontsize=10,
            color=SLATE, va="center")
    clean(ax, (-1.3, 15.2), (-0.6, 4.6))
    title(ax, "push_front: link the new node in FIRST, then move head")
    return base.save(fig, "push-front")


def figure_insert_middle():
    fig, ax = plt.subplots(figsize=(10.4, 3.9))
    gap = 1.1
    xs = [i * (NW + gap) for i in range(4)]
    for x, v in zip(xs, [3, 7, 1, 9]):
        node(ax, x, 1.3, v)
    for i in (0, 2):
        arrow(ax, (xs[i] + 1.25, 1.3 + NH / 2), (xs[i + 1] - 0.02, 1.3 + NH / 2))
    end = xs[3] + NW + gap
    arrow(ax, (xs[3] + 1.25, 1.3 + NH / 2), (end - 0.02, 1.3 + NH / 2), colour=MUTED)
    none_box(ax, end, 1.3)
    # the old link 7 -> 1, replaced: faded and dashed
    arrow(ax, (xs[1] + 1.25, 1.3 + NH / 2), (xs[2] - 0.02, 1.3 + NH / 2),
          colour="#B8C0C2", ls="--")
    label_pointer(ax, xs[0], 1.3, "head")
    label_pointer(ax, xs[1], 1.3, "prev", colour=RED)
    nx = xs[1] + 1.25
    new_dot = node(ax, nx, -0.4, 4, fill=DONE)
    arrow(ax, (xs[1] + 1.25, 1.3 + NH / 2 - 0.05), (nx + 0.5, -0.4 + NH + 0.02),
          colour=GREEN, lw=1.8, rad=0.2)
    arrow(ax, new_dot, (xs[2] + 0.3, 1.28), colour=GREEN, lw=1.8, rad=0.25)
    ax.text(10.2, 0.6, "insert_at(2, 4):\n1. walk to prev (index 1)  O(n)\n"
            "2. new.next = prev.next\n3. prev.next = new         O(1)",
            fontsize=10, color=SLATE, family="monospace", va="center")
    clean(ax, (-0.4, 15.6), (-0.9, 2.9))
    title(ax, "Insert in the middle: the walk costs O(n); the splice itself is O(1)")
    return base.save(fig, "insert-middle")


def figure_remove():
    fig, ax = plt.subplots(figsize=(10.0, 3.2))
    fills = [FILL, FILL, GREY, FILL]
    xs = []
    gap = 1.0
    for i, v in enumerate([3, 7, 1, 9]):
        x = i * (NW + gap)
        xs.append(x)
        node(ax, x, 0.5, v, fill=fills[i], faded=(i == 2))
    arrow(ax, (xs[0] + 1.25, 0.5 + NH / 2), (xs[1] - 0.02, 0.5 + NH / 2))
    arrow(ax, (xs[2] + 1.25, 0.5 + NH / 2), (xs[3] - 0.02, 0.5 + NH / 2),
          colour="#B8C0C2", ls="--")
    arrow(ax, (xs[1] + 1.25, 0.5 + NH / 2), (xs[2] - 0.02, 0.5 + NH / 2),
          colour="#B8C0C2", ls="--")
    arrow(ax, (xs[1] + 1.25, 0.5 + NH), (xs[3] + 0.4, 0.5 + NH + 0.02),
          colour=GREEN, lw=1.9, rad=-0.45)
    end = xs[3] + NW + 0.6
    arrow(ax, (xs[3] + 1.25, 0.5 + NH / 2), (end - 0.02, 0.5 + NH / 2), colour=MUTED)
    none_box(ax, end, 0.5)
    label_pointer(ax, xs[0], 0.5, "head", below=True)
    label_pointer(ax, xs[1], 0.5, "prev", colour=RED, below=True)
    ax.text(xs[2] + 0.75, -0.25, "unreachable:\ngarbage-collected", ha="center",
            fontsize=9, color=MUTED, va="top")
    ax.text(xs[1] + 2.0, 2.35, "prev.next = prev.next.next", ha="center",
            fontsize=10, color=GREEN, family="monospace")
    clean(ax, (-0.4, 11.4), (-1.2, 2.7))
    title(ax, "remove(1): make the previous node skip over it")
    return base.save(fig, "remove")


def figure_reverse():
    fig, ax = plt.subplots(figsize=(10.4, 3.6))
    # reversed part: 7 -> 3 -> None   (prev = 7), rest: 1 -> 9 -> None (node = 1)
    y = 0.8
    ax.text(0.1, y + NH / 2, "None", ha="center", va="center", fontsize=11,
            color=MUTED, family="monospace")
    n3 = 0.9
    n7 = 3.2
    node(ax, n3, y, 3, fill=DONE)
    node(ax, n7, y, 7, fill=DONE)
    arrow(ax, (n3 + 1.25, y + NH / 2 - 0.1), (0.45, y + NH / 2 - 0.1), colour=SLATE,
          rad=0.5)
    arrow(ax, (n7 + 1.25, y + NH / 2 - 0.1), (n3 + NW + 0.02, y + NH / 2 - 0.1),
          colour=SLATE, rad=0.5)
    n1 = 6.2
    n9 = 8.4
    node(ax, n1, y, 1)
    node(ax, n9, y, 9)
    arrow(ax, (n1 + 1.25, y + NH / 2), (n9 - 0.02, y + NH / 2))
    arrow(ax, (n9 + 1.25, y + NH / 2), (n9 + 2.1, y + NH / 2), colour=MUTED)
    none_box(ax, n9 + 2.1, y)
    label_pointer(ax, n7, y, "prev", colour=GREEN)
    label_pointer(ax, n1, y, "node", colour=AMBER)
    ax.text(2.4, -0.35, "reversed so far", ha="center", fontsize=10, color=GREEN)
    ax.text(8.2, -0.35, "still to do", ha="center", fontsize=10, color=AMBER)
    ax.plot([5.3, 5.3], [0.2, 2.2], color=MUTED, linestyle=":", linewidth=1.2)
    clean(ax, (-0.4, 11.4), (-0.8, 2.6))
    title(ax, "Reversing, halfway: one node crosses the line per step")
    return base.save(fig, "reverse")


# -- measured -----------------------------------------------------------------


def figure_measured():
    from dsa.array import Array
    from viz.complexity import measure

    class Node:
        __slots__ = ("value", "next")

        def __init__(self, value, next=None):
            self.value, self.next = value, next

    def make_list(n):
        head = None
        for v in range(n):
            head = Node(v, head)
        return head

    def make_array(n):
        arr = Array(n + 1)
        for i in range(n):
            arr[i] = i
        return arr

    def array_insert_front(pair):
        arr, n = pair
        for i in range(n, 0, -1):
            arr[i] = arr[i - 1]
        arr[0] = -1

    def list_push_front(pair):
        head, _ = pair
        for _ in range(1000):             # averaged below: one call is too fast to time
            Node(-1, head)

    reads = 1000

    def array_middle(pair):
        arr, n = pair
        mid = n // 2
        for _ in range(reads):
            arr[mid]

    def list_middle(pair):
        node, n = pair
        for _ in range(n // 2):
            node = node.next
        return node.value

    sizes = [1000, 2000, 4000, 8000, 16000, 32000]
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    panels = [
        ("insert at the front", [
            ("Array: shift everything", array_insert_front,
             lambda n: (make_array(n), n), RED, 1),
            ("linked list: push_front  (average of 1,000)", list_push_front,
             lambda n: (make_list(n), n), GREEN, 1000),
        ]),
        ("read the middle element", [
            ("Array: a[n // 2]  (average of 1,000 reads)", array_middle,
             lambda n: (make_array(n), n), GREEN, reads),
            ("linked list: walk n / 2 links", list_middle,
             lambda n: (make_list(n), n), RED, 1),
        ]),
    ]
    for ax, (name, series) in zip(axes, panels):
        for label, func, make, colour, per in series:
            measured, seconds = measure(func, sizes, make, repeat=7)
            ax.plot(measured, [s * 1e6 / per for s in seconds], "o-", color=colour,
                    label=label, linewidth=2.1, markersize=5)
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_xlabel("n (log scale)")
        ax.set_ylabel("microseconds (log scale)")
        ax.set_title(name, fontsize=11.5, color=SLATE)
        ax.grid(True, alpha=0.25, linewidth=0.7)
        ax.legend(frameon=False, fontsize=9, loc="upper left")
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    fig.suptitle("Measured: each structure is O(1) exactly where the other is O(n)",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "measured")


FIGURES = [figure_chain, figure_memory, figure_push_front, figure_insert_middle,
           figure_remove, figure_reverse, figure_measured]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
