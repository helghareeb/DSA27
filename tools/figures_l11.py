"""Generate the figures for Lecture 11 — Trees.

Run it from the repository root:

    python tools/figures_l11.py                       # timing uses YOUR dsa/tree.py
    python tools/with_solutions.py tools/figures_l11.py   # timing uses solutions/

Same conventions as `tools/figures.py`. The diagrams are drawn from fixed trees
built by a tiny insert of its own below, so they need nothing from `dsa/`. The
measured figure builds real trees with **your** `dsa/tree.py` and times them, so
it needs a working implementation (the lecture's copy was made from the
instructor's reference solution); without one, every other figure is still
drawn.
"""

from __future__ import annotations

import math
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
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "11-trees" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
PURPLE = "#7A5195"
SHADE = "#F1ECE0"
GONE = "#EEEEEE"

SAMPLE = [8, 3, 10, 1, 6, 14, 4, 7, 13]


# -- a tiny BST of our own, only for drawing ------------------------------------


class N:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right


def build(values):
    root = None
    for v in values:
        if root is None:
            root = N(v)
            continue
        node = root
        while True:
            if v == node.value:
                break
            side = "left" if v < node.value else "right"
            nxt = getattr(node, side)
            if nxt is None:
                setattr(node, side, N(v))
                break
            node = nxt
    return root


def nodes(root):
    out = []

    def walk(n):
        if n is not None:
            walk(n.left)
            out.append(n)
            walk(n.right)

    walk(root)
    return out


def layout(root, dx=1.0, dy=1.1):
    """x = in-order rank, y = -depth. A BST drawn this way reads sorted left to right."""
    pos = {}
    rank = [0]

    def walk(n, depth):
        if n is None:
            return
        walk(n.left, depth + 1)
        pos[n.value] = (rank[0] * dx, -depth * dy)
        rank[0] += 1
        walk(n.right, depth + 1)

    walk(root, 0)
    return pos


def draw_tree(ax, root, fills=None, edge_colours=None, pos=None, r=0.32, fontsize=12,
              ghost=(), text_colour=None, labels=None):
    fills = fills or {}
    edge_colours = edge_colours or {}
    text_colour = text_colour or {}
    labels = labels or {}
    pos = pos or layout(root)

    def edges(n):
        if n is None:
            return
        for c in (n.left, n.right):
            if c is not None:
                (x1, y1), (x2, y2) = pos[n.value], pos[c.value]
                colour = edge_colours.get((n.value, c.value), MUTED)
                lw = 2.6 if (n.value, c.value) in edge_colours else 1.3
                ax.plot([x1, x2], [y1, y2], color=colour, linewidth=lw, zorder=1,
                        linestyle=":" if c.value in ghost else "-")
                edges(c)

    edges(root)
    for n in nodes(root):
        x, y = pos[n.value]
        fill = fills.get(n.value, FILL)
        ax.add_patch(Circle((x, y), r, facecolor=fill, edgecolor=SLATE, linewidth=1.3,
                            zorder=2, linestyle=":" if n.value in ghost else "-"))
        ax.text(x, y, str(labels.get(n.value, n.value)), ha="center", va="center", fontsize=fontsize,
                color=text_colour.get(n.value, SLATE), zorder=3)
    return pos


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text, size=12.5):
    ax.set_title(text, fontsize=size, fontweight="bold", color=SLATE, pad=6)


def subtitle(ax, text):
    ax.set_title(text, fontsize=11, color=SLATE, pad=4)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.4):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def path_edges(path, colour=AMBER):
    return {(a, b): colour for a, b in zip(path, path[1:])}


# -- vocabulary -------------------------------------------------------------------


