"""Generate the figures for Lecture 03 — Recursion.

Run it from the repository root:

    python tools/figures_l03.py

Same conventions as `tools/figures.py`: PNG, the course palette, nothing
borrowed. The two charts are **counted**, not timed — the number of calls and
the number of multiplications are exact, so these figures are identical on
every machine.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import figures as base  # palette, rcParams, save() and save_dot()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "03-recursion" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"


def _digraph(rankdir="TB"):
    from graphviz import Digraph

    dot = Digraph(graph_attr={"rankdir": rankdir, "nodesep": "0.18", "ranksep": "0.38"})
    dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica",
             fontsize="11", color=MUTED, fillcolor=FILL, penwidth="1.0",
             margin="0.08,0.04")
    dot.attr("edge", color=MUTED, arrowsize="0.6")
    return dot


# -- the call stack -----------------------------------------------------------


def figure_call_stack():
    """factorial(4): the stack at each moment, left to right in time."""
    frames = ["factorial(4)", "factorial(3)", "factorial(2)", "factorial(1)", "factorial(0)"]
    # heights of the stack over time: wind up to 5, then unwind
    heights = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    # what the TOP frame is doing at each moment
    doing = ["calls\nfactorial(3)", "calls\nfactorial(2)", "calls\nfactorial(1)",
             "calls\nfactorial(0)", "base case:\nreturns 1", "1 × 1 = 1\nreturns 1",
             "2 × 1 = 2\nreturns 2", "3 × 2 = 6\nreturns 6", "4 × 6 = 24\nreturns 24"]
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    w, h, gap = 1.9, 0.62, 0.25
    for t, height in enumerate(heights):
        x = t * (w + gap)
        for level in range(height):
            top = level == height - 1
            if top and t == 4:
                colour = DONE                  # the base case
            elif top:
                colour = HILITE
            else:
                colour = FILL
            ax.add_patch(Rectangle((x, level * h), w, h, facecolor=colour,
                                   edgecolor=SLATE, linewidth=1.0))
            ax.text(x + w / 2, level * h + h / 2, frames[level], ha="center",
                    va="center", fontsize=7.6, family="monospace", color=SLATE)
        colour = MUTED if t < 4 else (GREEN if t == 4 else RED)
        ax.text(x + w / 2, -0.25, doing[t], ha="center", va="top", fontsize=8.3,
                color=colour)
    ax.annotate("", xy=(4 * (w + gap) - 0.1, 5 * h + 0.35), xytext=(0.2, 5 * h + 0.35),
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.6))
    ax.text(2 * (w + gap), 5 * h + 0.5, "winding: each call pushes a frame",
            ha="center", fontsize=10, color=SLATE)
    ax.annotate("", xy=(8 * (w + gap) + w - 0.2, 5 * h + 0.35),
                xytext=(4 * (w + gap) + w + 0.1, 5 * h + 0.35),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
    ax.text(6.5 * (w + gap) + 0.2, 5 * h + 0.5, "unwinding: each return pops one",
            ha="center", fontsize=10, color=SLATE)
    ax.set_xlim(-0.2, 9 * (w + gap))
    ax.set_ylim(-1.3, 5 * h + 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("factorial(4) on the call stack — time runs left to right",
                 fontsize=13, fontweight="bold", color=SLATE, pad=4)
    return base.save(fig, "call-stack")


# -- recursion trees ----------------------------------------------------------


def figure_fib_tree():
    dot = _digraph()
    counter = [0]
    repeated = {"fib(2)", "fib(1)", "fib(0)"}

    def build(n):
        counter[0] += 1
        name = f"n{counter[0]}"
        label = f"fib({n})"
        colour = HILITE if label == "fib(2)" else (DONE if n < 2 else FILL)
        dot.node(name, label, fillcolor=colour)
        if n >= 2:
            for child in (n - 1, n - 2):
                dot.edge(name, build(child))
        return name

    build(5)
    dot.attr(label=f"fib(5): {counter[0]} calls. fib(2) alone is computed 3 times "
             "(highlighted). Leaves are base cases.",
             labelloc="b", fontsize="11", fontname="Helvetica")
    del repeated
    return base.save_dot(dot, "fib-tree")


def figure_hanoi_tree():
    dot = _digraph()
    counter = [0]

    def build(n, src, dst, spare):
        counter[0] += 1
        name = f"h{counter[0]}"
        if n == 1:
            dot.node(name, f"move {src}→{dst}", fillcolor=DONE)
            return name
        dot.node(name, f"hanoi({n}, {src}→{dst})")
        left = build(n - 1, src, spare, dst)
        counter[0] += 1
        mid = f"h{counter[0]}"
        dot.node(mid, f"move {src}→{dst}", fillcolor=HILITE)
        right = build(n - 1, spare, dst, src)
        for child in (left, mid, right):
            dot.edge(name, child)
        return name

    build(3, "A", "C", "B")
    dot.attr(label="hanoi(3): move 2 out of the way, move the largest, move 2 back on top "
             "— 7 moves = 2³ − 1. Read the moves left to right along the bottom.",
             labelloc="b", fontsize="11", fontname="Helvetica")
    return base.save_dot(dot, "hanoi-tree")


def figure_binary_strings_tree():
    dot = _digraph()
    counter = [0]

    def build(prefix, remaining):
        counter[0] += 1
        name = f"b{counter[0]}"
        label = f'"{prefix}"' if prefix else '""'
        dot.node(name, label, fillcolor=DONE if remaining == 0 else FILL)
        if remaining:
            for bit in "01":
                child = build(prefix + bit, remaining - 1)
                dot.edge(name, child, label=f" {bit}", fontsize="10",
                         fontname="Helvetica", fontcolor=AMBER)
        return name

    build("", 3)
    dot.attr(label="All binary strings of length 3: two choices at every level, "
             "2³ = 8 leaves. The same shape as the subsets of a 3-item set.",
             labelloc="b", fontsize="11", fontname="Helvetica")
    return base.save_dot(dot, "choice-tree")


# -- counted, not timed -------------------------------------------------------


def figure_fib_calls():
    def naive_calls(n):
        return 1 if n < 2 else 1 + naive_calls(n - 1) + naive_calls(n - 2)

    ns = list(range(1, 31))
    naive = [naive_calls(n) for n in ns]
    memo = [2 * n - 1 for n in ns]             # each fib(k) computed once
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.plot(ns, naive, "o-", color=RED, markersize=4, linewidth=2,
            label="naive fib(n): calls  (≈ 1.6ⁿ)")
    ax.plot(ns, memo, "o-", color=GREEN, markersize=4, linewidth=2,
            label="with a memo array: calls  (2n − 1)")
    ax.set_yscale("log")
    ax.set_xlabel("n")
    ax.set_ylabel("number of calls (log scale)")
    ax.annotate(f"fib(30): {naive[-1]:,} calls", (30, naive[-1]),
                xytext=(17, naive[-1] * 1.8), fontsize=10, color=SLATE,
                arrowprops=dict(arrowstyle="-", color=MUTED))
    ax.annotate("fib(30): 59 calls", (30, memo[-1]), xytext=(20, 700), fontsize=10,
                color=SLATE, arrowprops=dict(arrowstyle="-", color=MUTED))
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("Same answer, different recursion: exponential against linear",
                 fontsize=12.5, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "fib-calls")


def figure_power_steps():
    def slow(n):
        return 0 if n == 0 else 1 + slow(n - 1)

    def fast(n):
        if n == 0:
            return 0
        half = fast(n // 2)
        return half + (2 if n % 2 else 1)

    ns = list(range(1, 257))
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.plot(ns, [slow(n) for n in ns], color=RED, linewidth=2,
            label="power by decrementing:  x · xⁿ⁻¹")
    ax.plot(ns, [fast(n) for n in ns], color=GREEN, linewidth=2,
            label="power by halving:  (x^(n/2))²")
    ax.set_xlabel("exponent n")
    ax.set_ylabel("multiplications")
    ax.set_xlim(0, 256)
    ax.set_ylim(0, 260)
    ax.text(200, 40, f"at n = 256:\n{fast(256)} multiplications against {slow(256)}",
            ha="center", fontsize=10, color=SLATE)
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("How you recurse decides the cost: O(n) against O(log n)",
                 fontsize=12.5, fontweight="bold", color=SLATE, pad=12)
    return base.save(fig, "power-steps")


FIGURES = [figure_call_stack, figure_fib_tree, figure_hanoi_tree,
           figure_binary_strings_tree, figure_fib_calls, figure_power_steps]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
