"""Question bank, Week 11 — trees. Problems W11-C1 to W11-C5.

Questions:  docs/question-bank/week11-questions.md
Tests:      tests/test_practice_week11.py

Every function takes a tree by its root: a `TreeNode` from `dsa/tree.py`, or
None for the empty tree. Use only `.value`, `.left` and `.right` — the tests
hand you nodes that count how often you read them, so an answer that looks at
more of the tree than it needs to will fail. Lists are fine as inputs and
results; do not collect the whole tree into a list and work on that.
"""

from dsa.tree import TreeNode  # noqa: F401  (given in dsa/tree.py)


def count_leaves(node):
    """W11-C1. The number of leaves — nodes with no children — in the tree.

    count_leaves(None)                                   -> 0
    count_leaves(TreeNode(8, TreeNode(3), TreeNode(10))) -> 2

    O(n). Base case, recursive case: what is a leaf's answer?
    """
    raise NotImplementedError


def is_balanced(node):
    """W11-C2. True when, at EVERY node, the heights of the two subtrees
    differ by at most 1 (the AVL condition). The empty tree is balanced.

    O(n): one post-order walk. Calling a separate height function at every
    node is O(n log n) on a balanced tree and O(n^2) on a chain — the tests
    count your reads. Hint: let a helper return the height, or -2 to mean
    "already unbalanced somewhere below".
    """
    raise NotImplementedError


def range_values(node, low, high):
    """W11-C3. The values v of a BST with low <= v <= high, in sorted order.

    For the tree built from [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    range_values(root, 4, 10) -> [4, 6, 7, 8, 10]

    An in-order walk that SKIPS a subtree whenever the BST property says it
    cannot hold an answer: if node.value < low, nothing on its left can be in
    range. O(h + k) for k answers, not O(n).
    """
    raise NotImplementedError


def build_balanced(values):
    """W11-C4. A BST of minimum height holding `values`, which are sorted and
    distinct. Returns the root TreeNode (None for an empty list).

    The middle value is the root; the middles of the two halves are its
    children; and so on. build_balanced([1, 2, 3, 4, 5, 6, 7]) has root 4,
    children 2 and 6, and height 2.

    O(n). Pass indices lo and hi down the recursion — never slice.
    """
    raise NotImplementedError


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
    raise NotImplementedError
