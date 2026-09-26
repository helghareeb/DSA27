"""SOLUTION — try the problems in `practice/week09.py` first; see `solutions/README.md`.

Question bank, Week 9 — basic sorting. Problems W9-C1 to W9-C5.

Questions:  docs/question-bank/week09-questions.md
Tests:      tests/test_practice_week09.py

Write the sorting yourself: do not call `sorted`, `list.sort`, `min` or `max`
on the values. Lists are fine as inputs and results; the counts of W9-C5 go
in a course `Array`. Several tests count your comparisons or your reads, so
the cost in each docstring is checked, not just the answer.
"""

from dsa.array import Array


def count_inversions(values):
    """W9-C1. The number of pairs i < j with values[i] > values[j].

    count_inversions([5, 2, 9, 1, 7, 3]) -> 8
    count_inversions([1, 2, 3])          -> 0
    count_inversions([3, 2, 1])          -> 3

    O(n^2): compare every pair once. (Week 10 does it in O(n log n).)
    """
    n = len(values)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if values[i] > values[j]:
                count += 1
    return count


def sort_by_key(items, key):
    """W9-C2. A new list of `items` sorted by `key(item)`, STABLY.

    Items with equal keys keep their original order. Compare keys only —
    never the items themselves, which may not be comparable at all.

    sort_by_key(["pear", "fig", "apple", "kiwi"], len)
        -> ["fig", "pear", "kiwi", "apple"]

    Insertion sort. O(n^2) worst, O(n) on input already in key order. Do not
    change `items`.
    """
    out = list(items)
    for i in range(1, len(out)):
        current = out[i]
        k = key(current)
        j = i - 1
        while j >= 0 and key(out[j]) > k:  # strictly greater: stable
            out[j + 1] = out[j]
            j -= 1
        out[j + 1] = current
    return out


def dutch_flag(values):
    """W9-C3. Sort a list of 0s, 1s and 2s IN PLACE, in one pass. Returns None.

    values = [2, 0, 1, 2, 1, 0]
    dutch_flag(values)  # values is now [0, 0, 1, 1, 2, 2]

    Dijkstra's Dutch national flag: keep three regions, 0s at the front, 2s at
    the back, 1s in between, and an unknown region that shrinks by one at
    every step. O(n) time, O(1) extra space.
    """
    lo, mid, hi = 0, 0, len(values) - 1
    # values[:lo] are 0, values[lo:mid] are 1, values[hi+1:] are 2
    while mid <= hi:
        v = values[mid]
        if v == 0:
            values[lo], values[mid] = values[mid], values[lo]
            lo += 1
            mid += 1
        elif v == 1:
            mid += 1
        else:
            values[mid], values[hi] = values[hi], values[mid]
            hi -= 1  # do not advance mid: new value unseen


def sort_k_sorted(values, k):
    """W9-C4. Sort a list in which every value is at most k places from its
    sorted position. Return a new list.

    sort_k_sorted([2, 1, 4, 3, 6, 5], 1) -> [1, 2, 3, 4, 5, 6]

    O(nk): insertion sort, because each value has at most k larger values
    before it, so it shifts at most k times. The tests count comparisons.
    """
    out = list(values)
    for i in range(1, len(out)):
        current = out[i]
        j = i - 1
        while j >= 0 and out[j] > current:
            out[j + 1] = out[j]
            j -= 1
        out[j + 1] = current
    return out


def counting_sort_by_key(items, key, k):
    """W9-C5. A new list of `items` sorted by the integer `key(item)`, where
    every key is in 0..k-1. STABLE, and O(n + k). No comparisons at all.

    counting_sort_by_key(list("banana"), lambda c: ord(c) - ord("a"), 26)
        -> ['a', 'a', 'a', 'b', 'n', 'n']

    Count the keys; turn the counts into starting positions (a running sum);
    then place each item, in input order, at the next free position for its
    key. Raise ValueError for a key outside 0..k-1.
    """
    counts = Array(k, fill=0)
    for item in items:
        kk = key(item)
        if not 0 <= kk < k:
            raise ValueError(f"key {kk!r} is outside 0..{k - 1}")
        counts[kk] += 1
    start = 0  # counts[v] becomes where v starts
    for v in range(k):
        counts[v], start = start, start + counts[v]
    out = Array(len(items))
    for item in items:  # input order: this is the stability
        kk = key(item)
        out[counts[kk]] = item
        counts[kk] += 1
    return list(out)
