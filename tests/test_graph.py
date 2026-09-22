"""Graph exercises. Fail until `dsa/graph.py` is written."""

import pytest

from dsa.graph import (
    Graph,
    MatrixGraph,
    bfs,
    connected_components,
    dfs,
    dfs_iterative,
    has_cycle,
    shortest_path_unweighted,
    topological_sort,
)

pytestmark = pytest.mark.challenge

# Both representations must satisfy the same contract, so every structural
# test runs against both.
BOTH = pytest.mark.parametrize("cls", [Graph, MatrixGraph], ids=lambda c: c.__name__)


def build(cls, edges, directed=False, nodes=()):
    graph = cls(directed=directed)
    for node in nodes:
        graph.add_node(node)
    for source, target in edges:
        graph.add_edge(source, target)
    return graph


#   A --- B       The sample undirected graph. D is reachable from A only
#   |   / |       through B or C, which makes the shortest-path tests
#   |  /  |       meaningful.
#   C     D
SAMPLE_EDGES = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D")]


# -- structure ------------------------------------------------------------


@BOTH
def test_add_node_and_len(cls):
    graph = cls()
    graph.add_node("A")
    graph.add_node("B")
    assert len(graph) == 2
    assert "A" in graph
    assert "Z" not in graph


@BOTH
def test_add_edge_creates_missing_nodes(cls):
    graph = cls()
    graph.add_edge("A", "B")
    assert len(graph) == 2
    assert graph.has_edge("A", "B")


@BOTH
def test_undirected_edges_go_both_ways(cls):
    graph = build(cls, [("A", "B")])
    assert graph.has_edge("A", "B")
    assert graph.has_edge("B", "A")


@BOTH
def test_directed_edges_go_one_way(cls):
    graph = build(cls, [("A", "B")], directed=True)
    assert graph.has_edge("A", "B")
    assert not graph.has_edge("B", "A")


@BOTH
def test_adding_a_node_twice_keeps_its_edges(cls):
    """A careless add_node resets the node's entry and silently drops edges."""
    graph = build(cls, [("A", "B")])
    graph.add_node("A")
    assert graph.has_edge("A", "B")
    assert len(graph) == 2


@BOTH
def test_neighbours(cls):
    graph = build(cls, SAMPLE_EDGES)
    assert sorted(graph.neighbours("A")) == ["B", "C"]
    assert sorted(graph.neighbours("D")) == ["B"]


@BOTH
def test_neighbours_of_missing_node_raises(cls):
    with pytest.raises(KeyError):
        build(cls, SAMPLE_EDGES).neighbours("Z")


@BOTH
def test_isolated_node_has_no_neighbours(cls):
    graph = build(cls, SAMPLE_EDGES, nodes=["Z"])
    assert graph.neighbours("Z") == []
    assert graph.degree("Z") == 0


@BOTH
def test_nodes_and_degree(cls):
    graph = build(cls, SAMPLE_EDGES)
    assert sorted(graph.nodes()) == ["A", "B", "C", "D"]
    assert graph.degree("B") == 3
    assert graph.degree("D") == 1


@BOTH
def test_undirected_edges_are_reported_once(cls):
    """Four edges, not eight — do not report A-B and B-A separately."""
    graph = build(cls, SAMPLE_EDGES)
    edges = graph.edges()
    assert len(edges) == 4
    assert {frozenset(edge) for edge in edges} == {frozenset(e) for e in SAMPLE_EDGES}


@BOTH
def test_directed_edges_keep_their_direction(cls):
    graph = build(cls, [("A", "B"), ("B", "C")], directed=True)
    assert sorted(graph.edges()) == [("A", "B"), ("B", "C")]


# -- the searches ---------------------------------------------------------


@BOTH
def test_bfs_visits_by_distance(cls):
    """A first, then its neighbours, then theirs. D is two steps out, so it
    must come last however the neighbours are ordered."""
    order = bfs(build(cls, SAMPLE_EDGES), "A")
    assert order[0] == "A"
    assert set(order) == {"A", "B", "C", "D"}
    assert order.index("D") > order.index("B")


@BOTH
def test_bfs_visits_each_node_once(cls):
    """The graph has a cycle A-B-C-A; without a visited set this never ends."""
    order = bfs(build(cls, SAMPLE_EDGES), "A")
    assert len(order) == len(set(order))


@BOTH
@pytest.mark.parametrize("search", [dfs, dfs_iterative], ids=["dfs", "dfs_iterative"])
def test_dfs_reaches_everything(cls, search):
    order = search(build(cls, SAMPLE_EDGES), "A")
    assert order[0] == "A"
    assert set(order) == {"A", "B", "C", "D"}
    assert len(order) == len(set(order))


