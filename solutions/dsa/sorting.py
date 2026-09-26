"""SOLUTION — try the exercise in `dsa/sorting.py` first; see `solutions/README.md`.

Sorting — basic and advanced.

Each algorithm appears twice:

  * `bubble_sort(values)`       -> returns a new sorted list
  * `bubble_sort_steps(values)` -> *generator* yielding (values, highlight)

The `_steps` form is the one implementation; the plain form exhausts it. So
there is one piece of code to keep correct, and the animation shows exactly the
code the tests grade.

The storage rule holds here too: the list you pass in is copied into the course
`Array`, the sort works on that `Array`, and a list comes back out. Each
snapshot yielded is `list(a)` — a fresh list — so the frames are independent.
"""

from __future__ import annotations

import random

from dsa.array import Array

__all__ = [
    "bubble_sort", "bubble_sort_steps",
    "selection_sort", "selection_sort_steps",
    "insertion_sort", "insertion_sort_steps",
    "merge_sort", "merge_sort_steps",
    "quick_sort", "quick_sort_steps",
    "heap_sort", "heap_sort_steps",
    "counting_sort",
    "is_sorted",
]


def is_sorted(values):
    """True when `values` is non-decreasing. Handy in tests and assertions."""
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def _copy(values):
    """The input, copied into a fresh `Array`. The caller's list is never touched."""
    return Array.from_values(values)


def _finish(steps):
    """Run a `_steps` generator to the end and return its last state."""
    state = []
    for state, _ in steps:
        pass
    return list(state)


# -- basic: O(n^2) --------------------------------------------------------
#
# Each basic sort takes `snapshot`, the function that turns the working Array
# into the frame it yields. The default, `list`, copies it: an animation needs
# every frame to be its own list. But a copy costs O(n), and a sort that copies
# before each of its O(n^2) comparisons costs O(n^3) — 70 seconds for 800
# values, measured. The plain sort needs only the last state, so it passes
# `_live`, which copies nothing: one implementation, and still O(n^2).


def _live(a):
    """The working Array itself — no copy. For the plain sorts only."""
    return a


def bubble_sort_steps(values, snapshot=list):
    """Yield (list, (i, j)) before each comparison. O(n^2), O(1) extra space.

    Early exit: a pass with no swap means the array is sorted, so the best
    case — already-sorted input — is one pass, O(n).
    """
    a = _copy(values)
    n = len(a)
    yield snapshot(a), ()
    for end in range(n - 1, 0, -1):          # a[end+1:] is already in place
        swapped = False
        for j in range(end):
            yield snapshot(a), (j, j + 1)      # about to compare
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    yield snapshot(a), ()


def bubble_sort(values):
    return _finish(bubble_sort_steps(values, snapshot=_live))


def selection_sort_steps(values, snapshot=list):
    """Repeatedly select the minimum of the unsorted tail. O(n^2) always.

    At most n-1 swaps — the fewest writes of any comparison sort. Not stable:
    the long-distance swap can jump an element over its equal.
    """
    a = _copy(values)
    n = len(a)
    yield snapshot(a), ()
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            yield snapshot(a), (smallest, j)
            if a[j] < a[smallest]:
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
            yield snapshot(a), (i, smallest)
    yield snapshot(a), ()


def selection_sort(values):
    return _finish(selection_sort_steps(values, snapshot=_live))


def insertion_sort_steps(values, snapshot=list):
    """Grow a sorted prefix one element at a time. O(n^2) worst, O(n) best.

    Stable: an element moves left only past values strictly greater than it,
    so it never overtakes an equal.
    """
    a = _copy(values)
    n = len(a)
    yield snapshot(a), ()
    for i in range(1, n):
        current = a[i]
        j = i - 1
        while j >= 0 and a[j] > current:       # strictly greater: stability
            a[j + 1] = a[j]                    # shift right, no swap
            j -= 1
            a[j + 1] = current
            yield snapshot(a), (j + 1, j + 2)
        a[j + 1] = current
    yield snapshot(a), ()


def insertion_sort(values):
    return _finish(insertion_sort_steps(values, snapshot=_live))


# -- advanced: O(n log n) -------------------------------------------------
#
# The same `snapshot` parameter as the basic sorts. Merge and quick sort yield
# about n frames and heap sort about n; copying n values for each would make
# the plain forms O(n^2) — merge sort measured 0.36, 1.29 and 4.7 seconds for
# 1,000, 2,000 and 4,000 values before this. With `_live` they are O(n log n).


def _merge(a, lo, mid, hi, scratch):
    """Merge the sorted runs a[lo:mid] and a[mid:hi] through `scratch`.

    Ties take from the LEFT run — that single `<=` is what makes merge sort
    stable.
    """
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if a[i] <= a[j]:
            scratch[k] = a[i]
            i += 1
        else:
            scratch[k] = a[j]
            j += 1
        k += 1
    while i < mid:
        scratch[k] = a[i]
        i += 1
        k += 1
    while j < hi:
        scratch[k] = a[j]
        j += 1
        k += 1
    for k in range(lo, hi):
        a[k] = scratch[k]


