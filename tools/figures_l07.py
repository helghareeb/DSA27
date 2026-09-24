"""Generate the figures for Lecture 07 — Queues.

Run it from the repository root:

    python tools/figures_l07.py                       # timing uses YOUR dsa/queue.py
    python tools/with_solutions.py tools/figures_l07.py   # timing uses solutions/

Same conventions as `tools/figures.py`. The timing figure is real measurement
with `viz.complexity.measure` of **your** `dsa/queue.py`, so it needs a working
implementation (the lecture's copy was made from the instructor's reference
solution); without one, every other figure is still drawn.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import figures as base  # palette, rcParams, save()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Wedge

base.OUT = ROOT / "docs" / "lectures" / "07-queues" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
DEAD = "#EEEEEE"


def box(ax, x, y, text, fill=FILL, w=1.0, h=0.6, fontsize=12, edge=SLATE, colour=SLATE):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, linewidth=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=colour)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.5):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def pointer(ax, x, y, label, colour=AMBER, below=False):
    """A labelled arrow pointing at a slot whose centre is x, from above or below."""
    if below:                                 # clear of the slot numbers
        ax.annotate(label, xy=(x, y - 0.38), xytext=(x, y - 0.9), ha="center", va="top",
                    color=colour, fontsize=10.5, fontweight="bold",
                    arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.4))
    else:
        ax.annotate(label, xy=(x, y), xytext=(x, y + 0.55), ha="center", va="bottom",
                    color=colour, fontsize=10.5, fontweight="bold",
                    arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.4))


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text):
    ax.set_title(text, fontsize=12.5, fontweight="bold", color=SLATE, pad=6)


def block(ax, x0, y, values, head=None, fills=None, index=True, h=0.6):
    """A row of slots. values: '' for an empty slot. Returns nothing."""
    for i, v in enumerate(values):
        fill = fills[i] if fills else (FILL if v else "white")
        box(ax, x0 + i, y, v, fill=fill, h=h)
        if index:
            ax.text(x0 + i + 0.5, y - 0.12, str(i), ha="center", va="top", fontsize=8.5,
                    color=MUTED)


# -- the ADT ------------------------------------------------------------------


def figure_fifo():
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    states = [
        ("enqueue(A)", ["A"], None),
        ("enqueue(B)", ["A", "B"], None),
        ("enqueue(C)", ["A", "B", "C"], None),
        ("dequeue() → A", ["B", "C"], "A"),
        ("enqueue(D)", ["B", "C", "D"], None),
        ("dequeue() → B", ["C", "D"], "B"),
    ]
    for r, (op, items, out) in enumerate(states):
        y = -r * 0.85
        ax.text(-0.3, y + 0.3, op, ha="right", va="center", fontsize=10.5,
                family="monospace", color=SLATE)
        for i, v in enumerate(items):
            fill = HILITE if i == 0 else (DONE if i == len(items) - 1 else FILL)
            box(ax, i, y, v, fill=fill)
        if out:
            ax.text(-3.55, y + 0.3, out, ha="center", va="center", fontsize=12,
                    color=AMBER, fontweight="bold")
    ax.text(0.5, 0.95, "front", ha="center", fontsize=10.5, color=AMBER,
            fontweight="bold")
    ax.text(4.6, -1.3, "enqueue at\nthe BACK", ha="left", va="center", fontsize=10.5,
            color=GREEN, fontweight="bold")
    ax.text(4.6, -3.2, "dequeue at\nthe FRONT", ha="left", va="center", fontsize=10.5,
            color=AMBER, fontweight="bold")
    ax.text(-3.55, 0.95, "out", ha="center", fontsize=10.5, color=AMBER,
            fontweight="bold")
    clean(ax, (-4.2, 6.6), (-4.6, 1.3))
    title(ax, "A queue: in at the back, out at the front — first in, first out (FIFO)")
    return base.save(fig, "fifo")


# -- the obvious design, and the fix ---------------------------------------------


def figure_slow_dequeue():
    fig, ax = plt.subplots(figsize=(9.6, 3.3))
    before = ["A", "B", "C", "D", "E", "", "", ""]
    after = ["B", "C", "D", "E", "", "", "", ""]
    ax.text(-0.3, 1.9, "before", ha="right", va="center", fontsize=10.5, color=SLATE)
    block(ax, 0, 1.6, before, fills=[HILITE] + [FILL] * 4 + ["white"] * 3)
    ax.text(-0.3, 0.3, "after", ha="right", va="center", fontsize=10.5, color=SLATE)
    block(ax, 0, 0.0, after)
    for i in range(1, 5):
        arrow(ax, (i + 0.5, 1.48), (i - 0.5, 0.72), colour=RED, lw=1.4)
    ax.annotate("returns A", xy=(0.5, 2.2), xytext=(0.5, 2.8), ha="center",
                color=AMBER, fontsize=10.5, fontweight="bold",
                arrowprops=dict(arrowstyle="<|-", color=AMBER, lw=1.4))
    ax.text(8.4, 1.0, "pop(0): every remaining\nelement moves one slot left\n"
            "→ n − 1 moves: O(n)", va="center", fontsize=10.5, color=RED)
    clean(ax, (-1.4, 12.4), (-0.5, 3.3))
    title(ax, "SlowQueue: enqueue is append (O(1)); dequeue is pop(0) — O(n)")
    return base.save(fig, "slow-dequeue")


def figure_crawl():
    fig, ax = plt.subplots(figsize=(9.8, 4.4))
    rows = [
        ("after enqueue A B C D", ["A", "B", "C", "D", "", "", "", ""], 0, 4),
        ("after 2 × dequeue", ["", "", "C", "D", "", "", "", ""], 2, 4),
        ("after enqueue E F G H", ["", "", "C", "D", "E", "F", "G", "H"], 2, 8),
    ]
    for r, (label, values, head, tail) in enumerate(rows):
        y = -r * 2.3
        fills = [DEAD if (i < head) else (FILL if v else "white")
                 for i, v in enumerate(values)]
        ax.text(-0.3, y + 0.3, label, ha="right", va="center", fontsize=10,
                color=SLATE, family="monospace")
        block(ax, 0, y, values, fills=fills)
        pointer(ax, head + 0.5, y + 0.6, "head")
        if tail < 8:
            pointer(ax, tail + 0.5, y, "tail", colour=GREEN, below=True)
        else:
            ax.text(8.15, y + 0.3, "tail = 8: no room at the end,\n"
                    "though slots 0 and 1 are free", va="center", fontsize=10,
                    color=RED)
    clean(ax, (-5.6, 12.6), (-5.0, 1.4))
    title(ax, "Idea 1 — don't shift, move a head index: O(1), but the queue crawls "
          "to the right")
    return base.save(fig, "crawl")


def ring(ax, cx, cy, values, head, size, r_out=1.6, r_in=0.85, label_tail=True):
    """Draw a ring buffer as a circle of slots, slot 0 at the top, clockwise."""
    n = len(values)
    step = 360 / n
    for i, v in enumerate(values):
        # slot i spans clockwise from angle (90 - i*step) to (90 - (i+1)*step)
        start = 90 - (i + 1) * step
        end = 90 - i * step
        in_use = (i - head) % n < size
        fill = FILL if in_use else "white"
        if in_use and i == head:
            fill = HILITE
        ax.add_patch(Wedge((cx, cy), r_out, start, end, width=r_out - r_in,
                           facecolor=fill, edgecolor=SLATE, linewidth=1.3))
        mid = math.radians((start + end) / 2)
        rm = (r_out + r_in) / 2
        ax.text(cx + rm * math.cos(mid), cy + rm * math.sin(mid), v, ha="center",
                va="center", fontsize=12, color=SLATE)
        ro = r_out + 0.2
        ax.text(cx + ro * math.cos(mid), cy + ro * math.sin(mid), str(i), ha="center",
                va="center", fontsize=8.5, color=MUTED)

    def mark(slot, colour):
        mid = math.radians(90 - (slot + 0.5) * step)
        a = (cx + (r_in - 0.05) * math.cos(mid), cy + (r_in - 0.05) * math.sin(mid))
        b = (cx + 0.25 * math.cos(mid), cy + 0.25 * math.sin(mid))
        arrow(ax, b, a, colour=colour, lw=1.6)

    tail = (head + size) % n
    mark(head, AMBER if size else MUTED)
    if tail == head:                          # label on the side away from the arrow
        mid = math.radians(90 - (head + 0.5) * step)
        ax.text(cx - 0.3 * math.cos(mid), cy - 0.3 * math.sin(mid), "head\n= tail",
                ha="center", va="center", fontsize=8.5,
                color=SLATE, fontweight="bold")
    elif label_tail:
        mark(tail, GREEN)


def figure_ring():
    fig, ax = plt.subplots(figsize=(10.4, 4.6))
    values = ["F", "G", "", "", "", "C", "D", "E"]
    head, size = 5, 5
    ring(ax, 1.9, 1.9, values, head, size)
    ax.text(0.0, 4.05, "head (amber) = 5    tail (green) = 2", fontsize=10,
            color=SLATE)
    # the same block, drawn flat
    fills = [FILL, FILL, "white", "white", "white", HILITE, FILL, FILL]
    block(ax, 5.0, 2.3, values, fills=fills)
    pointer(ax, 5.0 + head + 0.5, 2.9, "head")
    pointer(ax, 5.0 + 2 + 0.5, 2.3, "tail", colour=GREEN, below=True)
    ax.text(9.0, 0.75, "after slot 7 comes slot 0:   i = (i + 1) % capacity",
            ha="center", fontsize=10, color=MUTED)
    ax.text(5.0, -0.25, "queue order, front to back:  C  D  E  F  G\n"
            "tail = (head + size) % capacity = (5 + 5) % 8 = 2",
            fontsize=10.5, color=SLATE, family="monospace", va="center")
    clean(ax, (-0.2, 13.4), (-0.9, 4.3))
    title(ax, "Idea 2 — wrap around: the same fixed Array, read as a ring")
    return base.save(fig, "ring")


def figure_full_empty():
    fig, ax = plt.subplots(figsize=(9.6, 4.0))
    ring(ax, 1.9, 1.8, ["", "", "", ""], 0, 0)
    ax.text(1.9, -0.25, "empty: head = 0, size = 0", ha="center", fontsize=10.5,
            color=SLATE, family="monospace")
    ring(ax, 7.0, 1.8, ["E", "F", "C", "D"], 2, 4)
    ax.text(7.0, -0.25, "full: head = 2, size = 4", ha="center", fontsize=10.5,
            color=SLATE, family="monospace")
    ax.text(4.45, 1.8, "head = tail\nin both", ha="center", va="center", fontsize=11,
            color=RED, fontweight="bold")
    ax.text(10.0, 1.8, "head and tail alone\ncannot tell them apart.\n\n"
            "Fix: keep size\n(dsa/queue.py does),\nor always leave\none slot empty.",
            va="center", fontsize=10, color=SLATE)
    clean(ax, (-0.2, 13.2), (-0.7, 3.9))
    title(ax, "Full or empty? The one real trap in a ring buffer")
    return base.save(fig, "full-empty")


def figure_grow():
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    ax.text(-0.3, 4.2, "full, capacity 4\nhead = 2", ha="right", va="center",
            fontsize=10, color=SLATE)
    block(ax, 0, 3.9, ["E", "F", "C", "D"], fills=[FILL, FILL, HILITE, FILL])
    ax.text(4.3, 4.2, "queue order: C D E F", va="center", fontsize=10.5,
            color=SLATE, family="monospace")

    ax.text(-0.3, 2.2, "naive copy\nhead still 2", ha="right", va="center",
            fontsize=10, color=RED)
    block(ax, 0, 1.9, ["E", "F", "C", "D", "", "", "", ""],
          fills=[FILL, FILL, HILITE, FILL] + ["white"] * 4)
    ax.text(8.3, 2.2, "reads C D _ _   ✗", va="center", fontsize=11, color=RED,
            family="monospace", fontweight="bold")

    ax.text(-0.3, 0.2, "unrolled copy\nhead = 0", ha="right", va="center",
            fontsize=10, color=GREEN)
    block(ax, 0, -0.1, ["C", "D", "E", "F", "", "", "", ""],
          fills=[HILITE, FILL, FILL, FILL] + ["white"] * 4)
    ax.text(8.3, 0.2, "reads C D E F   ✓", va="center", fontsize=11, color=GREEN,
            family="monospace", fontweight="bold")
    ax.text(0.0, -1.1, "new[i] = old[(head + i) % old_capacity]   for i in "
            "range(size);   then head = 0", fontsize=10, color=SLATE,
            family="monospace")
    clean(ax, (-2.6, 12.6), (-1.5, 5.0))
    title(ax, "Growing a ring: copy in QUEUE order, not slot order")
    return base.save(fig, "grow")


def figure_linked():
    fig, ax = plt.subplots(figsize=(10.0, 2.9))
    xs = [0, 1.9, 3.8, 5.7]
    for x, v in zip(xs, ["A", "B", "C", "D"]):
        fill = HILITE if v == "A" else (DONE if v == "D" else FILL)
        box(ax, x, 0.25, v, fill=fill, w=0.9, h=0.6)
        box(ax, x + 0.9, 0.25, "•", fill=fill, w=0.45, h=0.6, fontsize=10)
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + 1.12, 0.55), (b - 0.02, 0.55))
    arrow(ax, (xs[-1] + 1.12, 0.55), (xs[-1] + 1.75, 0.55), colour=MUTED)
    ax.text(xs[-1] + 2.1, 0.55, "None", va="center", fontsize=10, color=MUTED,
            family="monospace")
    ax.annotate("head = front\ndequeue: pop_front, O(1)", xy=(0.45, 0.9),
                xytext=(0.45, 1.75), ha="center", color=AMBER, fontsize=10,
                fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.5))
    ax.annotate("tail = back\nenqueue: link after tail, O(1)", xy=(6.15, 0.9),
                xytext=(6.15, 1.75), ha="center", color=GREEN, fontsize=10,
                fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.5))
    clean(ax, (-1.0, 9.6), (0.0, 2.6))
    title(ax, "A linked queue: front at the head, back at the tail — never the other "
          "way round")
    return base.save(fig, "linked")


# -- measured -----------------------------------------------------------------


def linked_queue():
    """A linked queue, for comparison only: dsa/ has no linked queue exercise."""

    class Node:
        __slots__ = ("value", "next")

        def __init__(self, value):
            self.value, self.next = value, None

    class LinkedQueue:                        # head = front, tail = back
        def __init__(self, capacity=None):
            self.head = self.tail = None

        def enqueue(self, v):
            node = Node(v)
            if self.tail is None:
                self.head = self.tail = node
            else:
                self.tail.next = node
                self.tail = node

        def dequeue(self):
            v = self.head.value
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return v

    return LinkedQueue


def figure_measured():
    from dsa.queue import CircularQueue, SlowQueue
    from viz.complexity import measure

    try:
        probe = CircularQueue(2)
        probe.enqueue(1)
        probe.dequeue()
        SlowQueue([1]).dequeue()
    except NotImplementedError:
        print("  (skipped measured.png: dsa/queue.py is not implemented yet)")
        return None

    def make_ring(capacity):                # sized up front: growing is the challenge
        return CircularQueue(capacity)

    def make_slow(capacity):
        return SlowQueue()

    LinkedQueue = linked_queue()

    def total(cls):
        def work(n):
            q = cls(n)
            for i in range(n):
                q.enqueue(i)
            for _ in range(n):
                q.dequeue()
        return work

    def filled(cls, n):
        q = cls(n)
        for i in range(n):
            q.enqueue(i)
        return q

    def one_dequeue(per):
        def work(q):
            for i in range(per):            # size stays n: out one, in one
                q.enqueue(q.dequeue())
        return work

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6))

    ax = axes[0]
    sizes = [250, 500, 1000, 2000, 4000]
    for label, cls, colour in [
        ("SlowQueue (pop(0) shifts)", make_slow, RED),
        ("CircularQueue (ring buffer)", make_ring, GREEN),
        ("linked queue (head + tail)", LinkedQueue, AMBER),
    ]:
        measured, seconds = measure(total(cls), sizes, lambda n: n, repeat=3)
        ax.plot(measured, [s * 1e3 for s in seconds], "o-", color=colour, label=label,
                linewidth=2.1, markersize=5)
    ax.set_xlabel("n enqueues, then n dequeues (log scale)")
    ax.set_ylabel("milliseconds (log scale)")
    ax.set_title("the whole workload", fontsize=11.5, color=SLATE)

    ax = axes[1]
    sizes = [1000, 2000, 4000, 8000, 16000]
    for label, cls, colour, per in [
        ("SlowQueue  (average of 50)", make_slow, RED, 50),
        ("CircularQueue  (average of 2,000)", make_ring, GREEN, 2000),
        ("linked queue  (average of 2,000)", LinkedQueue, AMBER, 2000),
    ]:
        measured, seconds = measure(one_dequeue(per), sizes,
                                    lambda n, cls=cls: filled(cls, n), repeat=5)
        ax.plot(measured, [s * 1e6 / per for s in seconds], "o-", color=colour,
                label=label, linewidth=2.1, markersize=5)
    ax.set_xlabel("n items already in the queue (log scale)")
    ax.set_ylabel("microseconds per dequeue + enqueue (log scale)")
    ax.set_title("one dequeue, on a queue of n", fontsize=11.5, color=SLATE)

    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.grid(True, alpha=0.25, linewidth=0.7)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    axes[0].legend(frameon=False, fontsize=9, loc="upper left")
    axes[1].legend(frameon=False, fontsize=9, loc="center left")
    fig.suptitle("Measured: pop(0) makes each dequeue O(n); the ring keeps it O(1)",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "measured")


FIGURES = [figure_fifo, figure_slow_dequeue, figure_crawl, figure_ring,
           figure_full_empty, figure_grow, figure_linked, figure_measured]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
