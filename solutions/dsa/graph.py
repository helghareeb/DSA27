"""SOLUTION — try the exercise in `dsa/graph.py` first; see `solutions/README.md`.

Graphs, and the two searches that walk them.

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
from dsa.queue import CircularQueue
from dsa.stack import Stack

# The three colours of the directed cycle check. WHITE is "not in the map".
WHITE, GREY, BLACK = 0, 1, 2


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
    of neighbours, in the order the edges were added. A hash map hands its keys
    back in bucket order, which changes from run to run for strings, so the
    nodes are also kept in `_order`, in the order they were added: that makes
    `nodes()`, and every search that loops over it, give the same answer every
    time.
    """

    def __init__(self, directed=False):
        self.directed = directed
        self._adjacent = ChainingHashMap()   # node -> DynamicArray of nodes
        self._order = DynamicArray()         # nodes, in the order they were added

    def add_node(self, node):
        """Add an isolated node. Adding one twice must not wipe its edges.

        Target: O(1).
        """
        if node not in self._adjacent:               # the guard is the whole trap
            self._adjacent.put(node, DynamicArray())
            self._order.append(node)

    def add_edge(self, source, target):
        """Connect two nodes, adding either if it is missing. Target: O(1).

        In an undirected graph this records the edge in **both** directions.
        """
        self.add_node(source)
        self.add_node(target)
        self._adjacent.get(source).append(target)
        if not self.directed and source != target:   # a loop is recorded once
            self._adjacent.get(target).append(source)

    def neighbours(self, node):
        """The nodes reachable from `node` in one step, as a list.

        Raises KeyError when the node is not in the graph.
        Target: O(degree).
        """
        return list(self._adjacent.get(node))        # get raises KeyError

    def has_edge(self, source, target):
        """True when an edge runs from source to target. Target: O(degree)."""
        if source not in self._adjacent:
            return False
        for node in self._adjacent.get(source):
            if node == target:
                return True
        return False

    def nodes(self):
        """All nodes, as a list, in the order they were added. Target: O(V)."""
        return list(self._order)

    def edges(self):
        """All edges as (source, target) pairs. Target: O(V + E).

        In an undirected graph report each edge **once**, not once per
        direction.
        """
        result = []
        done = ChainingHashMap()                     # nodes whose edges are reported
        for node in self._order:
            for neighbour in self._adjacent.get(node):
                if self.directed or neighbour not in done:
                    result.append((node, neighbour))
            done.put(node, True)
        return result

    def degree(self, node):
        """How many edges leave `node`. Target: O(1) or O(degree)."""
        return len(self._adjacent.get(node))

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
        if node in self._index:
            return
        self._index.put(node, len(self._order))
        self._order.append(node)
        for row in self._matrix:                     # one new column ...
            row.append(False)
        row = DynamicArray()                         # ... and one new row
        for _ in range(len(self._order)):
            row.append(False)
        self._matrix.append(row)

    def add_edge(self, source, target):
        """Set the cell (and its mirror, when undirected). O(1) after lookup."""
        self.add_node(source)
        self.add_node(target)
        i, j = self._index.get(source), self._index.get(target)
        self._matrix[i][j] = True
        if not self.directed:
            self._matrix[j][i] = True

    def neighbours(self, node):
        """Scan the node's row. Target: **O(V)** — this is the cost of the
        matrix, and the reason traversals are slower on it.
        """
        row = self._matrix[self._index.get(node)]    # get raises KeyError
        return [self._order[j] for j in range(len(row)) if row[j]]

    def has_edge(self, source, target):
        """One cell lookup. Target: **O(1)** — this is the matrix's prize."""
        if source not in self._index or target not in self._index:
            return False
        return self._matrix[self._index.get(source)][self._index.get(target)]

    def nodes(self):
        """All nodes, as a list, in the order they were added. Target: O(V)."""
        return list(self._order)

    def edges(self):
        """All edges as (source, target) pairs, each once. Target: O(V^2)."""
        result = []
        size = len(self._order)
        for i in range(size):
            first = 0 if self.directed else i        # undirected: upper triangle only
            for j in range(first, size):
                if self._matrix[i][j]:
                    result.append((self._order[i], self._order[j]))
        return result

    def degree(self, node):
        """How many edges leave `node`. Target: O(V)."""
        count = 0
        for cell in self._matrix[self._index.get(node)]:
            if cell:
                count += 1
        return count

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
    order = []
    visited = ChainingHashMap()
    queue = CircularQueue()
    visited.put(start, True)
    queue.enqueue(start)
    while not queue.is_empty():
        node = queue.dequeue()
        order.append(node)
        for neighbour in graph.neighbours(node):
            if neighbour not in visited:
                visited.put(neighbour, True)         # mark when queued, not when taken
                queue.enqueue(neighbour)
    return order


def dfs(graph, start):
    """Depth-first, recursively: follow one path to its end, then back up.

    Returns the nodes in visit order, as a list. Target: O(V + E).

    Visit neighbours in the order `graph.neighbours()` returns them. The call
    stack is doing the bookkeeping for you here — that is the whole difference
    from the next function.
    """
    order = []
    _dfs_visit(graph, start, ChainingHashMap(), order)
    return order