def merge_sort_steps(values, snapshot=list):
    """Divide, sort each half, merge. O(n log n) always, O(n) extra space.

    Top-down and recursive, one `scratch` Array shared by every merge, so the
    extra space is n — not n log n. Yields after each merge, highlighting the
    range that was just merged.
    """
    a = _copy(values)
    scratch = Array(len(a))
    yield snapshot(a), ()

    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        yield from sort(lo, mid)
        yield from sort(mid, hi)
        _merge(a, lo, mid, hi, scratch)
        yield snapshot(a), tuple(range(lo, hi))

    yield from sort(0, len(a))
    yield snapshot(a), ()


def merge_sort(values):
    return _finish(merge_sort_steps(values, snapshot=_live))


def _choose_pivot(a, lo, hi, strategy, rng):
    """Index of the pivot for a[lo..hi] inclusive."""
    if strategy == "first":
        return lo
    if strategy == "last":
        return hi
    if strategy == "random":
        return rng.randint(lo, hi)
    if strategy == "median3":
        mid = (lo + hi) // 2
        first, middle, last = a[lo], a[mid], a[hi]
        if first <= middle <= last or last <= middle <= first:
            return mid
        if middle <= first <= last or last <= first <= middle:
            return lo
        return hi
    raise ValueError(f"unknown pivot strategy {strategy!r}: "
                     "use 'first', 'last', 'random' or 'median3'")


def _partition(a, lo, hi):
    """Lomuto partition around a[hi]. Returns the pivot's final index.

    Invariant: a[lo:boundary] < pivot, a[boundary:j] >= pivot.
    """
    pivot = a[hi]
    boundary = lo
    for j in range(lo, hi):
        if a[j] < pivot:
            a[boundary], a[j] = a[j], a[boundary]
            boundary += 1
    a[boundary], a[hi] = a[hi], a[boundary]
    return boundary


def quick_sort_steps(values, pivot="median3", snapshot=list):
    """Partition around a pivot, recurse. O(n log n) average, O(n^2) worst.

    `pivot` is "first", "last", "random" or "median3". The chosen pivot is
    swapped to the end and Lomuto's partition does the rest.

    Recursion goes into the SMALLER side and loops on the larger, so the call
    stack stays O(log n) deep even on the O(n^2) inputs — which is why the
    200-element sorted list with pivot="first" does not hit Python's recursion
    limit.
    """
    a = _copy(values)
    rng = random.Random(27)               # reproducible frames
    yield snapshot(a), ()

    def sort(lo, hi):
        while lo < hi:
            p = _choose_pivot(a, lo, hi, pivot, rng)
            a[p], a[hi] = a[hi], a[p]
            q = _partition(a, lo, hi)
            yield snapshot(a), (q,)
            if q - lo < hi - q:
                yield from sort(lo, q - 1)
                lo = q + 1
            else:
                yield from sort(q + 1, hi)
                hi = q - 1

    yield from sort(0, len(a) - 1)
    yield snapshot(a), ()


def quick_sort(values, pivot="median3"):
    return _finish(quick_sort_steps(values, pivot, snapshot=_live))


def _sift_down(a, index, size):
    """Max-heap sift-down of a[index] within a[0:size]."""
    while True:
        largest = index
        left, right = 2 * index + 1, 2 * index + 2
        if left < size and a[left] > a[largest]:
            largest = left
        if right < size and a[right] > a[largest]:
            largest = right
        if largest == index:
            return
        a[index], a[largest] = a[largest], a[index]
        index = largest


def heap_sort_steps(values, snapshot=list):
    """Build a max-heap in place, then repeatedly swap the root to the back.

    O(n log n) always, O(1) extra space, not stable. Build-heap sifts down
    from the last parent to the root: O(n) in total, not O(n log n).
    """
    a = _copy(values)
    n = len(a)
    yield snapshot(a), ()
    for index in range(n // 2 - 1, -1, -1):        # build the heap: O(n)
        _sift_down(a, index, n)
    yield snapshot(a), ()
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]                 # the max goes to the back
        _sift_down(a, 0, end)                       # restore the heap in a[:end]
        yield snapshot(a), (0, end)
    yield snapshot(a), ()


def heap_sort(values):
    return _finish(heap_sort_steps(values, snapshot=_live))


# -- not a comparison sort ------------------------------------------------


def counting_sort(values, max_value=None):
    """Sort small non-negative integers by counting. O(n + k), k = max_value + 1.

    Never compares two elements, which is how it gets under the O(n log n)
    lower bound — that bound is about comparison sorts only.
    """
    if len(values) == 0:
        return []
    for v in values:
        if not isinstance(v, int) or v < 0:
            raise ValueError("counting_sort needs non-negative integers")
    k = (max(values) if max_value is None else max_value) + 1
    counts = Array(k, fill=0)
    for v in values:
        counts[v] += 1
    out = Array(len(values))
    i = 0
    for v in range(k):
        for _ in range(counts[v]):
            out[i] = v
            i += 1
    return list(out)
