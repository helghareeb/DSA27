"""SOLUTION — try the problems in `practice/week10.py` first; see `solutions/README.md`.

Question bank, Week 10 — advanced sorting. Problems W10-C1 to W10-C5.

Questions:  docs/question-bank/week10-questions.md
Tests:      tests/test_practice_week10.py

Each problem is a piece of this week's sorts put to another use: the merge,
the partition, the recursion tree. The tests count comparisons (or reads), so a
solution that simply sorts everything fails where the question asks for less. Do not call
`sorted`, `list.sort`, `heapq` or `bisect`. Lists are fine here: these are
functions, not `dsa/` structures.
"""

import random


def merge_k_sorted(lists):
    """W10-C1. Merge k sorted lists into one sorted list.

    merge_k_sorted([[1, 4, 9], [2, 3], [], [5]]) -> [1, 2, 3, 4, 5, 9]
    merge_k_sorted([])                           -> []

    O(N log k) comparisons for N values in k lists: merge the lists in PAIRS,
    round after round, as merge sort's levels do — not one after another into
    a growing result, which costs O(N k). Stable: on a tie, the value from the
    earlier list comes first. The input lists are not changed.
    """
    if not lists:
        return []
    runs = [list(run) for run in lists]
    while len(runs) > 1:
        merged = []
        for i in range(0, len(runs) - 1, 2):
            merged.append(_merge_two(runs[i], runs[i + 1]))
        if len(runs) % 2 == 1:
            merged.append(runs[-1])                 # the odd one out waits a round
        runs = merged
    return runs[0]


def _merge_two(left, right):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:                     # a tie takes from the left
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def count_inversions(values):
    """W10-C2. The number of pairs i < j with values[i] > values[j].

    count_inversions([2, 4, 1, 3, 5]) -> 3      # (2, 1), (4, 1), (4, 3)
    count_inversions([1, 2, 3])       -> 0
    count_inversions([3, 2, 1])       -> 3

    O(n log n): merge sort, counting as you merge. When the merge takes a
    value from the RIGHT run, it jumps over every value still waiting in the
    left run — each of those is one inversion. Checking every pair is O(n^2).
    """
    def sort(items):
        if len(items) <= 1:
            return list(items), 0
        mid = len(items) // 2
        left, inside_left = sort(items[:mid])
        right, inside_right = sort(items[mid:])
        merged, i, j, across = [], 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                across += len(left) - i             # right[j] jumps over all of these
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inside_left + inside_right + across

    return sort(list(values))[1]


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
    if not 1 <= k <= len(values):
        raise ValueError("k must be between 1 and len(values)")
    a = list(values)
    rng = random.Random(10)
    lo, hi, target = 0, len(a) - 1, k - 1
    while True:
        p = rng.randint(lo, hi)
        a[p], a[hi] = a[hi], a[p]
        pivot, boundary = a[hi], lo
        for j in range(lo, hi):                     # Lomuto, as in quick sort
            if a[j] < pivot:
                a[boundary], a[j] = a[j], a[boundary]
                boundary += 1
        a[boundary], a[hi] = a[hi], a[boundary]
        if boundary == target:
            return a[boundary]
        if boundary < target:
            lo = boundary + 1                       # the answer is on the right
        else:
            hi = boundary - 1                       # the answer is on the left


def sort_colours(values):
    """W10-C4. Sort a list of 0s, 1s and 2s IN PLACE, in one pass. Returns None.

    v = [2, 0, 2, 1, 1, 0];  sort_colours(v);  v -> [0, 0, 1, 1, 2, 2]

    Dijkstra's "Dutch national flag": three regions, 0s at the front, 2s at the
    back, 1s in between, and one index scanning the unknown middle. It is a
    three-way partition around the pivot 1. O(n) time, O(1) extra space; only
    swaps, no counting and rebuilding.
    """
    low, mid, high = 0, 0, len(values) - 1
    while mid <= high:                              # values[mid..high] is unknown
        colour = values[mid]
        if colour == 0:
            values[low], values[mid] = values[mid], values[low]
            low += 1
            mid += 1
        elif colour == 1:
            mid += 1
        else:
            values[mid], values[high] = values[high], values[mid]
            high -= 1                               # do not advance mid: re-check


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
    a = list(values)
    n = len(a)
    scratch = [None] * n
    width = 1
    while width < n:
        for lo in range(0, n, 2 * width):           # merge a[lo:mid] and a[mid:hi]
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            i, j = lo, mid
            for k in range(lo, hi):
                if j >= hi or (i < mid and a[i] <= a[j]):
                    scratch[k] = a[i]               # left run: on a tie too
                    i += 1
                else:
                    scratch[k] = a[j]
                    j += 1
        a, scratch = scratch, a                     # the merged pass becomes the input
        width *= 2
    return a
