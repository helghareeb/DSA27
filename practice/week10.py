"""Question bank, Week 10 — advanced sorting. Problems W10-C1 to W10-C5.

Questions:  docs/question-bank/week10-questions.md
Tests:      tests/test_practice_week10.py

Each problem is a piece of this week's sorts put to another use: the merge,
the partition, the recursion tree. The tests count comparisons (or reads), so a
solution that simply sorts everything fails where the question asks for less. Do not call
`sorted`, `list.sort`, `heapq` or `bisect`. Lists are fine here: these are
functions, not `dsa/` structures.
"""



def merge_k_sorted(lists):
    """W10-C1. Merge k sorted lists into one sorted list.

    merge_k_sorted([[1, 4, 9], [2, 3], [], [5]]) -> [1, 2, 3, 4, 5, 9]
    merge_k_sorted([])                           -> []

    O(N log k) comparisons for N values in k lists: merge the lists in PAIRS,
    round after round, as merge sort's levels do — not one after another into
    a growing result, which costs O(N k). Stable: on a tie, the value from the
    earlier list comes first. The input lists are not changed.
    """
    raise NotImplementedError


def count_inversions(values):
    """W10-C2. The number of pairs i < j with values[i] > values[j].

    count_inversions([2, 4, 1, 3, 5]) -> 3      # (2, 1), (4, 1), (4, 3)
    count_inversions([1, 2, 3])       -> 0
    count_inversions([3, 2, 1])       -> 3

    O(n log n): merge sort, counting as you merge. When the merge takes a
    value from the RIGHT run, it jumps over every value still waiting in the
    left run — each of those is one inversion. Checking every pair is O(n^2).
    """
    raise NotImplementedError


def kth_smallest(values, k):
    """W10-C3. The k-th smallest value, k = 1 for the smallest.

    kth_smallest([7, 2, 9, 4, 1], 1) -> 1
    kth_smallest([7, 2, 9, 4, 1], 3) -> 4
    kth_smallest([7, 2, 9, 4, 1], 5) -> 9

    Quickselect: partition as quicksort does, then continue into the ONE side
    that holds position k - 1 — the other side is never sorted. Use a random
    pivot. Expected O(n) comparisons. Raise ValueError unless
    1 <= k <= len(values). Do not change the caller's list.
    """
    raise NotImplementedError


def sort_colours(values):
    """W10-C4. Sort a list of 0s, 1s and 2s IN PLACE, in one pass. Returns None.

    v = [2, 0, 2, 1, 1, 0];  sort_colours(v);  v -> [0, 0, 1, 1, 2, 2]

    Dijkstra's "Dutch national flag": three regions, 0s at the front, 2s at the
    back, 1s in between, and one index scanning the unknown middle. It is a
    three-way partition around the pivot 1. O(n) time, O(1) extra space; only
    swaps, no counting and rebuilding.
    """
    raise NotImplementedError


def merge_sort_bottom_up(values):
    """W10-C5. Merge sort WITHOUT recursion: merge runs of width 1, 2, 4, ...

    merge_sort_bottom_up([5, 2, 9, 1, 7]) -> [1, 2, 5, 7, 9]

    Pass 1 merges neighbouring runs of 1 element into runs of 2, pass 2 merges
    those into runs of 4, and so on, until one run is left: ceil(log2 n)
    passes of O(n) each — the recursion tree of Lecture 10, walked from the
    leaves up. The last run of a pass may be short, or have no partner. Stable,
    at most about n log2 n comparisons, no recursive calls. Return a new list;
    do not change the caller's.
    """
    raise NotImplementedError
