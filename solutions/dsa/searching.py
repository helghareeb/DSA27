"""SOLUTION — try the exercise in `dsa/searching.py` first; see `solutions/README.md`.

Searching — basic and advanced.

Every function takes an already-sorted sequence unless it says otherwise.
Plot linear against binary with `viz.complexity.measure` and the difference
between O(n) and O(log n) stops being a claim and becomes a picture.
"""

from __future__ import annotations

import math

__all__ = [
    "linear_search",
    "binary_search",
    "binary_search_recursive",
    "lower_bound",
    "upper_bound",
    "jump_search",
    "exponential_search",
    "interpolation_search",
]


def linear_search(values, target):
    """Index of `target`, or -1. Target: O(n). Works on unsorted data."""
    for i in range(len(values)):
        if values[i] == target:
            return i
    return -1


def binary_search(values, target):
    """Index of `target` in a sorted sequence, or -1. Target: O(log n).

    Write the loop form first. Watch the two classic bugs: `while lo <= hi`
    versus `<`, and computing mid in a way that cannot overflow (irrelevant in
    Python, but worth naming — your students will meet it in C and Java).
    """
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        value = values[mid]                 # one read per step
        if value == target:
            return mid
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binary_search_recursive(values, target, lo=0, hi=None):
    """Same contract, recursive. Compare the call stack against the loop.

    Target: O(log n) time, O(log n) stack — the loop version is O(1) space.
    """
    if hi is None:
        hi = len(values) - 1
    if lo > hi:
        return -1
    mid = lo + (hi - lo) // 2
    value = values[mid]
    if value == target:
        return mid
    if value < target:
        return binary_search_recursive(values, target, mid + 1, hi)
    return binary_search_recursive(values, target, lo, mid - 1)


def lower_bound(values, target):
    """First index where `values[i] >= target` (may equal len(values)).

    The building block for insertion into a sorted list, and for counting
    duplicates: `upper_bound(v, x) - lower_bound(v, x)`.
    """
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(values, target):
    """First index where `values[i] > target` (may equal len(values))."""
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def jump_search(values, target):
    """Step by sqrt(n), then walk back linearly. Target: O(sqrt n).

    Slower than binary search, but it only ever moves forward — which matters
    on storage where seeking backwards is expensive.
    """
    n = len(values)
    if n == 0:
        return -1
    step = max(1, math.isqrt(n))
    prev = 0
    while prev + step < n and values[prev + step - 1] < target:
        prev += step
    for i in range(prev, min(prev + step, n)):
        value = values[i]
        if value == target:
            return i
        if value > target:
            return -1
    return -1


def exponential_search(values, target):
    """Double a bound until it passes `target`, then binary search inside it.

    Target: O(log i) where i is the answer's index — faster than binary search
    when the target is near the front, and it works on unbounded sequences.
    """
    n = len(values)
    if n == 0:
        return -1
    if values[0] == target:
        return 0
    bound = 1
    while bound < n and values[bound] < target:
        bound *= 2
    lo, hi = bound // 2, min(bound, n - 1)
    while lo <= hi:
        mid = (lo + hi) // 2
        value = values[mid]
        if value == target:
            return mid
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def interpolation_search(values, target):
    """Guess the position by linear interpolation rather than halving.

    O(log log n) on uniformly distributed data, but degrades to O(n) when the
    distribution is skewed. A good example of an average case that hides a bad
    worst case.
    """
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        low, high = values[lo], values[hi]          # three reads per step
        if target < low or target > high:
            return -1
        if high == low:
            return lo if low == target else -1
        pos = lo + (target - low) * (hi - lo) // (high - low)
        value = values[pos]
        if value == target:
            return pos
        if value < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1
