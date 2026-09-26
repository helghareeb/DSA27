"""Question bank, Week 12 — heaps and priority queues. Problems W12-C1 to W12-C5.

Questions:  docs/question-bank/week12-questions.md
Tests:      tests/test_practice_week12.py

Use your own heaps as the working storage — `MinHeap` and `MaxHeap` from
`dsa/heap.py` — not a Python list, `sorted`, or the `heapq` module. Lists are
fine as inputs and results.
"""

from dsa.heap import MaxHeap, MinHeap  # noqa: F401  (your Week 12 exercise)


def is_min_heap(values):
    """W12-C1. True when the plain list `values` is a valid min-heap.

    Every element must be no smaller than its parent, where the parent of
    index i is (i - 1) // 2. The empty list and a single value are heaps.

    is_min_heap([1, 3, 2, 7, 4])  -> True
    is_min_heap([1, 3, 2, 2, 4])  -> False     (2 at index 3 is below 3)

    O(n), one comparison per element. No heap object is needed.
    """
    raise NotImplementedError


def top_k(values, k):
    """W12-C2. The k largest values, largest first.

    top_k([5, 1, 9, 3, 7, 2], 3) -> [9, 7, 5]
    top_k([4, 1], 5)             -> [4, 1]       (fewer than k: all of them)
    top_k([4, 1], 0)             -> []

    Raise ValueError for a negative k. O(n log k) time and O(k) extra space:
    keep a MinHeap of at most k values, whose root is the weakest of the best
    k seen so far. The tests count your comparisons, so sorting everything
    fails.
    """
    raise NotImplementedError


def merge_sorted(lists):
    """W12-C3. Merge k sorted lists into one sorted list.

    merge_sorted([[1, 4, 9], [2, 3], [], [5]]) -> [1, 2, 3, 4, 5, 9]
    merge_sorted([])                           -> []

    O(N log k) for N values in k lists: keep one entry per list in a MinHeap —
    its current front value, and enough to find the next one. The lists
    themselves must not be changed.
    """
    raise NotImplementedError


def join_ropes(lengths):
    """W12-C4. The cheapest total cost of joining all the ropes into one.

    Joining two ropes of lengths a and b costs a + b, and gives a rope of
    length a + b. Join them all, two at a time, as cheaply as possible.

    join_ropes([4, 3, 2, 6]) -> 29      (2+3=5, 4+5=9, 6+9=15; 5+9+15 = 29)
    join_ropes([7])          -> 0
    join_ropes([])           -> 0

    O(n log n). Hint: always join the two shortest ropes you have.
    """
    raise NotImplementedError


def running_medians(values):
    """W12-C5. The median of the first i values, for every i from 1 to n.

    For an odd count the median is the middle value; for an even count, the
    mean of the two middle values.

    running_medians([5, 15, 1, 3]) -> [5, 10.0, 5, 4.0]

    O(n log n): keep the smaller half in a MaxHeap and the larger half in a
    MinHeap, with sizes that never differ by more than one. The median is
    then at one or both roots.
    """
    raise NotImplementedError
