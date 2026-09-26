"""SOLUTION — try the problems in `practice/week11.py` first; see `solutions/README.md`.

Question bank, Week 11 — trees. Problems W11-C1 to W11-C5.

Questions:  docs/question-bank/week11-questions.md
Tests:      tests/test_practice_week11.py

Every function takes a tree by its root: a `TreeNode` from `dsa/tree.py`, or
None for the empty tree. Use only `.value`, `.left` and `.right` — the tests
hand you nodes that count how often you read them, so an answer that looks at
more of the tree than it needs to will fail. Lists are fine as inputs and
results; do not collect the whole tree into a list and work on that.
"""

from dsa.tree import TreeNode


def count_leaves(node):
    """W11-C1. The number of leaves — nodes with no children — in the tree.

    count_leaves(None)                                   -> 0
    count_leaves(TreeNode(8, TreeNode(3), TreeNode(10))) -> 2

    O(n). Base case, recursive case: what is a leaf's answer?
    """
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return count_leaves(node.left) + count_leaves(node.right)


def is_balanced(node):
    """W11-C2. True when, at EVERY node, the heights of the two subtrees
    differ by at most 1 (the AVL condition). The empty tree is balanced.

    O(n): one post-order walk. Calling a separate height function at every
    node is O(n log n) on a balanced tree and O(n^2) on a chain — the tests
    count your reads. Hint: let a helper return the height, or -2 to mean
    "already unbalanced somewhere below".
    """
    return _balanced_height(node) != -2


def _balanced_height(node):
    # The height of the subtree, or -2 if it is unbalanced anywhere.
    if node is None:
        return -1
    left = _balanced_height(node.left)
    if left == -2:
        return -2
    right = _balanced_height(node.right)
    if right == -2 or abs(left - right) > 1:
        return -2
    return 1 + max(left, right)


def range_values(node, low, high):
    """W11-C3. The values v of a BST with low <= v <= high, in sorted order.

    For the tree built from [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    range_values(root, 4, 10) -> [4, 6, 7, 8, 10]

    An in-order walk that SKIPS a subtree whenever the BST property says it
    cannot hold an answer: if node.value < low, nothing on its left can be in
    range. O(h + k) for k answers, not O(n).
    """
    out = []
    _collect(node, low, high, out)
    return out


def _collect(node, low, high, out):
    if node is None:
        return
    value = node.value
    if value > low:                 # answers may lie on the left
        _collect(node.left, low, high, out)
    if low <= value <= high:
        out.append(value)
    if value < high:                # answers may lie on the right
        _collect(node.right, low, high, out)


def build_balanced(values):
    """W11-C4. A BST of minimum height holding `values`, which are sorted and
    distinct. Returns the root TreeNode (None for an empty list).

    The middle value is the root; the middles of the two halves are its
    children; and so on. build_balanced([1, 2, 3, 4, 5, 6, 7]) has root 4,
    children 2 and 6, and height 2.

    O(n). Pass indices lo and hi down the recursion — never slice.
    """
    return _build(values, 0, len(values) - 1)


def _build(values, lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    root = TreeNode(values[mid])
    root.left = _build(values, lo, mid - 1)
    root.right = _build(values, mid + 1, hi)
    return root


def lowest_common_ancestor(node, a, b):
    """W11-C5. The value of the lowest node of a BST that has both a and b in
    its subtree (a node counts as in its own subtree). a and b are in the tree.

    For the tree built from [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    lowest_common_ancestor(root, 4, 7)  -> 6
    lowest_common_ancestor(root, 1, 7)  -> 3
    lowest_common_ancestor(root, 6, 4)  -> 6
    lowest_common_ancestor(root, 4, 13) -> 8

    O(h), with a loop: walk down from the root while a and b are on the same
    side.
    """
    while node is not None:
        value = node.value
        if a < value and b < value:
            node = node.left
        elif a > value and b > value:
            node = node.right
        else:
            return value            # a and b split here
    raise ValueError("a and b must be in the tree")
