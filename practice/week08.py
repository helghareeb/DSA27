"""Question bank, Week 8 — searching. Problems W8-C1 to W8-C5.

Questions:  docs/question-bank/week08-questions.md
Tests:      tests/test_practice_week08.py

Every problem is a binary search in disguise, and every one must run in
O(log n) — the tests count how many elements you read. Write the searches
yourself: do not call Python's `bisect`, `list.index`, `in` or `sorted`. You
may call your own functions from `dsa/searching.py`.
"""


def search_rotated(values, target):
    """W8-C1. Index of `target` in a sorted list that has been rotated, or -1.

    A rotated list is a sorted one cut in two and the halves swapped:
    [1, 3, 5, 7, 9, 11] rotated by 2 is [5, 7, 9, 11, 1, 3]. The values are
    distinct.

    search_rotated([5, 7, 9, 11, 1, 3], 3)  -> 5
    search_rotated([5, 7, 9, 11, 1, 3], 6)  -> -1

    O(log n). Hint: whichever half you cut, one of the two is sorted.
    """
    raise NotImplementedError


def integer_sqrt(n):
    """W8-C2. The largest integer r with r * r <= n, for n >= 0.

    integer_sqrt(10) -> 3;  integer_sqrt(16) -> 4;  integer_sqrt(0) -> 0

    Binary search on the ANSWER: r lies somewhere in 0..n, and the test
    r * r <= n is true up to the answer and false after it. O(log n)
    multiplications. Do not use math.sqrt, math.isqrt or ** 0.5.
    Raise ValueError for a negative n.
    """
    raise NotImplementedError


def find_peak(values):
    """W8-C3. The index of a peak: an element not smaller than its neighbours.

    The list is not sorted; it is non-empty, and positions outside it count as
    minus infinity, so a peak always exists. If there are several, return any.

    find_peak([1, 3, 20, 4, 1, 0]) -> 2
    find_peak([5])                 -> 0

    O(log n). Hint: compare values[mid] with values[mid + 1] — which side must
    hold a peak?
    """
    raise NotImplementedError


def closest_value(values, target):
    """W8-C4. The value in a sorted, non-empty list closest to `target`.

    On a tie, return the smaller value.

    closest_value([1, 4, 9, 16], 6)  -> 4
    closest_value([1, 4, 9, 16], 7)  -> 9
    closest_value([1, 4, 9, 16], 50) -> 16

    O(log n): find where target would be inserted; the answer is one of its two
    neighbours.
    """
    raise NotImplementedError


def min_capacity(weights, days):
    """W8-C5. The smallest ship capacity that delivers every package in time.

    Packages must be shipped in the given order; each day the ship takes the
    next packages while their total fits the capacity. Return the smallest
    capacity that ships them all within `days` days (days >= 1, weights
    non-empty, every weight positive).

    min_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) -> 15

    Binary search on the answer, between max(weights) and sum(weights). Each
    check "can capacity c do it in `days` days?" is one O(n) pass, so the whole
    is O(n log S), where S = sum(weights).
    """
    raise NotImplementedError
