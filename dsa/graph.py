"""Graphs, and the two searches that walk them.

A graph is just nodes and the edges between them — the most general structure
in the course. A linked list is a graph. A tree is a graph. A road network, a
social network, a dependency graph and a maze are all the same thing wearing
different clothes, which is why this is the last structure we build.

Two representations, deliberately paired so you can measure the trade-off
yourself, the way `SlowQueue` and `CircularQueue` are paired in `dsa/queue.py`:

    Graph        adjacency list    O(V + E) space   neighbours in O(degree)
    MatrixGraph  adjacency matrix  O(V^2) space     has_edge in O(1)

Sparse graph? The list wins, usually by a lot. Dense graph, or you ask
"is there an edge?" constantly? The matrix earns its space.

Declared in the bylaw: "graphs" and "graph searches" (CS2101, AI 2020 p. 44;
IS122, SWE 2013 p. 38 and Medical Informatics 2014 p. 35).

Neither representation uses Python's `dict`, `list` or `set` for storage: the
adjacency list is your own `ChainingHashMap` (Week 13) from each node to a
`DynamicArray` (Week 4) of its neighbours, and the matrix is a `DynamicArray` of
rows. The searches follow the same rule for their working storage — your
`CircularQueue` for BFS, your `Stack` for iterative DFS, your hash map for the
set of visited nodes. Lists are only for handing results back.

Draw one:

    from viz.draw import draw_graph
    draw_graph(to_networkx(g), highlight_nodes=bfs(g, "A"))
"""

from __future__ import annotations

from dsa.dynamic_array import DynamicArray
from dsa.hashmap import ChainingHashMap


def to_networkx(graph):
    """Convert to a networkx graph for `viz.draw.draw_graph`.

    Given to you — the conversion is plumbing, not the lesson.
    """
    import networkx as nx

    result = nx.DiGraph() if graph.directed else nx.Graph()
    result.add_nodes_from(graph.nodes())
    result.add_edges_from(graph.edges())
    return result


class Graph:
    """Adjacency list: a mapping from each node to the nodes it reaches.

    The mapping is your own `ChainingHashMap`; each value is a `DynamicArray`
    of neighbours, in the order the edges were added.
    """

    def __init__(self, directed=False):
        self.directed = directed
        self._adjacent = ChainingHashMap()   # node -> DynamicArray of nodes

    def add_node(self, node):
        """Add an isolated node. Adding one twice must not wipe its edges.

        Target: O(1).
        """
        raise NotImplementedError

    def add_edge(self, source, target):
        """Connect two nodes, adding either if it is missing. Target: O(1).

        In an undirected graph this records the edge in **both** directions.
        """
        raise NotImplementedError

    def neighbours(self, node):
        """The nodes reachable from `node` in one step, as a list.

        Raises KeyError when the node is not in the graph.
        Target: O(degree).
        """
        raise NotImplementedError

    def has_edge(self, source, target):
        """True when an edge runs from source to target. Target: O(degree)."""
        raise NotImplementedError

    def nodes(self):
        """All nodes, as a list. Target: O(V)."""
        raise NotImplementedError

    def edges(self):
        """All edges as (source, target) pairs. Target: O(V + E).

        In an undirected graph report each edge **once**, not once per
        direction.
        """
        raise NotImplementedError

    def degree(self, node):
        """How many edges leave `node`. Target: O(1) or O(degree)."""
        raise NotImplementedError

    def __len__(self):
        return len(self._adjacent)

    def __contains__(self, node):
        return node in self._adjacent

    def __repr__(self):
        kind = "directed" if self.directed else "undirected"
        return f"Graph({kind}, {len(self._adjacent)} nodes)"