@BOTH
def test_dfs_and_dfs_iterative_agree(cls):
    """Same walk, one using the call stack and one using your own stack."""
    graph = build(cls, SAMPLE_EDGES)
    assert dfs(graph, "A") == dfs_iterative(graph, "A")


@BOTH
def test_dfs_goes_deep_and_bfs_goes_wide(cls):
    """The test that tells the two searches apart. A has two branches; DFS
    follows the first to its end (C) before touching D, BFS takes D first."""
    graph = build(cls, [("A", "B"), ("B", "C"), ("A", "D")])
    assert dfs(graph, "A") == ["A", "B", "C", "D"]
    assert bfs(graph, "A") == ["A", "B", "D", "C"]


@BOTH
def test_search_from_isolated_node(cls):
    graph = build(cls, SAMPLE_EDGES, nodes=["Z"])
    assert bfs(graph, "Z") == ["Z"]
    assert dfs(graph, "Z") == ["Z"]


# -- paths and components -------------------------------------------------


@BOTH
def test_shortest_path(cls):
    graph = build(cls, SAMPLE_EDGES)
    assert shortest_path_unweighted(graph, "A", "D") == ["A", "B", "D"]


@BOTH
def test_shortest_path_to_self(cls):
    graph = build(cls, SAMPLE_EDGES)
    assert shortest_path_unweighted(graph, "A", "A") == ["A"]


@BOTH
def test_shortest_path_is_shortest_not_merely_a_path(cls):
    """A long way round exists; BFS must still find the two-edge route."""
    graph = build(cls, [("A", "B"), ("B", "Z"), ("A", "X"), ("X", "Y"), ("Y", "Z")])
    assert shortest_path_unweighted(graph, "A", "Z") == ["A", "B", "Z"]


@BOTH
def test_unreachable_goal_is_none(cls):
    graph = build(cls, SAMPLE_EDGES, nodes=["Z"])
    assert shortest_path_unweighted(graph, "A", "Z") is None


@BOTH
def test_connected_components(cls):
    graph = build(cls, [("A", "B"), ("C", "D")], nodes=["E", "F"])
    groups = sorted(sorted(group) for group in connected_components(graph))
    assert groups == [["A", "B"], ["C", "D"], ["E"], ["F"]]


@BOTH
def test_one_component_when_connected(cls):
    graph = build(cls, SAMPLE_EDGES)
    assert len(connected_components(graph)) == 1


# -- cycles and ordering --------------------------------------------------


@BOTH
def test_undirected_cycle_detection(cls):
    assert has_cycle(build(cls, [("A", "B"), ("B", "C"), ("C", "A")]))
    assert not has_cycle(build(cls, [("A", "B"), ("B", "C")]))


@BOTH
def test_undirected_tree_has_no_cycle(cls):
    """The trap: B's neighbour A is already visited, but it is only the node
    we arrived from — that is not a cycle."""
    graph = build(cls, [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")])
    assert not has_cycle(graph)


@BOTH
def test_directed_cycle_detection(cls):
    assert has_cycle(build(cls, [("A", "B"), ("B", "C"), ("C", "A")], directed=True))
    assert not has_cycle(build(cls, [("A", "B"), ("A", "C"), ("B", "C")], directed=True))


@BOTH
def test_directed_diamond_is_not_a_cycle(cls):
    """A -> B -> D and A -> C -> D. D is visited twice but never on the stack
    twice, so this is a DAG. Confusing "visited" with "on the current path" is
    the classic bug here."""
    graph = build(cls, [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")], directed=True)
    assert not has_cycle(graph)


@BOTH
def test_topological_sort_respects_every_edge(cls):
    graph = build(cls, [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")], directed=True)
    order = topological_sort(graph)
    assert sorted(order) == ["A", "B", "C", "D"]
    position = {node: index for index, node in enumerate(order)}
    for source, target in graph.edges():
        assert position[source] < position[target]


@BOTH
def test_topological_sort_of_a_cycle_is_none(cls):
    graph = build(cls, [("A", "B"), ("B", "C"), ("C", "A")], directed=True)
    assert topological_sort(graph) is None


@BOTH
def test_topological_sort_includes_isolated_nodes(cls):
    graph = build(cls, [("A", "B")], directed=True, nodes=["Z"])
    assert sorted(topological_sort(graph)) == ["A", "B", "Z"]


# -- the bridge to viz ----------------------------------------------------


def test_to_networkx_round_trip():
    """Given to you, but it must agree with the graph you built."""
    from dsa.graph import to_networkx

    graph = build(Graph, SAMPLE_EDGES)
    converted = to_networkx(graph)
    assert sorted(converted.nodes()) == ["A", "B", "C", "D"]
    assert converted.number_of_edges() == 4
