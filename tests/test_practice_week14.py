"""Question bank, Week 14 practice. Fail until `practice/week14.py` is written."""

import pytest

from dsa.graph import Graph
from practice.week14 import (count_islands, is_bipartite, maze_distance, semester_plan,
                             topological_order_dfs)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


def build(edges, directed=False, nodes=()):
    graph = Graph(directed=directed)
    for node in nodes:
        graph.add_node(node)
    for source, target in edges:
        graph.add_edge(source, target)
    return graph


# -- W14-C1 ---------------------------------------------------------------

@pytest.mark.parametrize(
    "maze,expected",
    [(["S.#", ".##", "..T"], 4), (["S#T"], -1), (["ST"], 1), (["S", ".", "T"], 2),
     (["S...", "###.", "T..."], 8), (["S..", "#.#", "..T"], 4)],
)
def test_maze_distance(maze, expected):
    assert maze_distance(maze) == expected


def test_maze_distance_takes_the_short_way_round():
    """Two routes: 3 steps down the left, 17 round the right. A search that
    stops at the first route it finds may return 17."""
    maze = ["S.......",
            ".######.",
            ".######.",
            "T......."]
    assert maze_distance(maze) == 3


def test_maze_distance_on_a_large_open_grid():
    size = 200                            # 40,000 cells: O(R * C), not worse
    maze = ["S" + "." * (size - 1)] + ["." * size] * (size - 2) + ["." * (size - 1) + "T"]
    assert maze_distance(maze) == 2 * (size - 1)


# -- W14-C2 ---------------------------------------------------------------

def test_even_cycle_is_bipartite():
    assert is_bipartite(build([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]))


def test_odd_cycle_is_not_bipartite():
    assert not is_bipartite(build([("A", "B"), ("B", "C"), ("C", "A")]))


def test_graph_without_edges_is_bipartite():
    assert is_bipartite(build([], nodes=["A", "B", "C"]))


def test_bipartite_checks_every_component():
    """The first component is fine; the odd cycle is in the second."""
    graph = build([("A", "B"), ("B", "C"), ("X", "Y"), ("Y", "Z"), ("Z", "X")])
    assert not is_bipartite(graph)


def test_tree_is_bipartite():
    assert is_bipartite(build([("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")]))


# -- W14-C3 ---------------------------------------------------------------

def respects_every_edge(graph, order):
    position = {node: i for i, node in enumerate(order)}
    return sorted(order) == sorted(graph.nodes()) and all(
        position[a] < position[b] for a, b in graph.edges())


def test_topological_order_dfs_example():
    graph = build([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")], directed=True)
    assert topological_order_dfs(graph) == ["A", "C", "B", "D"]


def test_topological_order_dfs_is_valid():
    edges = [("CS012", "CS113"), ("CS012", "IS122"), ("MATH012", "IS122"), ("IS122", "IS123"),
             ("IS123", "IS142"), ("CS012", "IS142"), ("IS122", "SWE141"), ("SWE132", "SWE141")]
    graph = build(edges, directed=True, nodes=["ALONE"])
    assert respects_every_edge(graph, topological_order_dfs(graph))


def test_topological_order_dfs_finds_a_cycle():
    graph = build([("A", "B"), ("B", "C"), ("C", "A")], directed=True)
    assert topological_order_dfs(graph) is None


def test_topological_order_dfs_diamond_is_not_a_cycle():
    graph = build([("A", "B"), ("A", "C"), ("C", "B")], directed=True)
    assert respects_every_edge(graph, topological_order_dfs(graph))


# -- W14-C4 ---------------------------------------------------------------

def test_semester_plan_example():
    pairs = [("CS012", "IS122"), ("MATH012", "IS122"), ("IS122", "IS123")]
    assert semester_plan(pairs) == [["CS012", "MATH012"], ["IS122"], ["IS123"]]


def test_semester_plan_empty():
    assert semester_plan([]) == []


def test_semester_plan_takes_a_course_as_soon_as_it_can():
    """C needs only A, so it goes in semester 2 with B, not after B."""
    pairs = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    assert semester_plan(pairs) == [["A"], ["B", "C"], ["D"]]


def test_semester_plan_bylaw():
    pairs = [("CS012", "CS113"), ("CS012", "IS122"), ("MATH012", "IS122"),
             ("IS122", "IS123"), ("IS123", "IS142"), ("CS012", "IS142"),
             ("IT022", "IT131"), ("IS122", "IT131"), ("SWE021", "SWE132"),
             ("SWE132", "SWE141"), ("IS122", "SWE141"), ("SWE141", "SWE144")]
    assert semester_plan(pairs) == [
        ["CS012", "IT022", "MATH012", "SWE021"],
        ["CS113", "IS122", "SWE132"],
        ["IS123", "IT131", "SWE141"],
        ["IS142", "SWE144"],
    ]


def test_semester_plan_with_a_cycle_is_none():
    assert semester_plan([("A", "B"), ("B", "C"), ("C", "B")]) is None


# -- W14-C5 ---------------------------------------------------------------

@pytest.mark.parametrize(
    "grid,expected",
    [(["110", "010", "001"], 2), ([], 0), (["000"], 0), (["1"], 1), (["101", "010", "101"], 5),
     (["11000", "11000", "00100", "00011"], 3), (["111", "101", "111"], 1)],
)
def test_count_islands(grid, expected):
    assert count_islands(grid) == expected


def test_count_islands_on_a_large_grid():
    """A 300 x 300 checkerboard of 2 x 2 blocks: 90,000 cells to visit in
    O(R * C). Then one island 2,000 cells long, deeper than Python's recursion
    limit: a recursive flood fill raises RecursionError, a queue does not."""
    size = 300
    grid = ["".join("1" if (r // 2 + c // 2) % 2 == 0 else "0" for c in range(size))
            for r in range(size)]
    assert count_islands(grid) == (size // 2) ** 2 // 2
    snake = ["1" * 2000]
    assert count_islands(snake) == 1
