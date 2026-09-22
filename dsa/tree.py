"""Binary search trees, and the four ways to walk them.

A **binary search tree** keeps one invariant: for every node, everything in the
left subtree is smaller and everything in the right subtree is larger. Hold that
invariant and search costs O(h), where h is the height.

The catch is that h is only O(log n) when the tree is *balanced*. Insert
1, 2, 3, 4, 5 in order and you build a linked list wearing a tree costume —
every operation degrades to O(n). Balancing is the cure, and it is the subject
of the courses that follow this one.

Declared in the bylaw: "trees" and "tree traversals" (CS2101, AI 2020 p. 44;
IS122, SWE 2013 p. 38 and Medical Informatics 2014 p. 35).

Draw your tree at any point with the helper below:

    from viz.draw import draw_tree
    draw_tree(to_edges(bst.root), highlight={"8"})
"""

from __future__ import annotations


class TreeNode:
    """One node. Given to you — the structure is the lesson, not the box."""

    __slots__ = ("value", "left", "right")

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.value!r})"


def to_edges(node):
    """Collect (parent, child) pairs for `viz.draw.draw_tree`.

    Given to you so you can *see* your tree before the traversals work. BST
    values are unique — `insert` ignores duplicates — so a value is a safe id.
    """
    edges = []

    def walk(current):
        if current is None:
            return
        for child in (current.left, current.right):
            if child is not None:
                edges.append((str(current.value), str(child.value)))
                walk(child)

    walk(node)
    return edges


class BinarySearchTree:
    """An unbalanced BST. Every operation is O(h) — and h is your problem."""

    def __init__(self, values=()):
        self.root = None
        for value in values:
            self.insert(value)

    # -- building ---------------------------------------------------------

    def insert(self, value):
        """Place `value` in the tree, keeping the BST invariant.

        Duplicates are ignored — inserting a value already present leaves the
        tree unchanged. Target: O(h).
        """
        raise NotImplementedError

    def contains(self, value):
        """True when `value` is in the tree. Target: O(h).

        Compare once per level and discard half the remaining tree each time —
        the same idea as binary search, in pointer form.
        """
        raise NotImplementedError

    def delete(self, value):
        """Remove `value`, keeping the BST invariant. Target: O(h).

        The hard one, because there are three cases:
          * a leaf              -> detach it
          * one child           -> splice the child into its place
          * two children        -> replace the value with its in-order
                                   successor (the smallest value in the right
                                   subtree), then delete that successor

        Deleting a value that is not present does nothing. Returns None.
        """
        raise NotImplementedError

    # -- asking -----------------------------------------------------------

    def min(self):
        """Smallest value. Raises ValueError when empty. Target: O(h).

        No comparisons needed — the BST invariant already says where it is.
        """
        raise NotImplementedError

    def max(self):
        """Largest value. Raises ValueError when empty. Target: O(h)."""
        raise NotImplementedError

    def height(self):
        """Edges on the longest root-to-leaf path. Target: O(n).

        An empty tree is -1 and a single node is 0, so that height is always
        "how many edges", never "how many nodes".
        """
        raise NotImplementedError

    def size(self):
        """Number of nodes. Target: O(n)."""
        raise NotImplementedError

    def is_valid(self):
        """True when the BST invariant actually holds. Target: O(n).

        Careful: checking only `node.left.value < node.value` at each node is
        **not enough**. A value must beat every ancestor it passed on the way
        down, so carry a (low, high) range as you descend.
        """
        raise NotImplementedError

    # -- walking ----------------------------------------------------------
    # Each traversal yields values lazily. Return a generator, not a list.

    def in_order(self):
        """left, node, right — yields a BST's values **in sorted order**.

        list(BinarySearchTree([5, 3, 8]).in_order()) -> [3, 5, 8]

        That sortedness is the single most useful property a BST has.
        """
        raise NotImplementedError

    def pre_order(self):
        """node, left, right — the order that rebuilds this exact tree.

        Re-inserting a pre-order walk reproduces the original shape, which is
        why it is what you serialise.
        """
        raise NotImplementedError

    def post_order(self):
        """left, right, node — children always before their parent.

        The order you free a tree in, and the order an expression tree
        evaluates in (see `dsa/translation.py`).
        """
        raise NotImplementedError

    def level_order(self):
        """Top to bottom, left to right — breadth-first.

        The only one of the four that is **not** naturally recursive: it needs
        a queue, not the call stack. Use your own `dsa.queue.CircularQueue`,
        or a plain list as a queue if that is not written yet.
        """
        raise NotImplementedError

    # -- plumbing ---------------------------------------------------------

    def __len__(self):
        return self.size()

    def __contains__(self, value):
        return self.contains(value)

    def __iter__(self):
        return self.in_order()

    def __repr__(self):
        return f"BinarySearchTree({list(self)!r})" if self.root else "BinarySearchTree([])"