def _dfs_visit(graph, node, visited, order):
    visited.put(node, True)
    order.append(node)
    for neighbour in graph.neighbours(node):
        if neighbour not in visited:
            _dfs_visit(graph, neighbour, visited, order)


def dfs_iterative(graph, start):
    """The same walk, with your own stack instead of the call stack.

    Returns the nodes in visit order, as a list. Target: O(V + E).

    Worth writing because it shows what recursion *was* doing, and because it
    survives graphs deeper than Python's recursion limit. To match `dfs`
    exactly, push neighbours in reverse so the first one comes off first.
    """
    order = []
    visited = ChainingHashMap()
    stack = Stack()
    stack.push(start)
    while not stack.is_empty():
        node = stack.pop()
        if node in visited:                          # pushed twice; the first pop won
            continue
        visited.put(node, True)                      # mark when taken, not when pushed
        order.append(node)
        neighbours = graph.neighbours(node)
        for i in range(len(neighbours) - 1, -1, -1):
            if neighbours[i] not in visited:
                stack.push(neighbours[i])
    return order


def shortest_path_unweighted(graph, start, goal):
    """A shortest path from start to goal, as a list of nodes.

    Returns [start, ..., goal], or None when goal is unreachable.
    shortest_path_unweighted(g, "A", "A") -> ["A"]. Target: O(V + E).

    BFS, but remember which node you came from, then walk those links
    backwards. "Shortest" means fewest edges — no weights in this course.
    """
    parent = ChainingHashMap()                       # node -> the node it was reached from
    queue = CircularQueue()
    parent.put(start, None)
    queue.enqueue(start)
    while not queue.is_empty():
        node = queue.dequeue()
        if node == goal:
            path = []
            while node is not None:                  # walk the links back to start
                path.append(node)
                node = parent.get(node)
            path.reverse()
            return path
        for neighbour in graph.neighbours(node):
            if neighbour not in parent:              # the parent map is the visited set
                parent.put(neighbour, node)
                queue.enqueue(neighbour)
    return None


def connected_components(graph):
    """Group the nodes of an undirected graph into connected sets.

    Returns a list of lists. Target: O(V + E).

    Start a search from every node not yet seen; each search gives one
    component.
    """
    seen = ChainingHashMap()
    components = []
    for node in graph.nodes():
        if node not in seen:
            component = bfs(graph, node)
            for member in component:
                seen.put(member, True)
            components.append(component)
    return components


def has_cycle(graph):
    """True when the graph contains a cycle. Target: O(V + E).

    The two cases genuinely differ:
      * undirected — a visited neighbour that is not the node you came from
      * directed   — a node currently on the recursion stack (grey), which is
                     not the same as merely visited (black)
    """
    if graph.directed:
        colour = ChainingHashMap()                   # absent means WHITE
        for node in graph.nodes():
            if colour.get(node, WHITE) == WHITE and _directed_cycle_from(graph, node, colour):
                return True
        return False
    visited = ChainingHashMap()
    for node in graph.nodes():
        if node not in visited and _undirected_cycle_from(graph, node, None, visited):
            return True
    return False


def _undirected_cycle_from(graph, node, parent, visited):
    visited.put(node, True)
    for neighbour in graph.neighbours(node):
        if neighbour not in visited:
            if _undirected_cycle_from(graph, neighbour, node, visited):
                return True
        elif neighbour != parent:                    # seen, and not the way we came
            return True
    return False


def _directed_cycle_from(graph, node, colour):
    colour.put(node, GREY)                           # on the current path
    for neighbour in graph.neighbours(node):
        state = colour.get(neighbour, WHITE)
        if state == GREY:                            # an edge back into the path
            return True
        if state == WHITE and _directed_cycle_from(graph, neighbour, colour):
            return True
    colour.put(node, BLACK)                          # finished: off the path for good
    return False


def topological_sort(graph):
    """Order a directed acyclic graph so every edge points forwards.

    Returns a list of nodes, or None when the graph has a cycle (no valid
    order exists). Target: O(V + E).

    This is what resolves build dependencies, course prerequisites and package
    installs. Any valid order is accepted. Raises ValueError on an undirected
    graph, where "forwards" means nothing.

    Kahn's algorithm: repeatedly take a node that nothing still points at.
    """
    if not graph.directed:
        raise ValueError("topological order needs a directed graph")
    in_degree = ChainingHashMap()                    # node -> edges still pointing at it
    for node in graph.nodes():
        in_degree.put(node, 0)
    for node in graph.nodes():
        for neighbour in graph.neighbours(node):
            in_degree.put(neighbour, in_degree.get(neighbour) + 1)
    ready = CircularQueue()
    for node in graph.nodes():
        if in_degree.get(node) == 0:
            ready.enqueue(node)
    order = []
    while not ready.is_empty():
        node = ready.dequeue()
        order.append(node)
        for neighbour in graph.neighbours(node):
            remaining = in_degree.get(neighbour) - 1
            in_degree.put(neighbour, remaining)
            if remaining == 0:
                ready.enqueue(neighbour)
    if len(order) < len(graph):                      # the rest wait on each other: a cycle
        return None
    return order
