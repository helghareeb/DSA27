"""Searching — basic and advanced.

Every function takes an already-sorted sequence unless it says otherwise.
Plot linear against binary with `viz.complexity.measure` and the difference
between O(n) and O(log n) stops being a claim and becomes a picture.
"""

from __future__ import annotations

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
    raise NotImplementedError


def binary_search(values, target):
    """Index of `target` in a sorted sequence, or -1. Target: O(log n).

    Write the loop form first. Watch the two classic bugs: `while lo <= hi`
    versus `<`, and computing mid in a way that cannot overflow (irrelevant in
    Python, but worth naming — your students will meet it in C and Java).
    """
    raise NotImplementedError


def binary_search_recursive(values, target, lo=0, hi=None):
    """Same contract, recursive. Compare the call stack against the loop.

    Target: O(log n) time, O(log n) stack — the loop version is O(1) space.
    """
    raise NotImplementedError


def lower_bound(values, target):
    """First index where `values[i] >= target` (may equal len(values)).

    The building block for insertion into a sorted list, and for counting
    duplicates: `upper_bound(v, x) - lower_bound(v, x)`.
    """
    raise NotImplementedError


def upper_bound(values, target):
    """First index where `values[i] > target` (may equal len(values))."""
    raise NotImplementedError


def jump_search(values, target):
    """Step by sqrt(n), then walk back linearly. Target: O(sqrt n).

    Slower than binary search, but it only ever moves forward — which matters
    on storage where seeking backwards is expensive.
    """
    raise NotImplementedError


def exponential_search(values, target):
    """Double a bound until it passes `target`, then binary search inside it.

    Target: O(log i) where i is the answer's index — faster than binary search
    when the target is near the front, and it works on unbounded sequences.
    """
    raise NotImplementedError


def interpolation_search(values, target):
    """Guess the position by linear interpolation rather than halving.

    O(log log n) on uniformly distributed data, but degrades to O(n) when the
    distribution is skewed. A good example of an average case that hides a bad
    worst case.
    """
    raise NotImplementedError
