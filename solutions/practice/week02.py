"""SOLUTION — try the problems in `practice/week02.py` first; see `solutions/README.md`.

Question bank, Week 2 — complexity and the Array. Problems W2-C1 to W2-C4.

Questions:  docs/question-bank/week02-questions.md
Tests:      tests/test_practice_week02.py

Work on the course `Array` with indices only: no slicing, no converting to a
`list`, no list scratch space. Each docstring states the target complexity —
meeting it is part of the problem.
"""

from dsa.array import Array


def count_occurrences(arr, target, size=None):
    """W2-C1. How many of the first `size` slots (all, if None) equal `target`.

    Target: O(n) time, O(1) extra space.
    """
    n = len(arr) if size is None else size
    count = 0
    for i in range(n):
        if arr[i] == target:
            count += 1
    return count


def remove_all(arr, size, target):
    """W2-C2. Remove every occurrence of `target` from the first `size` slots,
    keeping the order of the rest. Return the new size; set the freed slots at
    the end to None.

    arr = [3, 1, 3, 2, 3, None], size 5, target 3  ->  returns 2,
    arr becomes [1, 2, None, None, None, None]

    Target: O(n) time and O(1) extra space — ONE pass. Calling a remove-at-index
    function once per occurrence is O(n^2); do not.
    """
    write = 0                             # next slot to keep a value in
    for read in range(size):
        if arr[read] != target:
            arr[write] = arr[read]
            write += 1
    for i in range(write, size):          # clear the freed tail
        arr[i] = None
    return write


def two_sum_sorted(arr, target):
    """W2-C3. `arr` is sorted in non-decreasing order. Return a pair of indices
    (i, j) with i < j and arr[i] + arr[j] == target, or None if there is none.
    Any valid pair is accepted.

    Target: O(n) time, O(1) extra space. The O(n^2) "try every pair" answer is
    correct and too slow.
    """
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        total = arr[lo] + arr[hi]
        if total == target:
            return (lo, hi)
        if total < target:
            lo += 1                       # need a bigger sum
        else:
            hi -= 1                       # need a smaller sum
    return None


def prefix_sums(arr):
    """W2-C4. A NEW Array p of the same length with p[i] = arr[0] + ... + arr[i].

    prefix_sums([2, 5, 1, 4]) -> [2, 7, 8, 12]

    Target: O(n). (Then the sum of any range arr[i..j] is p[j] - p[i-1]: O(1).)
    """
    result = Array(len(arr))
    running = 0
    for i in range(len(arr)):
        running += arr[i]
        result[i] = running
    return result
