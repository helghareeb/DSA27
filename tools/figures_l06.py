"""Generate the figures for Lecture 06 — Stacks.

Run it from the repository root:

    python tools/figures_l06.py

Same conventions as `tools/figures.py`. The timing figure is real measurement
with `viz.complexity.measure` on reference implementations, so it exists before
anyone has written `dsa/stack.py`.
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

base.OUT = ROOT / "docs" / "lectures" / "06-stacks" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"


def box(ax, x, y, text, fill=FILL, w=1.0, h=0.55, fontsize=12, edge=SLATE):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, linewidth=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=SLATE)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.5):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text):
    ax.set_title(text, fontsize=12.5, fontweight="bold", color=SLATE, pad=6)


def column(ax, x, items, top_fill=HILITE, label=None, w=1.0, h=0.55):
    """A vertical stack, bottom item first. Returns the y just above the top."""
    for i, item in enumerate(items):
        fill = top_fill if i == len(items) - 1 else FILL
        box(ax, x, i * h, item, fill=fill, w=w, h=h)
    ax.plot([x - 0.08, x - 0.08, x + w + 0.08, x + w + 0.08],
            [len(items) * h + 0.25, -0.05, -0.05, len(items) * h + 0.25],
            color=MUTED, linewidth=1.4)
    if label:
        ax.text(x + w / 2, -0.4, label, ha="center", va="top", fontsize=10,
                color=SLATE, family="monospace")
    return len(items) * h


# -- the ADT ------------------------------------------------------------------


def figure_lifo():
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    states = [
        (["A"], "push(A)"),
        (["A", "B"], "push(B)"),
        (["A", "B", "C"], "push(C)"),
        (["A", "B"], "pop() → C"),
        (["A", "B"], "peek() → B"),
        (["A"], "pop() → B"),
    ]
    for i, (items, op) in enumerate(states):
        column(ax, i * 1.75, items, label=op)
    ax.text(10.5, 1.2, "the last in\nis the first out\n(LIFO)", ha="center",
            va="center", fontsize=11, color=AMBER, fontweight="bold")
    clean(ax, (-0.4, 11.6), (-1.0, 2.2))
    title(ax, "A stack: push, pop and peek all act on the top — and only the top")
    return base.save(fig, "lifo")


def figure_two_ways():
    fig, ax = plt.subplots(figsize=(10.2, 4.0))
    # array: top at the end
    ax.text(-0.2, 2.9, "on a\nDynamicArray", ha="right", va="center", fontsize=11,
            color=SLATE, fontweight="bold")
    vals = ["A", "B", "C", "", ""]
    for i, v in enumerate(vals):
        fill = HILITE if i == 2 else (FILL if v else "white")
        box(ax, i, 2.6, v, fill=fill, h=0.6)
    ax.annotate("top", xy=(2.5, 3.25), xytext=(2.5, 3.85), ha="center", color=AMBER,
                fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.5))
    ax.text(5.4, 2.9, "top = the END: append and pop() move nothing\n"
            "push, pop, peek: O(1)  (push amortised)", va="center", fontsize=10,
            color=SLATE)
    # linked list: top at the head
    ax.text(-0.2, 0.55, "on a\nlinked list", ha="right", va="center", fontsize=11,
            color=SLATE, fontweight="bold")
    xs = [0, 1.9, 3.8]
    for x, v, fill in zip(xs, ["C", "B", "A"], [HILITE, FILL, FILL]):
        box(ax, x, 0.25, v, fill=fill, w=0.9, h=0.6)
        box(ax, x + 0.9, 0.25, "•", fill=fill, w=0.45, h=0.6, fontsize=10)
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + 1.12, 0.55), (b - 0.02, 0.55))
    arrow(ax, (xs[-1] + 1.12, 0.55), (xs[-1] + 1.75, 0.55), colour=MUTED)
    ax.text(xs[-1] + 2.1, 0.55, "None", va="center", fontsize=10, color=MUTED,
            family="monospace")
    ax.annotate("top = head", xy=(0.45, 0.9), xytext=(0.45, 1.6), ha="center",
                color=AMBER, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.5))
    ax.text(7.3, 0.55, "top = the HEAD: push_front and pop_front\n"
            "push, pop, peek: O(1)  (worst case)", va="center", fontsize=10,
            color=SLATE)
    clean(ax, (-2.2, 12.6), (-0.2, 4.3))
    title(ax, "One ADT, two honest implementations — the top goes where the O(1) end is")
    return base.save(fig, "two-ways")


def figure_brackets():
    fig, ax = plt.subplots(figsize=(10.6, 3.9))
    text = "( [ { } ] )"
    tokens = text.split()
    stack, x = [], 0.0
    for i, ch in enumerate(tokens):
        if ch in "([{":
            stack.append(ch)
            op = f"push {ch}"
        else:
            top = stack.pop()
            op = f"pop {top} ✓"
        column(ax, x, stack if stack else [], label=None)
        ax.text(x + 0.5, -0.4, ch, ha="center", va="top", fontsize=15, color=SLATE,
                fontweight="bold", family="monospace")
        ax.text(x + 0.5, -1.05, op.replace(" ✓", ""), ha="center", va="top",
                fontsize=9, color=GREEN if "pop" in op else MUTED)
        x += 1.7
    ax.text(x + 0.2, 0.3, "empty at the end\n→ balanced", fontsize=11, color=GREEN,
            fontweight="bold", va="center")
    clean(ax, (-0.4, x + 2.6), (-1.6, 2.2))
    title(ax, "is_balanced(\"([{}])\"): push each opener; each closer must match the top")
    return base.save(fig, "brackets")


# -- measured -----------------------------------------------------------------


def figure_measured():
    """Push n then pop n, three ways."""
    from dsa.array import Array
    from viz.complexity import measure

    class ArrayStack:                         # top at the END — the right way
        def __init__(self):
            self.block, self.size = Array(1), 0

        def _grow(self):
            bigger = Array(2 * len(self.block))
            for i in range(self.size):
                bigger[i] = self.block[i]
            self.block = bigger

        def push(self, v):
            if self.size == len(self.block):
                self._grow()
            self.block[self.size] = v
            self.size += 1

        def pop(self):
            self.size -= 1
            v = self.block[self.size]
            self.block[self.size] = None
            return v

    class FrontArrayStack(ArrayStack):        # top at index 0 — the wrong way
        def push(self, v):
            if self.size == len(self.block):
                self._grow()
            for i in range(self.size, 0, -1):
                self.block[i] = self.block[i - 1]
            self.block[0] = v
            self.size += 1

        def pop(self):
            v = self.block[0]
            for i in range(self.size - 1):
                self.block[i] = self.block[i + 1]
            self.size -= 1
            self.block[self.size] = None
            return v

    class Node:
        __slots__ = ("value", "next")

        def __init__(self, value, next=None):
            self.value, self.next = value, next

    class LinkedStack:                        # top at the head
        def __init__(self):
            self.head = None

        def push(self, v):
            self.head = Node(v, self.head)

        def pop(self):
            v = self.head.value
            self.head = self.head.next
            return v

    def run(cls):
        def work(n):
            s = cls()
            for i in range(n):
                s.push(i)
            for _ in range(n):
                s.pop()
        return work

    sizes = [500, 1000, 2000, 4000, 8000]
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    for label, cls, colour in [
        ("array, top at index 0  (every push/pop shifts)", FrontArrayStack, RED),
        ("array, top at the end", ArrayStack, GREEN),
        ("linked list, top at the head", LinkedStack, AMBER),
    ]:
        measured, seconds = measure(run(cls), sizes, lambda n: n, repeat=3)
        ax.plot(measured, [s * 1e3 for s in seconds], "o-", color=colour, label=label,
                linewidth=2.1, markersize=5)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("n pushes, then n pops (log scale)")
    ax.set_ylabel("milliseconds (log scale)")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("Same ADT, three designs: where you put the top decides O(n) or O(n²)",
                 fontsize=12, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "measured")


FIGURES = [figure_lifo, figure_two_ways, figure_brackets, figure_measured]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
