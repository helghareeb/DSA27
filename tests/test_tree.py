"""Binary search tree exercises. Fail until `dsa/tree.py` is written."""

import pytest

from dsa.tree import BinarySearchTree, TreeNode, to_edges

pytestmark = pytest.mark.challenge


# A tree used by several tests below:
#
#           8
#         /   \
#        3     10
#       / \      \
#      1   6      14
#         / \    /
#        4   7  13
SAMPLE = [8, 3, 10, 1, 6, 14, 4, 7, 13]


# -- building -------------------------------------------------------------


def test_insert_and_contains():
    bst = BinarySearchTree(SAMPLE)
    for value in SAMPLE:
        assert bst.contains(value)
    for missing in (0, 2, 5, 9, 15):
        assert not bst.contains(missing)


def test_empty_tree():
    bst = BinarySearchTree()
    assert bst.root is None
    assert bst.size() == 0
    assert bst.height() == -1
    assert not bst.contains(1)
    assert list(bst.in_order()) == []


def test_insert_keeps_the_invariant():
    bst = BinarySearchTree(SAMPLE)
    assert bst.is_valid()


def test_duplicates_are_ignored():
    bst = BinarySearchTree([5, 3, 5, 3, 5])
    assert bst.size() == 2
    assert list(bst.in_order()) == [3, 5]


def test_structure_is_actually_a_bst():
    """Check the shape, not just the contents — a sorted list would pass
    in_order() while being nothing like a tree."""
    bst = BinarySearchTree([8, 3, 10])
    assert bst.root.value == 8
    assert bst.root.left.value == 3
    assert bst.root.right.value == 10


# -- asking ---------------------------------------------------------------


def test_size_and_height():
    bst = BinarySearchTree(SAMPLE)
    assert bst.size() == len(SAMPLE)
    assert bst.height() == 3          # 8 -> 10 -> 14 -> 13, three edges

    single = BinarySearchTree([1])
    assert single.height() == 0       # a lone node has no edges


def test_degenerate_tree_is_a_linked_list():
    """Sorted input gives the worst case: every operation becomes O(n)."""
    bst = BinarySearchTree([1, 2, 3, 4, 5])
    assert bst.height() == 4
    assert bst.root.left is None


def test_min_and_max():
    bst = BinarySearchTree(SAMPLE)
    assert bst.min() == 1
    assert bst.max() == 14


def test_min_max_on_empty_raise():
    bst = BinarySearchTree()
    with pytest.raises(ValueError):
        bst.min()
    with pytest.raises(ValueError):
        bst.max()


def test_is_valid_catches_a_hand_built_broken_tree():
    """9 is a legal right child of 3 if you only look at its parent — but it
    sits in the left subtree of 8, where nothing may exceed 8. Only a check
    that carries the ancestors' range down catches this one."""
    bad = BinarySearchTree()
    bad.root = TreeNode(8, left=TreeNode(3, right=TreeNode(9)), right=TreeNode(10))
    assert not bad.is_valid()


# -- deleting -------------------------------------------------------------


def test_delete_leaf():
    bst = BinarySearchTree(SAMPLE)
    bst.delete(1)
    assert not bst.contains(1)
    assert bst.size() == len(SAMPLE) - 1
    assert bst.is_valid()


def test_delete_node_with_one_child():
    bst = BinarySearchTree(SAMPLE)
    bst.delete(14)                     # has only a left child, 13
    assert not bst.contains(14)
    assert bst.contains(13)
    assert bst.is_valid()


def test_delete_node_with_two_children():
    bst = BinarySearchTree(SAMPLE)
    bst.delete(3)                      # has both 1 and 6 beneath it
    assert not bst.contains(3)
    for value in SAMPLE:
        if value != 3:
            assert bst.contains(value)
    assert bst.is_valid()


def test_delete_the_root():
    bst = BinarySearchTree(SAMPLE)
    bst.delete(8)
    assert not bst.contains(8)
    assert bst.is_valid()
    assert list(bst.in_order()) == sorted(v for v in SAMPLE if v != 8)


def test_delete_missing_value_is_a_no_op():
    bst = BinarySearchTree(SAMPLE)
    bst.delete(999)
    assert bst.size() == len(SAMPLE)


def test_delete_everything():
    bst = BinarySearchTree(SAMPLE)
    for value in SAMPLE:
        bst.delete(value)
        assert bst.is_valid()
    assert bst.size() == 0
    assert bst.root is None


# -- walking --------------------------------------------------------------


def test_in_order_is_sorted():
    """The single most useful property a BST has."""
    bst = BinarySearchTree(SAMPLE)
    assert list(bst.in_order()) == sorted(SAMPLE)


def test_pre_order():
    bst = BinarySearchTree(SAMPLE)
    assert list(bst.pre_order()) == [8, 3, 1, 6, 4, 7, 10, 14, 13]


def test_post_order():
    bst = BinarySearchTree(SAMPLE)
    assert list(bst.post_order()) == [1, 4, 7, 6, 3, 13, 14, 10, 8]


def test_level_order():
    bst = BinarySearchTree(SAMPLE)
    assert list(bst.level_order()) == [8, 3, 10, 1, 6, 14, 4, 7, 13]


def test_pre_order_rebuilds_the_same_tree():
    """Re-inserting a pre-order walk reproduces the original shape. That is
    why pre-order is what you serialise."""
    bst = BinarySearchTree(SAMPLE)
    rebuilt = BinarySearchTree(bst.pre_order())
    assert list(rebuilt.pre_order()) == list(bst.pre_order())


def test_traversals_are_lazy():
    """Yield the values, do not build a list and return it. Collecting into a
    list costs O(n) memory the caller may not want."""
    walk = BinarySearchTree(SAMPLE).in_order()
    assert not isinstance(walk, (list, tuple))
    assert iter(walk) is walk, "a traversal must be an iterator"
    assert next(walk) == 1


# -- plumbing -------------------------------------------------------------


def test_dunder_helpers():
    bst = BinarySearchTree(SAMPLE)
    assert len(bst) == len(SAMPLE)
    assert 6 in bst
    assert 5 not in bst
    assert list(bst) == sorted(SAMPLE)


def test_to_edges_matches_the_structure():
    """Given to you, but it must agree with the tree you built."""
    bst = BinarySearchTree([8, 3, 10])
    assert sorted(to_edges(bst.root)) == [("8", "10"), ("8", "3")]