class MatrixGraph:
    """Adjacency matrix: a V x V grid of booleans.

    Same contract as `Graph`, so the tests run against both. O(1) to ask
    whether an edge exists; O(V^2) memory whether you use it or not.
    """

    def __init__(self, directed=False):
        self.directed = directed
        self._index = ChainingHashMap()   # node -> row/column number
        self._order = DynamicArray()      # row/column number -> node
        self._matrix = DynamicArray()     # one DynamicArray of bools per row

    def add_node(self, node):
        """Add a node, growing the matrix by one row and one column. O(V)."""
        raise NotImplementedError

    def add_edge(self, source, target):
        """Set the cell (and its mirror, when undirected). O(1) after lookup."""
        raise NotImplementedError

    def neighbours(self, node):
        """Scan the node's row. Target: **O(V)** — this is the cost of the
        matrix, and the reason traversals are slower on it.
        """
        raise NotImplementedError

    def has_edge(self, source, target):
        """One cell lookup. Target: **O(1)** — this is the matrix's prize."""
        raise NotImplementedError

    def nodes(self):
        """All nodes, as a list. Target: O(V)."""
        raise NotImplementedError

    def edges(self):
        """All edges as (source, target) pairs, each once. Target: O(V^2)."""
        raise NotImplementedError

    def degree(self, node):
        """How many edges leave `node`. Target: O(V)."""
        raise NotImplementedError

    def __len__(self):
        return len(self._order)

    def __contains__(self, node):
        return node in self._index

    def __repr__(self):
        kind = "directed" if self.directed else "undirected"
        return f"MatrixGraph({kind}, {len(self._order)} nodes)"


# -- the searches ---------------------------------------------------------
# Both work on either representation: they only ever call .neighbours().


def bfs(graph, start):
    """Breadth-first: visit `start`, then everything one step away, and so on.

    Returns the nodes in visit order, as a list. Target: O(V + E).

    Needs a **queue**. Because it expands in rings, the first time it reaches a
    node it has arrived by a shortest path — which `shortest_path_unweighted`
    below depends on.
    """
    raise NotImplementedError


def dfs(graph, start):
    """Depth-first, recursively: follow one path to its end, then back up.

    Returns the nodes in visit order, as a list. Target: O(V + E).

    Visit neighbours in the order `graph.neighbours()` returns them. The call
    stack is doing the bookkeeping for you here — that is the whole difference
    from the next function.
    """
    raise NotImplementedError


def dfs_iterative(graph, start):
    """The same walk, with your own stack instead of the call stack.

    Returns the nodes in visit order, as a list. Target: O(V + E).

    Worth writing because it shows what recursion *was* doing, and because it
    survives graphs deeper than Python's recursion limit. To match `dfs`
    exactly, push neighbours in reverse so the first one comes off first.
    """
    raise NotImplementedError


def shortest_path_unweighted(graph, start, goal):
    """A shortest path from start to goal, as a list of nodes.

    Returns [start, ..., goal], or None when goal is unreachable.
    shortest_path_unweighted(g, "A", "A") -> ["A"]. Target: O(V + E).

    BFS, but remember which node you came from, then walk those links
    backwards. "Shortest" means fewest edges — no weights in this course.
    """
    raise NotImplementedError


def connected_components(graph):
    """Group the nodes of an undirected graph into connected sets.

    Returns a list of lists. Target: O(V + E).

    Start a search from every node not yet seen; each search gives one
    component.
    """
    raise NotImplementedError


def has_cycle(graph):
    """True when the graph contains a cycle. Target: O(V + E).

    The two cases genuinely differ:
      * undirected — a visited neighbour that is not the node you came from
      * directed   — a node currently on the recursion stack (grey), which is
                     not the same as merely visited (black)
    """
    raise NotImplementedError


def topological_sort(graph):
    """Order a directed acyclic graph so every edge points forwards.

    Returns a list of nodes, or None when the graph has a cycle (no valid
    order exists). Target: O(V + E).

    This is what resolves build dependencies, course prerequisites and package
    installs. Any valid order is accepted.
    """
    raise NotImplementedError