def figure_terminology():
    root = build(SAMPLE)
    pos = layout(root)
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    # the subtree rooted at 3
    ax.add_patch(FancyBboxPatch((-0.55, -3.75), 5.1, 3.1, boxstyle="round,pad=0.05",
                                facecolor=SHADE, edgecolor=AMBER, linewidth=1.2,
                                linestyle="--", zorder=0))
    ax.text(2.0, -3.85, "the subtree rooted at 3", fontsize=9.5, color=AMBER, va="top",
            ha="center")
    fills = {8: HILITE, 1: DONE, 4: DONE, 7: DONE, 13: DONE}
    draw_tree(ax, root, fills=fills, pos=pos)
    for d in range(4):
        ax.text(-1.4, -d * 1.1, f"depth {d}", ha="right", va="center", fontsize=10,
                color=MUTED)
    ax.annotate("root: no parent", xy=(pos[8][0] + 0.33, pos[8][1]),
                xytext=(pos[8][0] + 1.6, pos[8][1] + 0.35), fontsize=10, color=SLATE,
                arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.1))
    ax.annotate("leaves: no children", xy=(pos[13][0] + 0.3, pos[13][1] - 0.1),
                xytext=(pos[13][0] + 1.3, pos[13][1] - 0.2), fontsize=10, color=GREEN,
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.1))
    ax.annotate("an edge", xy=((pos[10][0] + pos[14][0]) / 2, (pos[10][1] + pos[14][1]) / 2),
                xytext=(pos[14][0] + 0.9, pos[10][1] + 0.1), fontsize=9.5, color=MUTED,
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))
    ax.text(10.4, -1.9, "9 nodes, 8 edges\nheight 3 = edges on the\nlongest root-to-leaf path"
            "\n(8 → 10 → 14 → 13)\n\n6 is the parent of 4 and 7;\n4 and 7 are siblings", fontsize=10, color=SLATE, va="center")
    clean(ax, (-2.9, 13.4), (-4.3, 0.9))
    title(ax, "A tree: one root, every other node has exactly one parent")
    return base.save(fig, "terminology")


def figure_bst_property():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.3),
                             gridspec_kw={"width_ratios": [1.55, 1]})
    ax = axes[0]
    root = build(SAMPLE)
    pos = draw_tree(ax, root)
    ranges = {8: "(−∞, ∞)", 3: "(−∞, 8)", 10: "(8, ∞)", 1: "(−∞, 3)", 6: "(3, 8)",
              14: "(10, ∞)", 4: "(3, 6)", 7: "(6, 8)", 13: "(10, 14)"}
    for v, text in ranges.items():
        x, y = pos[v]
        ax.text(x, y - 0.45, text, ha="center", va="top", fontsize=7.8, color=PURPLE)
    clean(ax, (-0.8, 8.8), (-4.0, 0.6))
    subtitle(ax, "valid: each value lies inside the range its ancestors allow")

    ax = axes[1]
    bad = N(8, N(3, None, N(9)), N(10))
    pos = {8: (1.5, 0.0), 3: (0.5, -1.1), 9: (1.1, -2.2), 10: (2.6, -1.1)}
    draw_tree(ax, bad, pos=pos, fills={9: "#F6D5D2"}, text_colour={9: RED})
    ax.text(1.1, -2.7, "9 > 3: fine for its parent\n9 > 8: but it is in 8's LEFT subtree",
            ha="center", va="top", fontsize=9, color=RED)
    clean(ax, (-0.8, 3.4), (-4.0, 0.6))
    subtitle(ax, "not a BST, though every parent–child pair looks right")
    fig.suptitle("The BST property: left subtree smaller, right subtree larger — "
                 "all of it", fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "bst-property")


# -- search and insert ------------------------------------------------------------


def figure_search():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.0))
    root = build(SAMPLE)
    ax = axes[0]
    path = [8, 3, 6, 7]
    pos = draw_tree(ax, root, fills={8: HILITE, 3: HILITE, 6: HILITE, 7: DONE},
                    edge_colours=path_edges(path))
    notes = {8: "7 < 8: left", 3: "7 > 3: right", 6: "7 > 6: right", 7: "found"}
    for v, t in notes.items():
        x, y = pos[v]
        left = v == 3
        ax.text(x - 0.4 if left else x + 0.4, y + 0.25, t, fontsize=8.5,
                ha="right" if left else "left", color=AMBER if v != 7 else GREEN)
    clean(ax, (-0.8, 9.2), (-3.8, 0.7))
    subtitle(ax, "contains(7): 4 comparisons")

    ax = axes[1]
    path = [8, 3, 6, 4]
    pos = draw_tree(ax, root, fills={8: HILITE, 3: HILITE, 6: HILITE, 4: HILITE},
                    edge_colours=path_edges(path))
    x, y = pos[4]
    ax.plot([x, x + 0.55], [y, y - 0.75], color=RED, linewidth=1.6, linestyle="--")
    ax.text(x + 0.6, y - 0.8, "None", fontsize=9, color=RED, va="top")
    ax.text(x - 0.2, y - 1.25, "5 > 4: right — but there is nothing there", fontsize=8.5,
            color=RED, va="top")
    clean(ax, (-0.8, 9.2), (-3.8, 0.7))
    subtitle(ax, "contains(5): 4 comparisons, then None: not there")
    fig.suptitle("Search goes down one path: at most h + 1 comparisons",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "search")


