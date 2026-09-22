"""Static diagrams: arrays, linked lists, trees and graphs.

Every function takes *plain Python data* — a list, a list of (parent, child)
pairs, a networkx graph — so it works with whatever you implement in `dsa/`
without importing any of it.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch

from viz.style import MUTED, NODE_EDGE, as_index_set, colours

__all__ = [
    "draw_array",
    "draw_linked_list",
    "draw_tree",
    "draw_array_as_tree",
    "draw_graph",
]

_BOX_W = 1.15
_BOX_H = 0.70


def draw_array(values, highlight=None, done=None, title=None, show_index=True, ax=None):
    """Draw a list as contiguous cells with their indices underneath.

    Use this for arrays, for the partition state in quicksort, or for a DP
    table row.

    >>> draw_array([5, 2, 9, 1], highlight=2, done=[0])
    """
    highlight, done = as_index_set(highlight), as_index_set(done)
    n = len(values)
    if ax is None:
        _, ax = plt.subplots(figsize=(max(3.0, 0.95 * n + 1.0), 1.85))

    for i, value in enumerate(values):
        x = i * _BOX_W
        fill, edge = colours(i, highlight, done)
        ax.add_patch(
            FancyBboxPatch(
                (x, 0),
                _BOX_W,
                _BOX_H,
                boxstyle="square,pad=0",
                facecolor=fill,
                edgecolor=edge,
                linewidth=2.0 if (i in highlight or i in done) else 1.3,
            )
        )
        ax.text(x + _BOX_W / 2, _BOX_H / 2, str(value), ha="center", va="center", fontsize=12)
        if show_index:
            ax.text(
                x + _BOX_W / 2, -0.22, str(i),
                ha="center", va="center", fontsize=9, color=MUTED,
            )

    ax.set_xlim(-0.25, max(n * _BOX_W, 1) + 0.25)
    ax.set_ylim(-0.45, _BOX_H + 0.30)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=12)
    return ax


def draw_linked_list(values, highlight=None, done=None, title=None, ax=None):
    """Draw a singly linked list: boxes joined by arrows, terminated by None.

    `values` is the payload of each node, head first. Pass `highlight` the
    index your pointer is currently on — that is what makes a traversal
    legible when you step through it in class.
    """
    highlight, done = as_index_set(highlight), as_index_set(done)
    n = len(values)
    gap = 0.62
    if ax is None:
        _, ax = plt.subplots(figsize=(max(4.0, (_BOX_W + gap) * n + 2.0), 2.0))

    if n == 0:
        ax.text(0, _BOX_H / 2, "head → None", va="center", fontsize=12, color=MUTED)
        ax.set_xlim(-0.3, 3.0)
        ax.set_ylim(-0.3, _BOX_H + 0.6)
        ax.axis("off")
        if title:
            ax.set_title(title, fontsize=12)
        return ax

    for i, value in enumerate(values):
        x = i * (_BOX_W + gap)
        fill, edge = colours(i, highlight, done)
        ax.add_patch(
            FancyBboxPatch(
                (x, 0),
                _BOX_W,
                _BOX_H,
                boxstyle="round,pad=0.02",
                facecolor=fill,
                edgecolor=edge,
                linewidth=2.0 if (i in highlight or i in done) else 1.3,
            )
        )
        ax.text(x + _BOX_W / 2, _BOX_H / 2, str(value), ha="center", va="center", fontsize=12)
        ax.annotate(
            "",
            xy=(x + _BOX_W + gap, _BOX_H / 2),
            xytext=(x + _BOX_W, _BOX_H / 2),
            arrowprops=dict(arrowstyle="->", linewidth=1.3, color=NODE_EDGE),
        )

    ax.text(0, _BOX_H + 0.18, "head", fontsize=10, color=NODE_EDGE)
    tail_x = (n - 1) * (_BOX_W + gap) + _BOX_W + gap
    ax.text(tail_x + 0.08, _BOX_H / 2, "None", va="center", fontsize=10, color=MUTED)

    ax.set_xlim(-0.3, tail_x + 1.1)
    ax.set_ylim(-0.3, _BOX_H + 0.6)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=12)
    return ax


def draw_tree(edges, highlight=(), title=None, rankdir="TB"):
    """Render a tree or DAG from (parent, child) pairs using Graphviz.

    Returns a `graphviz.Digraph`, which renders inline in a notebook. Graphviz
    does the layout, so the result is clean without you positioning anything.

    >>> draw_tree([("A", "B"), ("A", "C"), ("B", "D")], highlight={"C"})

    Two nodes may need the same label — an expression tree can hold `2` twice.
    Anything after a `#` disambiguates the node without being displayed, the
    same `value#index` convention `draw_array_as_tree` uses:

    >>> draw_tree([("+#0", "2#1"), ("+#0", "2#2")])   # two distinct 2s

    Save it with `.render("bst", format="png", cleanup=True)`.
    """
    from graphviz import Digraph  # imported lazily: needs the dot binary

    dot = Digraph(graph_attr={"rankdir": rankdir, "bgcolor": "transparent"})
    if title:
        dot.attr(label=title, labelloc="t", fontsize="14")
    dot.attr("node", shape="circle", style="filled", fontname="Helvetica", fontsize="12")
    dot.attr("edge", color=NODE_EDGE)

    seen = set()
    highlight = set(highlight)
    for parent, child in edges:
        for node in (parent, child):
            if node in seen:
                continue
            seen.add(node)
            fill, edge = colours(node, highlight)
            dot.node(str(node), label=str(node).split("#", 1)[0], fillcolor=fill, color=edge)
        dot.edge(str(parent), str(child))
    return dot


def draw_array_as_tree(values, highlight=(), title=None):
    """View a list as a complete binary tree — the heap layout.

    Children of index i are 2i+1 and 2i+2. Shows *why* heapify works on a
    flat array.
    """
    edges = []
    for i in range(len(values)):
        for child in (2 * i + 1, 2 * i + 2):
            if child < len(values):
                edges.append((f"{values[i]}#{i}", f"{values[child]}#{child}"))

    from graphviz import Digraph

    dot = Digraph(graph_attr={"bgcolor": "transparent"})
    if title:
        dot.attr(label=title, labelloc="t", fontsize="14")
    dot.attr("node", shape="circle", style="filled", fontname="Helvetica", fontsize="12")
    dot.attr("edge", color=NODE_EDGE)

    highlight = as_index_set(highlight)
    for i, value in enumerate(values):
        fill, edge = colours(i, highlight)
        dot.node(f"{value}#{i}", label=str(value), fillcolor=fill, color=edge)
    for parent, child in edges:
        dot.edge(parent, child)
    return dot


def draw_graph(graph, pos=None, highlight_nodes=(), highlight_edges=(), title=None, ax=None):
    """Draw a networkx graph, optionally emphasising a path or visited set.

    Pass `highlight_nodes` the frontier of a BFS, or `highlight_edges` the
    edges of a shortest path, to show an algorithm mid-run.
    """
    from viz.style import HILITE_EDGE, HILITE_FILL, NODE_FILL

    if ax is None:
        _, ax = plt.subplots(figsize=(6.0, 4.5))
    if pos is None:
        pos = nx.spring_layout(graph, seed=27)

    highlight_nodes = set(highlight_nodes)
    node_fill = [HILITE_FILL if n in highlight_nodes else NODE_FILL for n in graph.nodes()]
    node_edge = [HILITE_EDGE if n in highlight_nodes else NODE_EDGE for n in graph.nodes()]

    hl = {frozenset(e) for e in highlight_edges}
    edge_colour = [HILITE_EDGE if frozenset(e) in hl else NODE_EDGE for e in graph.edges()]
    edge_width = [2.6 if frozenset(e) in hl else 1.2 for e in graph.edges()]

    nx.draw_networkx_nodes(
        graph, pos, ax=ax, node_color=node_fill, edgecolors=node_edge,
        linewidths=1.6, node_size=760,
    )
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color=edge_colour, width=edge_width)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=11)

    weights = nx.get_edge_attributes(graph, "weight")
    if weights:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights, ax=ax, font_size=9)

    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=12)
    return ax
