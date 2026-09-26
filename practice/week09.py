"""Question bank, Week 9 — basic sorting. Problems W9-C1 to W9-C5.

Questions:  docs/question-bank/week09-questions.md
Tests:      tests/test_practice_week09.py

Write the sorting yourself: do not call `sorted`, `list.sort`, `min` or `max`
on the values. Lists are fine as inputs and results; the counts of W9-C5 go
in a course `Array`. Several tests count your comparisons or your reads, so
the cost in each docstring is checked, not just the answer.
"""

from dsa.array import Array  # noqa: F401  (for W9-C5)


def count_inversions(values):
    """W9-C1. The number of pairs i < j with values[i] > values[j].

    count_inversions([5, 2, 9, 1, 7, 3]) -> 8
    count_inversions([1, 2, 3])          -> 0
    count_inversions([3, 2, 1])          -> 3

    O(n^2): compare every pair once. (Week 10 does it in O(n log n).)
    """
    raise NotImplementedError


def sort_by_key(items, key):
    """W9-C2. A new list of `items` sorted by `key(item)`, STABLY.

    Items with equal keys keep their original order. Compare keys only —
    never the items themselves, which may not be comparable at all.

    sort_by_key(["pear", "fig", "apple", "kiwi"], len)
        -> ["fig", "pear", "kiwi", "apple"]

    Insertion sort. O(n^2) worst, O(n) on input already in key order. Do not
    change `items`.
    """
    raise NotImplementedError


def dutch_flag(values):
    """W9-C3. Sort a list of 0s, 1s and 2s IN PLACE, in one pass. Returns None.

    values = [2, 0, 1, 2, 1, 0]
    dutch_flag(values)  # values is now [0, 0, 1, 1, 2, 2]

    Dijkstra's Dutch national flag: keep three regions, 0s at the front, 2s at
    the back, 1s in between, and an unknown region that shrinks by one at
    every step. O(n) time, O(1) extra space.
    """
    raise NotImplementedError


def sort_k_sorted(values, k):
    """W9-C4. Sort a list in which every value is at most k places from its
    sorted position. Return a new list.

    sort_k_sorted([2, 1, 4, 3, 6, 5], 1) -> [1, 2, 3, 4, 5, 6]

    O(nk): insertion sort, because each value has at most k larger values
    before it, so it shifts at most k times. The tests count comparisons.
    """
    raise NotImplementedError


def counting_sort_by_key(items, key, k):
    """W9-C5. A new list of `items` sorted by the integer `key(item)`, where
    every key is in 0..k-1. STABLE, and O(n + k). No comparisons at all.

    counting_sort_by_key(list("banana"), lambda c: ord(c) - ord("a"), 26)
        -> ['a', 'a', 'a', 'b', 'n', 'n']

    Count the keys; turn the counts into starting positions (a running sum);
    then place each item, in input order, at the next free position for its
    key. Raise ValueError for a key outside 0..k-1.
    """
    raise NotImplementedError