def figure_insert():
    fig, ax = plt.subplots(figsize=(8.4, 4.3))
    root = build(SAMPLE + [5])
    path = [8, 3, 6, 4, 5]
    pos = draw_tree(ax, root, fills={8: HILITE, 3: HILITE, 6: HILITE, 4: HILITE, 5: DONE},
                    edge_colours={**path_edges(path[:-1]), (4, 5): GREEN})
    x, y = pos[5]
    ax.text(x + 0.45, y, "new leaf: 4.right = TreeNode(5)", fontsize=9.5, color=GREEN,
            va="center")
    ax.text(10.6, -0.4, "insert(5):\n5 < 8: left\n5 > 3: right\n5 < 6: left\n"
            "5 > 4: right — None,\nso the new node goes here", fontsize=9.5, color=SLATE,
            va="top", family="monospace")
    clean(ax, (-0.8, 14.8), (-4.8, 0.7))
    title(ax, "Insert = a search that fails, then one new leaf where it stopped")
    return base.save(fig, "insert")


# -- delete -----------------------------------------------------------------------


def figure_delete_easy():
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 7.0))
    root = build(SAMPLE)
    pos = layout(root)
    red = "#F6D5D2"
    draw_tree(axes[0][0], root, fills={1: red}, text_colour={1: RED})
    subtitle(axes[0][0], "leaf: delete(1)")
    draw_tree(axes[0][1], build([8, 3, 10, 6, 14, 4, 7, 13]), pos=pos)
    subtitle(axes[0][1], "after: 3.left = None")
    draw_tree(axes[1][0], root, fills={14: red, 13: HILITE}, text_colour={14: RED})
    subtitle(axes[1][0], "one child: delete(14) — its only child is 13")
    moved = dict(pos)
    moved[13] = pos[14]
    draw_tree(axes[1][1], build([8, 3, 10, 1, 6, 13, 4, 7]), pos=moved, fills={13: HILITE},
              edge_colours={(10, 13): GREEN})
    subtitle(axes[1][1], "after: 10.right = 13 — the child moves up")
    for row in axes:
        for ax in row:
            clean(ax, (-0.7, 8.7), (-3.8, 0.6))
    for y in (0.73, 0.26):
        fig.text(0.5, y, "→", fontsize=26, color=AMBER, ha="center", va="center")
    fig.suptitle("The easy cases: a leaf is cut off; a single child takes its parent's "
                 "place", fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "delete-easy")


