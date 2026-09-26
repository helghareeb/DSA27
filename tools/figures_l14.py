"""Generate the figures for Lecture 14 — Graphs and graph searches.

Run it from the repository root:

    python tools/figures_l14.py                            # uses YOUR dsa/graph.py
    python tools/with_solutions.py tools/figures_l14.py    # uses solutions/

Same conventions as `tools/figures.py`. Every picture of a search is drawn
from what `dsa/graph.py` actually returns — visit orders, parents, the
topological order, the maze route — so the figures need a working
`dsa/graph.py` (and the hash map, queue and stack it stands on). The lecture's
copies were made from the instructor's reference solution. The measured figure
is real timing and will differ slightly on your machine.
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
import networkx as nx
from matplotlib.patches import Rectangle

base.OUT = ROOT / "docs" / "lectures" / "14-graphs" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
GREY_NODE = "#BFC5C7"
WALL = "#3C4A4D"
NODE_EDGE = "#3a5a8c"

# The lecture's running example: seven nodes, eight edges, laid out by distance
# from A so the BFS layers read left to right.
G_EDGES = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"),
           ("D", "F"), ("E", "F"), ("F", "G")]
G_POS = {"A": (0, 0), "B": (1, 0.8), "C": (1, -0.8), "D": (2, 0.8),
         "E": (2, -0.8), "F": (3, 0), "G": (4, 0)}

# The test file's sample graph.
SAMPLE_EDGES = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D")]
SAMPLE_POS = {"A": (0, 1), "B": (1, 1), "C": (0, 0), "D": (1, 0)}

# Course prerequisites from the Software Engineering bylaw (2013), course
# specifications: an edge X -> Y means "X is a prerequisite of Y".
PREREQUISITES = [("CS012", "CS113"), ("CS012", "IS122"), ("MATH012", "IS122"),
                 ("IS122", "IS123"), ("IS123", "IS142"), ("CS012", "IS142"),
                 ("IT022", "IT131"), ("IS122", "IT131"), ("SWE021", "SWE132"),
                 ("SWE132", "SWE141"), ("IS122", "SWE141"), ("SWE141", "SWE144")]
COURSE_NAMES = {
    "CS012": "Fundamentals of\nProgramming", "CS113": "Programming 2",
    "MATH012": "Discrete\nStructures", "IS122": "Data Structures\nand Algorithms",
    "IS123": "Database\nSystems", "IS142": "Data Mining", "IT022": "Data\nCommunications",
    "IT131": "Computer\nNetworks", "SWE021": "Intro. to Software\nEngineering",
    "SWE132": "Software Design\nand Architecture", "SWE141": "Software\nConstruction",
    "SWE144": "Software\nReengineering",
}

MAZE = [
    "S..#....",
    "##.#.##.",
    "....#...",
    ".##...#.",
    "...##.#.",
    "##.....T",
]


def build(cls, edges, directed=False, nodes=()):
    graph = cls(directed=directed)
    for node in nodes:
        graph.add_node(node)
    for source, target in edges:
        graph.add_edge(source, target)
    return graph


def draw(ax, edges, pos, directed=False, fills=None, edge_colours=None, labels=None,
         node_size=760, font_size=11, widths=None, nodes=None):
    """A networkx drawing in the course palette, with per-node fills."""
    graph = nx.DiGraph() if directed else nx.Graph()
    graph.add_nodes_from(nodes if nodes is not None else pos)
    graph.add_edges_from(edges)
    fills = fills or {}
    edge_colours = edge_colours or {}
    widths = widths or {}
    node_list = list(graph.nodes())
    nx.draw_networkx_nodes(graph, pos, ax=ax, nodelist=node_list,
                           node_color=[fills.get(n, FILL) for n in node_list],
                           edgecolors=NODE_EDGE, linewidths=1.5, node_size=node_size)
    edge_list = list(graph.edges())

    def key(e):
        return e if directed else frozenset(e)

    kwargs = dict(arrows=True, arrowstyle="-|>", arrowsize=16,
                  node_size=node_size) if directed else {}
    nx.draw_networkx_edges(graph, pos, ax=ax, edgelist=edge_list,
                           edge_color=[edge_colours.get(key(e), NODE_EDGE) for e in edge_list],
                           width=[widths.get(key(e), 1.3) for e in edge_list], **kwargs)
    nx.draw_networkx_labels(graph, pos, ax=ax, labels=labels, font_size=font_size,
                            font_color=SLATE)
    ax.axis("off")


def title(ax, text, size=11.5):
    ax.set_title(text, fontsize=size, color=SLATE, pad=6)


def pad(ax, dx=0.35, dy=0.45):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    ax.set_xlim(x0 - dx, x1 + dx)
    ax.set_ylim(y0 - dy, y1 + dy)


# -- vocabulary ---------------------------------------------------------------


def figure_vocabulary():
    from dsa.graph import Graph

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9))
    g = build(Graph, G_EDGES)

    # left: undirected, with degrees
    ax = axes[0]
    draw(ax, G_EDGES, G_POS)
    for node, (x, y) in G_POS.items():
        ax.text(x, y + (0.34 if y >= 0 else -0.34), f"deg {g.degree(node)}",
                ha="center", va="center", fontsize=8.5, color=AMBER)
    pad(ax)
    title(ax, "undirected: 7 vertices, 8 edges\ndegrees add up to 16 = 2 × 8")

    # middle: a path and a cycle
    ax = axes[1]
    path = [("A", "B"), ("B", "D"), ("D", "F"), ("F", "G")]
    cycle = [("C", "D"), ("D", "F"), ("F", "E"), ("E", "C")]
    colours = {frozenset(e): AMBER for e in path}
    colours.update({frozenset(e): GREEN for e in cycle})
    colours[frozenset(("D", "F"))] = SLATE
    widths = {frozenset(e): 3.0 for e in path + cycle}
    draw(ax, G_EDGES, G_POS, edge_colours=colours, widths=widths)
    ax.text(2.0, -1.55, "path A-B-D-F-G (amber), 4 edges\ncycle C-D-F-E-C (green); D-F is in both",
            ha="center", va="center", fontsize=8.8, color=SLATE)
    pad(ax, dy=0.6)
    title(ax, "a path, and a cycle")

    # right: directed
    ax = axes[2]
    dag = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    pos = {"A": (0, 0), "B": (1, 0.8), "C": (1, -0.8), "D": (2, 0)}
    draw(ax, dag, pos, directed=True)
    ax.text(0, -0.45, "out 2, in 0", ha="center", fontsize=8.5, color=AMBER)
    ax.text(2, -0.45, "out 0, in 2", ha="center", fontsize=8.5, color=AMBER)
    ax.text(1.0, -1.55, "no way back to A: a DAG", ha="center", fontsize=8.8,
            color=SLATE)
    pad(ax, dy=0.6)
    title(ax, "directed: an edge has a direction")

    fig.suptitle("Vertices, edges, degree, paths and cycles", fontsize=12.5,
                 fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "vocabulary")


def figure_components():
    from dsa.graph import Graph, connected_components

    edges = [("A", "B"), ("B", "C"), ("A", "C"), ("D", "E"), ("F", "G"), ("G", "H")]
    g = build(Graph, edges, nodes=["A", "B", "C", "D", "E", "F", "G", "H", "I"])
    groups = connected_components(g)
    pos = {"A": (0, 1), "B": (1, 1), "C": (0.5, 0.2), "D": (2.2, 1), "E": (2.2, 0.2),
           "F": (3.4, 1), "G": (4.2, 0.6), "H": (3.4, 0.2), "I": (5.3, 0.6)}
    palette = [FILL, HILITE, DONE, "#E6D6EC"]
    fills = {}
    for i, group in enumerate(groups):
        for node in group:
            fills[node] = palette[i]
    fig, ax = plt.subplots(figsize=(9.6, 2.9))
    draw(ax, edges, pos, fills=fills, nodes=list(pos))
    text = "   ".join("{" + ", ".join(group) + "}" for group in groups)
    ax.text(2.65, -0.45, f"connected_components(g) → {len(groups)} components:  {text}",
            ha="center", fontsize=9.5, color=SLATE)
    pad(ax, dy=0.5)
    title(ax, "Connected components: the pieces you can walk within", 12.5)
    return base.save(fig, "components")


# -- representations ----------------------------------------------------------


def figure_representations():
    from dsa.graph import Graph, MatrixGraph

    g = build(Graph, SAMPLE_EDGES)
    m = build(MatrixGraph, SAMPLE_EDGES)
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.8),
                             gridspec_kw={"width_ratios": [1, 1.35, 1.2]})
    ax = axes[0]
    draw(ax, SAMPLE_EDGES, SAMPLE_POS)
    pad(ax)
    title(ax, "the graph")

    ax = axes[1]
    nodes = g.nodes()
    for r, node in enumerate(nodes):
        y = -r
        ax.add_patch(Rectangle((0, y), 0.8, 0.7, facecolor=HILITE, edgecolor=SLATE))
        ax.text(0.4, y + 0.35, node, ha="center", va="center", fontsize=11, color=SLATE)
        ax.annotate("", xy=(1.35, y + 0.35), xytext=(0.85, y + 0.35),
                    arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.2))
        for c, other in enumerate(g.neighbours(node)):
            ax.add_patch(Rectangle((1.4 + 0.75 * c, y), 0.75, 0.7, facecolor=FILL,
                                   edgecolor=SLATE))
            ax.text(1.4 + 0.75 * c + 0.375, y + 0.35, other, ha="center", va="center",
                    fontsize=11, color=SLATE)
    ax.text(0.2, 1.05, "hash map", ha="center", fontsize=9, color=AMBER)
    ax.text(2.75, 1.05, "DynamicArray of neighbours", ha="center", fontsize=9, color=AMBER)
    ax.set_xlim(-0.3, 4.2)
    ax.set_ylim(-3.5, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    title(ax, "adjacency list: V + 2E = 12 cells")

    ax = axes[2]
    size = len(nodes)
    for i, a in enumerate(nodes):
        ax.text(-0.5, -i + 0.5, a, ha="center", va="center", fontsize=11, color=AMBER)
        ax.text(i + 0.5, 1.3, a, ha="center", va="center", fontsize=11, color=AMBER)
        for j, b in enumerate(nodes):
            on = m.has_edge(a, b)
            ax.add_patch(Rectangle((j, -i), 1, 0.7 + 0.3, facecolor=DONE if on else "white",
                                   edgecolor=MUTED))
            ax.text(j + 0.5, -i + 0.5, "1" if on else "0", ha="center", va="center",
                    fontsize=11, color=SLATE if on else MUTED)
    ax.set_xlim(-1.0, size + 0.3)
    ax.set_ylim(-size + 0.7, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    title(ax, "adjacency matrix: V² = 16 cells")
    fig.suptitle("One graph, two representations", fontsize=12.5, fontweight="bold",
                 color=SLATE)
    fig.tight_layout()
    return base.save(fig, "representations")


# -- BFS -----------------------------------------------------------------------


def figure_bfs_snapshots():
    """Four moments of bfs(G, "A"), recomputed step by step with the course queue."""
    from dsa.graph import Graph, bfs

    g = build(Graph, G_EDGES)
    order = bfs(g, "A")
    # Replay the algorithm to recover the queue after each dequeue.
    states = []
    queue, seen, taken = ["A"], {"A"}, []
    while queue:
        node = queue.pop(0)
        taken.append(node)
        for other in g.neighbours(node):
            if other not in seen:
                seen.add(other)
                queue.append(other)
        states.append((list(taken), list(queue)))
    assert taken == order
    fig, axes = plt.subplots(1, 4, figsize=(13.4, 3.3))
    for ax, step in zip(axes, [0, 1, 3, 5]):
        done, waiting = states[step]
        fills = {n: DONE for n in done}
        fills.update({n: HILITE for n in waiting})
        fills[done[-1]] = AMBER
        draw(ax, G_EDGES, G_POS, fills=fills, node_size=620, font_size=10)
        ax.text(2, -1.5, "queue: " + (" ".join(waiting) if waiting else "empty"),
                ha="center", fontsize=10, color=SLATE, family="monospace")
        pad(ax, dy=0.55)
        title(ax, f"take {done[-1]}; order so far {''.join(done)}", 10.5)
    fig.suptitle("BFS from A: taken now (amber), done (green), waiting in the queue "
                 "(yellow)", fontsize=12, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "bfs-snapshots")


def figure_bfs_tree():
    """Layers and parent pointers, from the reference shortest_path_unweighted."""
    from dsa.graph import Graph, bfs, shortest_path_unweighted

    g = build(Graph, G_EDGES)
    order = bfs(g, "A")
    distance, parent = {"A": 0}, {"A": None}
    for node in order:                      # parents in BFS order: first discoverer
        for other in g.neighbours(node):
            if other not in distance:
                distance[other] = distance[node] + 1
                parent[other] = node
    path = shortest_path_unweighted(g, "A", "G")
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 3.9))
    ax = axes[0]
    layer_fill = [HILITE, FILL, DONE, "#E6D6EC", "#F6C9C4"]
    draw(ax, G_EDGES, G_POS, fills={n: layer_fill[d] for n, d in distance.items()})
    for layer in range(5):
        xs = [G_POS[n][0] for n, d in distance.items() if d == layer]
        ax.text(xs[0], -1.4, f"layer {layer}", ha="center", fontsize=9.5, color=AMBER)
    pad(ax, dy=0.5)
    title(ax, "distance from A = the layer BFS finds it in")

    ax = axes[1]
    tree = [(parent[n], n) for n in order if parent[n] is not None]
    on_path = {(path[i], path[i + 1]) for i in range(len(path) - 1)}
    draw(ax, [e for e in G_EDGES], G_POS, edge_colours={frozenset(e): "#D9DDDE" for e in G_EDGES},
         fills={n: (HILITE if n in path else FILL) for n in G_POS})
    graph = nx.DiGraph()
    graph.add_edges_from((child, par) for par, child in tree)
    nx.draw_networkx_edges(graph, G_POS, ax=ax, arrows=True, arrowstyle="-|>", arrowsize=16,
                           node_size=760, width=[3.0 if (p, c) in on_path else 1.6
                                                 for c, p in graph.edges()],
                           edge_color=[AMBER if (p, c) in on_path else SLATE
                                       for c, p in graph.edges()])
    ax.text(2, -1.5, "path = " + " → ".join(path) + f"   ({len(path) - 1} edges)",
            ha="center", fontsize=10, color=SLATE)
    pad(ax, dy=0.55)
    title(ax, "parent pointers; walk them back from G, then reverse")
    fig.suptitle("BFS finds shortest paths by edge count", fontsize=12.5,
                 fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "bfs-tree")


# -- DFS -----------------------------------------------------------------------


def figure_dfs_vs_bfs():
    from dsa.graph import Graph, bfs, dfs

    g = build(Graph, G_EDGES)
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 3.7))
    for ax, name, order, colour in [(axes[0], "bfs", bfs(g, "A"), HILITE),
                                    (axes[1], "dfs", dfs(g, "A"), DONE)]:
        rank = {n: i + 1 for i, n in enumerate(order)}
        draw(ax, G_EDGES, G_POS, fills={n: colour for n in G_POS},
             labels={n: f"{n}\n{rank[n]}" for n in G_POS}, font_size=9.5)
        ax.text(2, -1.45, f"{name}(g, 'A') = " + " ".join(order), ha="center",
                fontsize=10, color=SLATE, family="monospace")
        pad(ax, dy=0.5)
        title(ax, "breadth first: a queue — rings round A" if name == "bfs"
              else "depth first: a stack — one path to its end, then back up")
    fig.suptitle("Same graph, same start, different order: the number is the visit order",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "dfs-vs-bfs")


# -- cycles --------------------------------------------------------------------


def figure_cycles():
    from dsa.graph import Graph, has_cycle

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.7))

    ax = axes[0]
    tree = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")]
    pos = {"A": (1, 1), "B": (0.4, 0.2), "C": (1.6, 0.2), "D": (0, -0.6), "E": (0.8, -0.6)}
    assert not has_cycle(build(Graph, tree))
    draw(ax, tree, pos, fills={"A": DONE, "B": AMBER},
         edge_colours={frozenset(("A", "B")): AMBER}, widths={frozenset(("A", "B")): 3.0})
    ax.text(1.0, -1.2, "at B, neighbour A is visited —\nbut it is B's parent: not a cycle",
            ha="center", fontsize=9, color=SLATE)
    pad(ax, dy=0.5)
    title(ax, "undirected: skip the edge you came in by")

    ax = axes[1]
    diamond = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    pos = {"A": (0, 0), "B": (1, 0.7), "C": (1, -0.7), "D": (2, 0)}
    assert not has_cycle(build(Graph, diamond, directed=True))
    draw(ax, diamond, pos, directed=True,
         fills={"A": GREY_NODE, "C": GREY_NODE, "B": SLATE, "D": SLATE},
         labels={"A": "A", "B": "B", "C": "C", "D": "D"})
    for n in ("B", "D"):
        x, y = pos[n]
        ax.text(x, y, n, ha="center", va="center", fontsize=11, color="white")
    ax.text(1.0, -1.35, "reaching D again from C: D is black\n(finished) — a diamond, not a cycle",
            ha="center", fontsize=9, color=SLATE)
    pad(ax, dy=0.55)
    title(ax, "directed: visited is not enough")

    ax = axes[2]
    loop = [("A", "B"), ("B", "C"), ("C", "A")]
    pos = {"A": (0, 0.6), "B": (1.2, 0.6), "C": (0.6, -0.4)}
    assert has_cycle(build(Graph, loop, directed=True))
    draw(ax, loop, pos, directed=True, fills={n: GREY_NODE for n in pos},
         edge_colours={("C", "A"): RED}, widths={("C", "A"): 3.0})
    ax.text(0.6, -1.15, "C → A reaches a grey node: A is still on\nthe current path — a cycle",
            ha="center", fontsize=9, color=SLATE)
    pad(ax, dy=0.55)
    title(ax, "grey = on the path now: a cycle")
    fig.suptitle("Cycle detection: white (unseen), grey (on the path), black (finished)",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "cycles")


# -- topological sort ----------------------------------------------------------


def figure_prerequisites():
    import graphviz

    from dsa.graph import Graph, has_cycle, topological_sort

    g = build(Graph, PREREQUISITES, directed=True)
    assert not has_cycle(g)
    order = topological_sort(g)
    rank = {course: i + 1 for i, course in enumerate(order)}
    dot = graphviz.Digraph()
    dot.attr(rankdir="LR", nodesep="0.25", ranksep="0.55")
    dot.attr("node", shape="box", style="rounded,filled", fontname="DejaVu Sans",
             fontsize="10", color=SLATE, fillcolor=FILL, fontcolor=SLATE)
    dot.attr("edge", color=SLATE, arrowsize="0.7")
    for course in g.nodes():
        fill = HILITE if course == "IS122" else FILL
        dot.node(course, label=f"{rank[course]}. {course}\n{COURSE_NAMES[course]}",
                 fillcolor=fill)
    for source, target in g.edges():
        dot.edge(source, target)
    dot.attr(label="Software Engineering bylaw (2013): an arrow X → Y means X is a "
             "prerequisite of Y.\nThe number is the position in topological_sort(g).",
             fontname="DejaVu Sans", fontsize="11", fontcolor=SLATE, labelloc="b")
    return base.save_dot(dot, "prerequisites")


# -- the maze ------------------------------------------------------------------


def maze_graph():
    from dsa.graph import Graph

    g = Graph()
    rows, cols = len(MAZE), len(MAZE[0])
    start = goal = None
    for r in range(rows):
        for c in range(cols):
            if MAZE[r][c] == "#":
                continue
            g.add_node((r, c))
            if MAZE[r][c] == "S":
                start = (r, c)
            if MAZE[r][c] == "T":
                goal = (r, c)
            for dr, dc in ((0, 1), (1, 0)):          # right and down; undirected
                rr, cc = r + dr, c + dc
                if rr < rows and cc < cols and MAZE[rr][cc] != "#":
                    g.add_edge((r, c), (rr, cc))
    return g, start, goal


def figure_maze():
    from dsa.graph import bfs, shortest_path_unweighted

    g, start, goal = maze_graph()
    path = shortest_path_unweighted(g, start, goal)
    distance = {start: 0}
    for cell in bfs(g, start):
        for other in g.neighbours(cell):
            if other not in distance:
                distance[other] = distance[cell] + 1
    rows, cols = len(MAZE), len(MAZE[0])
    fig, ax = plt.subplots(figsize=(8.2, 6.4))
    on_path = set(path)
    for r in range(rows):
        for c in range(cols):
            y = rows - 1 - r
            if MAZE[r][c] == "#":
                ax.add_patch(Rectangle((c, y), 1, 1, facecolor=WALL, edgecolor="white"))
                continue
            fill = HILITE if (r, c) in on_path else "white"
            ax.add_patch(Rectangle((c, y), 1, 1, facecolor=fill, edgecolor="#D0D5D6"))
            text = MAZE[r][c] if MAZE[r][c] in "ST" else str(distance[(r, c)])
            ax.text(c + 0.5, y + 0.5, text, ha="center", va="center",
                    fontsize=13 if MAZE[r][c] in "ST" else 11,
                    fontweight="bold" if (r, c) in on_path else "normal",
                    color=AMBER if MAZE[r][c] in "ST" else SLATE)
    xs = [c + 0.5 for r, c in path]
    ys = [rows - 1 - r + 0.5 for r, c in path]
    ax.plot(xs, ys, color=AMBER, linewidth=2.2, alpha=0.8)
    ax.set_xlim(-0.1, cols + 0.1)
    ax.set_ylim(-1.1, rows + 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(cols / 2, -0.6, f"{len(g)} open cells = {len(g)} vertices, {len(g.edges())} edges;"
            f" shortest route S → T: {len(path) - 1} steps", ha="center", fontsize=10.5,
            color=SLATE)
    ax.set_title("A maze is a graph: each number is BFS's distance from S",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    print(f"    maze: {len(g)} cells, {len(g.edges())} edges, path of {len(path) - 1} steps")
    return base.save(fig, "maze")


# -- measured ------------------------------------------------------------------


def random_graph(cls, n, edges, seed):
    """A connected-ish random undirected graph with `edges` distinct edges."""
    rng = random.Random(seed)
    g = cls()
    for node in range(n):
        g.add_node(node)
    seen = set()
    for node in range(1, n):                 # a spanning path keeps it connected
        other = rng.randrange(node)
        g.add_edge(node, other)
        seen.add((min(node, other), max(node, other)))
    while len(seen) < edges:
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and (min(a, b), max(a, b)) not in seen:
            seen.add((min(a, b), max(a, b)))
            g.add_edge(a, b)
    return g


def figure_measured():
    from dsa.graph import Graph, MatrixGraph, bfs
    from viz.complexity import measure

    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.4))

    # left: memory — cells actually stored, sparse graph with E = 2V
    ax = axes[0]
    sizes = [100, 200, 400, 800, 1600]
    cells = {"list": [], "matrix": []}
    for n in sizes:
        g = random_graph(Graph, n, 2 * n, seed=n)
        m = random_graph(MatrixGraph, n, 2 * n, seed=n)
        cells["list"].append(len(g) + sum(g.degree(v) for v in g.nodes()))
        cells["matrix"].append(sum(len(row) for row in m._matrix))
    ax.plot(sizes, cells["list"], "o-", color=GREEN, lw=2.1, label="adjacency list: V + 2E")
    ax.plot(sizes, cells["matrix"], "o-", color=RED, lw=2.1, label="adjacency matrix: V²")
    ax.set_ylabel("cells stored (log scale)")
    ax.set_title("memory, sparse graph (E = 2V)", fontsize=11, color=SLATE)
    print("    cells", cells)

    # middle: one BFS over a sparse graph
    ax = axes[1]
    sizes = [250, 500, 1000, 2000]
    cache = {}

    def graph_for(cls, n):
        if (cls, n) not in cache:
            cache[(cls, n)] = random_graph(cls, n, 2 * n, seed=n)
        return cache[(cls, n)]

    times = {}
    for label, cls, colour in [("adjacency list", Graph, GREEN),
                               ("adjacency matrix", MatrixGraph, RED)]:
        measured, seconds = measure(lambda g: bfs(g, 0), sizes,
                                    lambda n, cls=cls: graph_for(cls, n), repeat=3)
        times[label] = seconds
        ax.plot(measured, [s * 1e3 for s in seconds], "o-", color=colour, lw=2.1,
                label=label)
    ax.set_ylabel("milliseconds per BFS (log scale)")
    ax.set_title("one BFS, sparse graph (E = 2V)", fontsize=11, color=SLATE)
    print("    bfs ms", {k: [round(s * 1e3, 2) for s in v] for k, v in times.items()})

    # right: has_edge on a dense graph (every node joined to about half the rest)
    ax = axes[2]
    sizes = [100, 200, 400, 800]
    rng = random.Random(14)
    queries = 2000
    dense_times = {}
    for label, cls, colour in [("adjacency list", Graph, GREEN),
                               ("adjacency matrix", MatrixGraph, RED)]:
        per_query = []
        for n in sizes:
            g = random_graph(cls, n, n * (n - 1) // 4, seed=n)
            pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(queries)]

            def ask(payload, g=g):
                for a, b in payload:
                    g.has_edge(a, b)
            _, seconds = measure(ask, [n], lambda _n, pairs=pairs: pairs, repeat=3)
            per_query.append(seconds[0] / queries * 1e6)
        dense_times[label] = per_query
        ax.plot(sizes, per_query, "o-", color=colour, lw=2.1, label=label)
    ax.set_ylabel("microseconds per has_edge (log scale)")
    ax.set_title("has_edge, dense graph (E ≈ V²/4)", fontsize=11, color=SLATE)
    print("    has_edge us", {k: [round(v, 2) for v in vals] for k, vals in dense_times.items()})

    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_xlabel("V, number of vertices (log scale)")
        ax.grid(True, alpha=0.25, linewidth=0.7)
        ax.legend(frameon=False, fontsize=8.5, loc="upper left")
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    fig.suptitle("Measured: sparse graphs want the list; a dense graph asked "
                 "\"is there an edge?\" wants the matrix", fontsize=12, fontweight="bold",
                 color=SLATE)
    fig.tight_layout()
    return base.save(fig, "measured")


FIGURES = [figure_vocabulary, figure_components, figure_representations,
           figure_bfs_snapshots, figure_bfs_tree, figure_dfs_vs_bfs, figure_cycles,
           figure_prerequisites, figure_maze, figure_measured]


def main():
    from dsa import graph

    try:
        graph.bfs(build(graph.Graph, [("A", "B")]), "A")
    except NotImplementedError:
        print("dsa/graph.py (or the hash map, queue or stack under it) is not "
              "implemented yet.\nRun: python tools/with_solutions.py tools/figures_l14.py")
        return
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
