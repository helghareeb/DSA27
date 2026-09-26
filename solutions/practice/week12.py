"""SOLUTION — try the problems in `practice/week12.py` first; see `solutions/README.md`.

Question bank, Week 12 — heaps and priority queues. Problems W12-C1 to W12-C5.

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
    for child in range(1, len(values)):
        if values[child] < values[(child - 1) // 2]:
            return False
    return True


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
    if k < 0:
        raise ValueError("k must be >= 0")
    if k == 0:
        return []
    heap = MinHeap()                  # the best k so far; root = weakest
    for value in values:
        if len(heap) < k:
            heap.push(value)
        elif heap.peek() < value:     # beats the weakest: replace it
            heap.pop()
            heap.push(value)
    result = [heap.pop() for _ in range(len(heap))]   # smallest first
    result.reverse()
    return result


def merge_sorted(lists):
    """W12-C3. Merge k sorted lists into one sorted list.

    merge_sorted([[1, 4, 9], [2, 3], [], [5]]) -> [1, 2, 3, 4, 5, 9]
    merge_sorted([])                           -> []

    O(N log k) for N values in k lists: keep one entry per list in a MinHeap —
    its current front value, and enough to find the next one. The lists
    themselves must not be changed.
    """
    heap = MinHeap()
    for which, values in enumerate(lists):
        if values:
            heap.push((values[0], which, 0))      # (value, list, position)
    merged = []
    while not heap.is_empty():
        value, which, position = heap.pop()
        merged.append(value)
        if position + 1 < len(lists[which]):
            heap.push((lists[which][position + 1], which, position + 1))
    return merged


def join_ropes(lengths):
    """W12-C4. The cheapest total cost of joining all the ropes into one.

    Joining two ropes of lengths a and b costs a + b, and gives a rope of
    length a + b. Join them all, two at a time, as cheaply as possible.

    join_ropes([4, 3, 2, 6]) -> 29      (2+3=5, 4+5=9, 6+9=15; 5+9+15 = 29)
    join_ropes([7])          -> 0
    join_ropes([])           -> 0

    O(n log n). Hint: always join the two shortest ropes you have.
    """
    heap = MinHeap(lengths)                       # heapify: O(n)
    total = 0
    while len(heap) > 1:
        joined = heap.pop() + heap.pop()          # the two shortest
        total += joined
        heap.push(joined)
    return total


def running_medians(values):
    """W12-C5. The median of the first i values, for every i from 1 to n.

    For an odd count the median is the middle value; for an even count, the
    mean of the two middle values.

    running_medians([5, 15, 1, 3]) -> [5, 10.0, 5, 4.0]

    O(n log n): keep the smaller half in a MaxHeap and the larger half in a
    MinHeap, with sizes that never differ by more than one. The median is
    then at one or both roots.
    """
    low = MaxHeap()                   # smaller half; root = its largest
    high = MinHeap()                  # larger half; root = its smallest
    medians = []
    for value in values:
        if low.is_empty() or value <= low.peek():
            low.push(value)
        else:
            high.push(value)
        if len(low) > len(high) + 1:  # rebalance: sizes differ by <= 1
            high.push(low.pop())
        elif len(high) > len(low):
            low.push(high.pop())
        if len(low) > len(high):
            medians.append(low.peek())
        else:
            medians.append((low.peek() + high.peek()) / 2)
    return medians