def figure_delete_successor():
    """Two verified examples: delete(3) and delete(8) on SAMPLE."""
    fig, axes = plt.subplots(2, 3, figsize=(13.0, 7.8))
    root = build(SAMPLE)
    red = "#F6D5D2"

    # row 1: delete(3) — the successor 4 is a leaf, two levels down
    ax = axes[0][0]
    draw_tree(ax, root, fills={3: red, 6: HILITE, 4: DONE}, text_colour={3: RED},
              edge_colours=path_edges([3, 6, 4]))
    subtitle(ax, "1. find the successor: right once,\nthen left until None → 4")
    ax = axes[0][1]
    pos = layout(root)
    draw_tree(ax, root, fills={3: DONE, 4: GONE}, labels={3: 4}, ghost={4},
              text_colour={4: MUTED})
    ax.text(pos[4][0], pos[4][1] - 0.45, "old 4:\nremove it", ha="center", va="top",
            fontsize=8.5, color=RED)
    ax.text(pos[3][0] - 0.45, pos[3][1] + 0.35, "3 → 4", ha="right", fontsize=9,
            color=GREEN)
    subtitle(ax, "2. copy 4 into the node that held 3\n(two 4s for a moment)")
    ax = axes[0][2]
    moved = dict(pos)
    moved[4] = pos[3]
    draw_tree(ax, build([8, 4, 10, 1, 6, 14, 7, 13]), pos=moved, fills={4: DONE})
    subtitle(ax, "3. delete the old 4 — a leaf.\nStill valid: 1 < 4 < 6 and 7")

    # row 2: delete(8) — the successor 10 is the right child, with a right subtree
    ax = axes[1][0]
    draw_tree(ax, root, fills={8: red, 10: DONE}, text_colour={8: RED},
              edge_colours=path_edges([8, 10]))
    subtitle(ax, "1. delete(8): right once → 10;\n10.left is None, so 10 is it")
    ax = axes[1][1]
    draw_tree(ax, root, fills={8: DONE, 10: GONE}, labels={8: 10}, ghost={10},
              text_colour={10: MUTED}, edge_colours={(10, 14): AMBER})
    subtitle(ax, "2. copy 10 into the root;\nold 10 has ONE child, 14")
    ax = axes[1][2]
    moved = dict(pos)
    moved[10], moved[14], moved[13] = pos[8], pos[10], pos[14]
    draw_tree(ax, build([10, 3, 14, 1, 6, 13, 4, 7]), pos=moved, fills={10: DONE, 14: HILITE},
              edge_colours={(10, 14): GREEN})
    subtitle(ax, "3. splice 14 into the old 10's place\n(the one-child case)")
    for row in axes:
        for ax in row:
            clean(ax, (-0.7, 8.7), (-3.8, 0.6))
    fig.suptitle("Two children: replace the value with the in-order successor, "
                 "then delete the successor", fontsize=12.5, fontweight="bold",
                 color=SLATE)
    fig.tight_layout()
    return base.save(fig, "delete-successor")


# -- traversals -------------------------------------------------------------------


def orders(root):
    pre, ino, post = [], [], []

    def walk(n):
        if n is None:
            return
        pre.append(n.value)
        walk(n.left)
        ino.append(n.value)
        walk(n.right)
        post.append(n.value)

    walk(root)
    level, frontier = [], [root]
    while frontier:                       # drawing helper only: a list is fine here
        nxt = []
        for n in frontier:
            level.append(n.value)
            nxt += [c for c in (n.left, n.right) if c is not None]
        frontier = nxt
    return {"in-order": ino, "pre-order": pre, "post-order": post, "level-order": level}


def figure_traversals():
    root = build(SAMPLE)
    walks = orders(root)
    rules = {"pre-order": "node, left, right", "in-order": "left, node, right",
             "post-order": "left, right, node", "level-order": "row by row, left to right"}
    fig, axes = plt.subplots(2, 2, figsize=(11.6, 7.4))
    for ax, name in zip(axes.flat, ["pre-order", "in-order", "post-order", "level-order"]):
        order = walks[name]
        pos = draw_tree(ax, root, fontsize=11)
        for k, v in enumerate(order, start=1):
            x, y = pos[v]
            ax.add_patch(Circle((x + 0.33, y + 0.33), 0.19, facecolor=AMBER, edgecolor="none",
                                zorder=4))
            ax.text(x + 0.33, y + 0.33, str(k), ha="center", va="center", fontsize=8,
                    color="white", fontweight="bold", zorder=5)
        ax.text(4.0, -4.05, ", ".join(map(str, order)), ha="center", va="top",
                fontsize=11, color=SLATE, family="monospace")
        subtitle(ax, f"{name}: {rules[name]}")
        clean(ax, (-0.8, 8.8), (-4.6, 0.8))
    fig.suptitle("Four walks of the same tree — the amber numbers are the visit order",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "traversals")


