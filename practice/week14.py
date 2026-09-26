"""Question bank, Week 14 — graphs and graph searches. Problems W14-C1 to W14-C5.

Questions:  docs/question-bank/week14-questions.md
Tests:      tests/test_practice_week14.py

Use your own structures as the working storage — `Graph` from `dsa/graph.py`,
`ChainingHashMap` from `dsa/hashmap.py` for visited sets and counts,
`CircularQueue` from `dsa/queue.py` and `Stack` from `dsa/stack.py` — not a
Python dict, set or `collections.deque`. Lists are fine as inputs and results.
"""

from dsa.graph import Graph  # noqa: F401  (your Week 14 exercise)
from dsa.hashmap import ChainingHashMap  # noqa: F401  (your Week 13 exercise)
from dsa.queue import CircularQueue  # noqa: F401  (your Week 7 exercise)
from dsa.stack import Stack  # noqa: F401  (your Week 6 exercise)


def maze_distance(maze):
    """W14-C1. The fewest steps from S to T in a maze, or -1 if T is unreachable.

    `maze` is a list of equal-length strings: "S" the start, "T" the target,
    "#" a wall, "." an open cell. A step moves up, down, left or right to an
    open cell (S and T are open).

    maze_distance(["S.#",
                   ".##",
                   "..T"])  -> 4
    maze_distance(["S#T"])  -> -1

    O(R * C): a BFS from S over the cells. You may build a `Graph` of the open
    cells first, or search the grid directly.
    """
    raise NotImplementedError


def is_bipartite(graph):
    """W14-C2. True when the vertices of an undirected graph can be coloured
    with two colours so that every edge joins two different colours.

    A square A-B-C-D-A -> True; a triangle A-B-C-A -> False; a graph with no
    edges -> True. The graph may have several components.

    O(V + E): BFS from every uncoloured vertex, giving each neighbour the
    other colour; a neighbour that already has the SAME colour means no.
    """
    raise NotImplementedError


def topological_order_dfs(graph):
    """W14-C3. A topological order of a directed graph, by depth-first search,
    or None when the graph has a cycle.

    Colour every vertex white; run a DFS from each white vertex, in
    `graph.nodes()` order. A vertex turns grey when entered and black when all
    its neighbours are finished; record it when it turns black. The reverse of
    that finishing order is the answer. Meeting a grey neighbour means a cycle.

    For A -> B, A -> C, B -> D, C -> D (added in that order):
    topological_order_dfs(g) -> ["A", "C", "B", "D"]

    O(V + E). Not Kahn's algorithm — that is `topological_sort` in dsa/graph.py.
    """
    raise NotImplementedError


def semester_plan(prerequisites):
    """W14-C4. Group courses into the fewest semesters, taking a course as soon
    as all its prerequisites are done.

    `prerequisites` is a list of (before, after) pairs: "before" must be
    passed first. Return a list of semesters, each a list of course codes in
    alphabetical order; or None when the prerequisites contain a cycle.

    semester_plan([("CS012", "IS122"), ("MATH012", "IS122"),
                   ("IS122", "IS123")])
        -> [["CS012", "MATH012"], ["IS122"], ["IS123"]]
    semester_plan([]) -> []

    O(V + E) plus the sorting of each semester: Kahn's algorithm, one layer
    at a time.
    """
    raise NotImplementedError


def count_islands(grid):
    """W14-C5. The number of islands in a grid of "1" (land) and "0" (water).

    Land cells joined up, down, left or right belong to the same island;
    diagonals do not join.

    count_islands(["110",
                   "010",
                   "001"])  -> 2
    count_islands([])       -> 0

    O(R * C): connected components — start a search from every land cell not
    yet seen.
    """
    raise NotImplementedError
