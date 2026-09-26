"""SOLUTION — try the exercise in `dsa/tree.py` first; see `solutions/README.md`.

Binary search trees, and the four ways to walk them.

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

from dsa.queue import CircularQueue


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
        new = TreeNode(value)
        if self.root is None:
            self.root = new
            return
        node = self.root
        while True:
            if value == node.value:
                return                          # already there: ignore
            if value < node.value:
                if node.left is None:
                    node.left = new
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = new
                    return
                node = node.right

    def contains(self, value):
        """True when `value` is in the tree. Target: O(h).

        Compare once per level and discard half the remaining tree each time —
        the same idea as binary search, in pointer form.
        """
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

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
        parent, node = None, self.root
        while node is not None and node.value != value:
            parent = node
            node = node.left if value < node.value else node.right
        if node is None:
            return                              # not present: nothing to do

        if node.left is not None and node.right is not None:
            # Two children: copy in the in-order successor, the leftmost node
            # of the right subtree, then delete that node instead. It has no
            # left child, so it is one of the two easy cases below.
            parent, successor = node, node.right
            while successor.left is not None:
                parent, successor = successor, successor.left
            node.value = successor.value
            node = successor

        # Now `node` has at most one child: a leaf (child is None) or one child.
        child = node.left if node.left is not None else node.right
        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child

    # -- asking -----------------------------------------------------------

    def min(self):
        """Smallest value. Raises ValueError when empty. Target: O(h).

        No comparisons needed — the BST invariant already says where it is.
        """
        if self.root is None:
            raise ValueError("min of an empty tree")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.value

    def max(self):
        """Largest value. Raises ValueError when empty. Target: O(h)."""
        if self.root is None:
            raise ValueError("max of an empty tree")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.value

    def height(self):
        """Edges on the longest root-to-leaf path. Target: O(n).

        An empty tree is -1 and a single node is 0, so that height is always
        "how many edges", never "how many nodes".
        """
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def size(self):
        """Number of nodes. Target: O(n)."""
        return self._size(self.root)

    def _size(self, node):
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def is_valid(self):
        """True when the BST invariant actually holds. Target: O(n).

        Careful: checking only `node.left.value < node.value` at each node is
        **not enough**. A value must beat every ancestor it passed on the way
        down, so carry a (low, high) range as you descend.
        """
        return self._is_valid(self.root, None, None)

    def _is_valid(self, node, low, high):
        """Every value in this subtree must lie strictly between low and high."""
        if node is None:
            return True
        if low is not None and node.value <= low:
            return False
        if high is not None and node.value >= high:
            return False
        return (self._is_valid(node.left, low, node.value)
                and self._is_valid(node.right, node.value, high))

    # -- walking ----------------------------------------------------------
    # Each traversal returns a NEW Python list of the values, in visit order.
    # The list is output only: the tree itself never stores one (the storage
    # rule). A private recursive helper that appends to that list is the
    # usual shape, e.g. `_in_order(self, node, out)`.

    def in_order(self):
        """left, node, right — returns a BST's values **in sorted order**.

        BinarySearchTree([5, 3, 8]).in_order() -> [3, 5, 8]

        That sortedness is the single most useful property a BST has.
        """
        out = []
        self._in_order(self.root, out)
        return out

    def _in_order(self, node, out):
        if node is not None:
            self._in_order(node.left, out)
            out.append(node.value)
            self._in_order(node.right, out)

    def pre_order(self):
        """node, left, right — the order that rebuilds this exact tree.

        Re-inserting a pre-order walk reproduces the original shape, which is
        why it is what you serialise.
        """
        out = []
        self._pre_order(self.root, out)
        return out

    def _pre_order(self, node, out):
        if node is not None:
            out.append(node.value)
            self._pre_order(node.left, out)
            self._pre_order(node.right, out)

    def post_order(self):
        """left, right, node — children always before their parent.

        The order you free a tree in, and the order an expression tree
        evaluates in (see `dsa/translation.py`).
        """
        out = []
        self._post_order(self.root, out)
        return out

    def _post_order(self, node, out):
        if node is not None:
            self._post_order(node.left, out)
            self._post_order(node.right, out)
            out.append(node.value)

    def level_order(self):
        """Top to bottom, left to right — breadth-first.

        The only one of the four that is **not** naturally recursive: it needs
        a queue, not the call stack. Use your own `dsa.queue.CircularQueue` —
        not a Python list (the course rule since Lecture 02). It must be the
        queue that **grows** (Lab 07's challenge): the last level of a tree
        can hold far more waiting nodes than the default capacity of 8.
        """
        out = []
        if self.root is None:
            return out
        pending = CircularQueue()               # grows as the frontier widens
        pending.enqueue(self.root)
        while not pending.is_empty():
            node = pending.dequeue()
            out.append(node.value)
            if node.left is not None:
                pending.enqueue(node.left)
            if node.right is not None:
                pending.enqueue(node.right)
        return out

    # -- plumbing ---------------------------------------------------------

    def __len__(self):
        return self.size()

    def __contains__(self, value):
        return self.contains(value)

    def __iter__(self):
        return iter(self.in_order())

    def __repr__(self):
        return f"BinarySearchTree({list(self)!r})" if self.root else "BinarySearchTree([])"
