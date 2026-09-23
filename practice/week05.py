"""Question bank, Week 5 — linked lists. Problems W5-C1 to W5-C5.

Questions:  docs/question-bank/week05-questions.md
Tests:      tests/test_practice_week05.py

Every function works on a chain of `Node` objects (from `dsa.linked_list`),
given by its first node, `head` (None for an empty chain). Do not copy the values
into a Python list: walk and re-link the nodes.
"""

from dsa.linked_list import Node  # noqa: F401  (for your own experiments)


def middle_value(head):
    """W5-C1. The value of the middle node, in ONE pass.

    With an even number of nodes, the second of the two middle ones.
    1 -> 2 -> 3 -> 4 -> 5  gives 3 ;  1 -> 2 -> 3 -> 4  gives 3.
    Raise ValueError for an empty chain.

    Hint: two references, one moving one step at a time, one moving two.
    """
    raise NotImplementedError


def has_cycle(head):
    """W5-C2. True if following `next` from `head` never reaches None.

    O(n) time and O(1) extra space — no set of visited nodes.
    """
    raise NotImplementedError


def merge_sorted_chains(first, second):
    """W5-C3. Merge two chains sorted in non-decreasing order into one sorted
    chain, by RE-LINKING the existing nodes (create no new `Node` holding a
    value). Return the head of the merged chain. Stable: on a tie, `first` first.

    O(n + m) time, O(1) extra space.
    """
    raise NotImplementedError


def remove_duplicates_sorted(head):
    """W5-C4. In a sorted chain, keep only the first node of each run of equal
    values. Modify the chain in place and return its head.

    1 -> 1 -> 2 -> 3 -> 3 -> 3  becomes  1 -> 2 -> 3.   O(n), O(1) extra space.
    """
    raise NotImplementedError


def kth_from_end(head, k):
    """W5-C5. The value k nodes from the end: k = 1 is the last node.

    Raise IndexError unless 1 <= k <= length. Walk the chain at most twice —
    or, better, once with two references k apart.
    """
    raise NotImplementedError