def figure_level_order():
    """The queue after each step of level_order on SAMPLE — verified by running it."""
    root = build(SAMPLE)
    rows = []
    queue, out = [root], []                  # a list here only to draw the states
    rows.append(("start", [], [n.value for n in queue]))
    while queue:
        n = queue.pop(0)
        out.append(n.value)
        added = [c for c in (n.left, n.right) if c is not None]
        queue += added
        rows.append((f"dequeue {n.value}", [c.value for c in added],
                     [q.value for q in queue]))
    fig, ax = plt.subplots(figsize=(10.2, 6.2))
    w, h = 0.62, 0.5
    for r, (step, added, q) in enumerate(rows):
        y = -r * 0.62
        ax.text(0, y + h / 2, step, fontsize=10, va="center", color=SLATE,
                family="monospace")
        ax.text(2.35, y + h / 2, ("enqueue " + ", ".join(map(str, added))) if added else
                ("—" if r else ""), fontsize=10, va="center",
                color=GREEN if added else MUTED, family="monospace")
        for i, v in enumerate(q):
            ax.add_patch(Rectangle((5.2 + i * w, y), w, h, facecolor=FILL if i else HILITE,
                                   edgecolor=SLATE, linewidth=1.1))
            ax.text(5.2 + i * w + w / 2, y + h / 2, str(v), ha="center", va="center",
                    fontsize=10, color=SLATE)
        if not q:
            ax.text(5.2, y + h / 2, "empty: stop", fontsize=10, va="center", color=RED)
    ax.text(0, 0.85, "step", fontsize=10, color=MUTED)
    ax.text(2.35, 0.85, "children added", fontsize=10, color=MUTED)
    ax.text(5.2, 0.85, "queue after the step (front on the left)", fontsize=10,
            color=MUTED)
    ax.text(0, -len(rows) * 0.62 - 0.1, "visited: " + ", ".join(map(str, out)),
            fontsize=10.5, color=SLATE, family="monospace", va="top")
    clean(ax, (-0.2, 9.4), (-len(rows) * 0.62 - 0.6, 1.2))
    title(ax, "level_order(): the queue holds the nodes found but not yet visited")
    return base.save(fig, "level-order")


def figure_expression():
    fig, ax = plt.subplots(figsize=(9.6, 3.9))
    tree = N("*", N("+", N("3"), N("4")), N("2"))
    pos = {"*": (2.0, 0.0), "+": (1.0, -1.1), "3": (0.4, -2.2), "4": (1.6, -2.2),
           "2": (3.0, -1.1)}
    draw_tree(ax, tree, pos=pos, fills={"*": HILITE, "+": HILITE})
    lines = [("pre-order", "* + 3 4 2", "prefix (Polish) notation"),
             ("in-order", "3 + 4 * 2", "infix — but the brackets are lost!"),
             ("post-order", "3 4 + 2 *", "postfix: Lecture 06's stack evaluates it → 14")]
    for i, (name, walk, note) in enumerate(lines):
        y = -0.1 - i * 0.8
        ax.text(4.3, y, f"{name:11s}", fontsize=10.5, color=SLATE, family="monospace",
                va="center")
        ax.text(6.15, y, walk, fontsize=11, color=AMBER, family="monospace", va="center",
                fontweight="bold")
        ax.text(8.2, y, note, fontsize=9.5, color=SLATE, va="center")
    clean(ax, (-0.2, 13.4), (-2.7, 0.6))
    title(ax, "An expression tree for (3 + 4) * 2: the shape holds the precedence")
    return base.save(fig, "expression")


# -- shape ------------------------------------------------------------------------


def figure_degenerate():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.0),
                             gridspec_kw={"width_ratios": [1.15, 1]})
    chain = build([1, 2, 3, 4, 5, 6, 7])
    pos = {v: ((v - 1) * 0.8, -(v - 1) * 0.72) for v in range(1, 8)}
    draw_tree(axes[0], chain, pos=pos, r=0.28, fontsize=11)
    axes[0].text(0.3, -4.2, "insert 1, 2, 3, 4, 5, 6, 7\nheight 6 = n − 1\n"
                 "contains(7): 7 comparisons", fontsize=10, color=RED, va="top")
    clean(axes[0], (-0.6, 5.6), (-4.9, 0.5))
    subtitle(axes[0], "sorted order: a linked list in a tree costume")
    balanced = build([4, 2, 6, 1, 3, 5, 7])
    draw_tree(axes[1], balanced, pos=layout(balanced, dx=0.8, dy=1.0), r=0.28, fontsize=11)
    axes[1].text(2.4, -2.6, "insert 4, 2, 6, 1, 3, 5, 7\nheight 2 = ⌊log₂ 7⌋\n"
                 "contains(7): 3 comparisons", fontsize=10, color=GREEN, va="top",
                 ha="center")
    clean(axes[1], (-0.6, 5.4), (-4.9, 0.5))
    subtitle(axes[1], "middle first: as short as 7 nodes can be")
    fig.suptitle("Same seven values, same code — the insertion order decides the height",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "degenerate")


