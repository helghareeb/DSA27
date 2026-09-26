"""Question bank, Week 11 practice. Fail until `practice/week11.py` is written."""

import math
import random

import pytest

from dsa.tree import TreeNode
from practice.week11 import (build_balanced, count_leaves, is_balanced,
                             lowest_common_ancestor, range_values)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


class CountingNode:
    """Looks like a TreeNode, but counts every read of .value, .left, .right."""

    reads = 0

    def __init__(self, value, left=None, right=None):
        self._value, self._left, self._right = value, left, right

    @property
    def value(self):
        CountingNode.reads += 1
        return self._value

    @property
    def left(self):
        CountingNode.reads += 1
        return self._left

    @property
    def right(self):
        CountingNode.reads += 1
        return self._right


def bst(values):
    """A plain BST insert, so these tests do not depend on dsa/tree.py."""
    root = None
    for v in values:
        if root is None:
            root = TreeNode(v)
            continue
        cur = root
        while True:
            side = "left" if v < cur.value else "right"
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, TreeNode(v))
                break
            cur = nxt
    return root


def perfect(lo, hi, node=TreeNode):
    """A perfect BST on lo..hi (hi - lo + 1 must be 2^k - 1)."""
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    return node(mid, perfect(lo, mid - 1, node), perfect(mid + 1, hi, node))


SAMPLE = [8, 3, 10, 1, 6, 14, 4, 7, 13]


def in_order(node):
    return [] if node is None else in_order(node.left) + [node.value] + in_order(node.right)


def height(node):
    return -1 if node is None else 1 + max(height(node.left), height(node.right))


# -- W11-C1 ------------------------------------------------------------------


def test_count_leaves():
    assert count_leaves(None) == 0
    assert count_leaves(TreeNode(5)) == 1
    assert count_leaves(TreeNode(8, TreeNode(3), TreeNode(10))) == 2
    assert count_leaves(bst(SAMPLE)) == 4                  # 1, 4, 7, 13
    assert count_leaves(bst([1, 2, 3, 4, 5])) == 1         # a chain has one leaf
    assert count_leaves(perfect(1, 31)) == 16


# -- W11-C2 ------------------------------------------------------------------


@pytest.mark.parametrize("values,expected", [
    ([], True), ([5], True), ([2, 1], True), ([1, 2, 3], False), ([2, 1, 3], True),
    (SAMPLE, False),                         # at 10: left height -1, right height 1
    ([8, 3, 10, 1, 6, 9, 14], True), ([8, 3, 10, 1, 6, 9, 14, 4, 7, 13], True),
    ([8, 3, 10, 1, 6, 4, 7], False),         # at 8: left height 2, right height 0
])
def test_is_balanced(values, expected):
    assert is_balanced(bst(values)) is expected


def test_is_balanced_checks_every_node_not_just_the_root():
    # Root's subtrees both have height 2, but 3 and 10 are chains of two.
    root = bst([8, 3, 10, 2, 11, 1, 12])
    assert height(root.left) == height(root.right) == 2
    assert is_balanced(root) is False


def test_is_balanced_is_linear():
    root = perfect(1, 2 ** 13 - 1, CountingNode)          # 8,191 nodes
    CountingNode.reads = 0
    assert is_balanced(root) is True
    assert CountingNode.reads <= 4 * (2 ** 13), "a height() call at every node is O(n log n)"


# -- W11-C3 ------------------------------------------------------------------


@pytest.mark.parametrize("low,high,expected", [
    (4, 10, [4, 6, 7, 8, 10]), (5, 5, []), (6, 6, [6]), (0, 100, sorted(SAMPLE)),
    (11, 12, []), (-5, 1, [1]), (14, 20, [14]), (9, 13, [10, 13]),
])
def test_range_values(low, high, expected):
    assert range_values(bst(SAMPLE), low, high) == expected


def test_range_values_empty_tree():
    assert range_values(None, 1, 10) == []


def test_range_values_agrees_with_filtering_on_random_trees():
    rng = random.Random(11)
    for _ in range(50):
        values = rng.sample(range(100), rng.randint(0, 40))
        root = bst(values)
        low = rng.randint(-5, 100)
        high = rng.randint(low, 105)
        assert range_values(root, low, high) == sorted(v for v in values if low <= v <= high)


def test_range_values_skips_what_cannot_match():
    root = perfect(1, 2 ** 14 - 1, CountingNode)          # 16,383 nodes, height 13
    CountingNode.reads = 0
    assert range_values(root, 5000, 5009) == list(range(5000, 5010))
    assert CountingNode.reads <= 400, "a full in-order walk reads every node"


# -- W11-C4 ------------------------------------------------------------------


@pytest.mark.parametrize("n", [0, 1, 2, 3, 7, 8, 10, 15, 16, 100, 1000])
def test_build_balanced(n):
    values = list(range(0, 3 * n, 3))
    root = build_balanced(values)
    assert in_order(root) == values
    expected = -1 if n == 0 else math.floor(math.log2(n))
    assert height(root) == expected


def test_build_balanced_uses_tree_nodes_and_the_middle():
    root = build_balanced([1, 2, 3, 4, 5, 6, 7])
    assert isinstance(root, TreeNode)
    assert (root.value, root.left.value, root.right.value) == (4, 2, 6)
    assert is_balanced(root)


# -- W11-C5 ------------------------------------------------------------------


@pytest.mark.parametrize("a,b,expected", [
    (4, 7, 6), (7, 4, 6), (1, 7, 3), (6, 4, 6), (4, 13, 8), (13, 14, 14),
    (10, 13, 10), (8, 8, 8), (1, 1, 1), (3, 14, 8),
])
def test_lowest_common_ancestor(a, b, expected):
    assert lowest_common_ancestor(bst(SAMPLE), a, b) == expected


def test_lowest_common_ancestor_is_one_path():
    root = perfect(1, 2 ** 14 - 1, CountingNode)
    CountingNode.reads = 0
    assert lowest_common_ancestor(root, 4097, 4099) == 4098
    assert CountingNode.reads <= 60, "walk down one path; do not search both subtrees"