def figure_measured():
    from dsa.tree import BinarySearchTree
    try:
        BinarySearchTree([2, 1, 3]).height()
    except NotImplementedError:
        print("  (skipped measured.png: dsa/tree.py is not implemented yet)")
        return None
    sys.setrecursionlimit(50_000)          # height() recurses h deep: n on sorted input
    rng = random.Random(11)
    sizes = [2 ** k for k in range(6, 13)]           # 64 .. 4,096
    trials = 20
    h_sorted, h_random, h_random_max = [], [], []
    t_sorted, t_random = [], []
    for n in sizes:
        values = list(range(n))
        tree = BinarySearchTree(values)
        h_sorted.append(tree.height())
        targets = [rng.randrange(n) for _ in range(2000)]
        t_sorted.append(time_lookups(tree, targets))
        heights = []
        for _ in range(trials):
            shuffled = values[:]
            rng.shuffle(shuffled)
            tree = BinarySearchTree(shuffled)
            heights.append(tree.height())
        h_random.append(sum(heights) / trials)
        h_random_max.append(max(heights))
        t_random.append(time_lookups(tree, targets))
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.7))
    ax = axes[0]
    ax.plot(sizes, h_sorted, "o-", color=RED, linewidth=2.1, markersize=5,
            label="sorted insertion order: n − 1")
    ax.plot(sizes, h_random, "o-", color=GREEN, linewidth=2.1, markersize=5,
            label=f"random order (mean of {trials})")
    ax.plot(sizes, [math.floor(math.log2(n)) for n in sizes], "--", color=MUTED,
            linewidth=1.4, label="⌊log₂ n⌋: the shortest possible")
    ax.set_ylabel("height (log scale)")
    ax.set_title("height", fontsize=11.5, color=SLATE)
    ax = axes[1]
    ax.plot(sizes, [t * 1e6 for t in t_sorted], "o-", color=RED, linewidth=2.1,
            markersize=5, label="sorted insertion order")
    ax.plot(sizes, [t * 1e6 for t in t_random], "o-", color=GREEN, linewidth=2.1,
            markersize=5, label="random insertion order")
    ax.set_ylabel("microseconds per contains() (log scale)")
    ax.set_title("time: one successful search, average of 2,000", fontsize=11.5,
                 color=SLATE)
    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_xlabel("n, values inserted (log scale)")
        ax.grid(True, alpha=0.25, linewidth=0.7)
        ax.legend(frameon=False, fontsize=9, loc="upper left")
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    fig.suptitle("Measured: a BST is only as fast as it is short", fontsize=12.5,
                 fontweight="bold", color=SLATE)
    fig.tight_layout()
    print("    n          ", sizes)
    print("    h sorted   ", h_sorted)
    print("    h random   ", [round(h, 1) for h in h_random], "max", h_random_max)
    print("    us sorted  ", [round(t * 1e6, 2) for t in t_sorted])
    print("    us random  ", [round(t * 1e6, 2) for t in t_random])
    return base.save(fig, "measured")


def time_lookups(tree, targets):
    best = float("inf")
    for _ in range(3):
        start = time.perf_counter()
        for t in targets:
            tree.contains(t)
        best = min(best, time.perf_counter() - start)
    return best / len(targets)


FIGURES = [figure_terminology, figure_bst_property, figure_search, figure_insert,
           figure_delete_easy, figure_delete_successor, figure_traversals,
           figure_level_order, figure_expression, figure_degenerate, figure_measured]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
