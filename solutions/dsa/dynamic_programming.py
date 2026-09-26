"""SOLUTION — try the exercise in `dsa/dynamic_programming.py` first; see `solutions/README.md`.

Dynamic programming — enrichment, not examined (see the study plan).

Each problem walks the same arc: naive recursion, then the same recursion with
a cache, then the table filled bottom-up. The storage rule holds: every cache
and every table is the course `Array` (a table is an `Array` of row `Array`s),
never a `list` or `dict`.
"""

from __future__ import annotations

from dsa.array import Array

__all__ = [
    "fib_naive", "fib_memo", "fib_table",
    "grid_paths", "coin_change", "longest_common_subsequence",
    "edit_distance", "knapsack_01", "longest_increasing_subsequence",
]


def _table(rows, cols, fill=0):
    """A rows x cols table: an Array of row Arrays, every cell `fill`."""
    t = Array(rows)
    for r in range(rows):
        t[r] = Array(cols, fill=fill)
    return t


# -- the three forms, on one problem --------------------------------------


def fib_naive(n):
    """Fibonacci by direct recursion. O(phi^n) — exponential."""
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, cache=None):
    """Same recursion, results cached. O(n) time, O(n) space.

    `cache=None`, not `cache=Array(...)`: a default is built once, when the
    function is defined, and would be shared by every call (Lab 02's trap).
    """
    if cache is None:
        cache = Array(n + 1)          # None marks "not computed yet"
    if n < 2:
        return n
    if cache[n] is None:
        cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]


def fib_table(n):
    """Bottom-up. O(n) time, O(1) space — only the last two values matter."""
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


# -- classic problems ------------------------------------------------------


def grid_paths(rows, cols, blocked=()):
    """Count paths from top-left to bottom-right moving only right or down.

    paths[r][c] = paths[r-1][c] + paths[r][c-1], and 0 on a blocked cell.
    O(rows * cols).
    """
    paths = _table(rows, cols)
    for r in range(rows):
        for c in range(cols):
            if (r, c) in blocked:
                paths[r][c] = 0
            elif r == 0 and c == 0:
                paths[r][c] = 1
            else:
                above = paths[r - 1][c] if r > 0 else 0
                left = paths[r][c - 1] if c > 0 else 0
                paths[r][c] = above + left
    return paths[rows - 1][cols - 1]


def coin_change(coins, amount):
    """Fewest coins summing to `amount`, or -1. O(amount * len(coins)).

    best[x] = 1 + min(best[x - coin]) over the coins that fit.
    """
    impossible = amount + 1                 # more coins than could ever be needed
    best = Array(amount + 1, fill=impossible)
    best[0] = 0
    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x and best[x - coin] + 1 < best[x]:
                best[x] = best[x - coin] + 1
    return -1 if best[amount] == impossible else best[amount]


def longest_common_subsequence(a, b):
    """Length of the LCS. O(len(a) * len(b)).

    L[i][j] is the LCS of a[:i] and b[:j]: one more than L[i-1][j-1] when the
    last characters match, otherwise the better of dropping either one.
    """
    L = _table(len(a) + 1, len(b) + 1)
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L[len(a)][len(b)]


def edit_distance(a, b):
    """Minimum insert/delete/replace operations turning `a` into `b`.

    D[i][j] turns a[:i] into b[:j]. Row 0 and column 0 are pure inserts and
    pure deletes. O(len(a) * len(b)).
    """
    D = _table(len(a) + 1, len(b) + 1)
    for i in range(len(a) + 1):
        D[i][0] = i
    for j in range(len(b) + 1):
        D[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = 1 + min(D[i - 1][j],        # delete a[i-1]
                                  D[i][j - 1],        # insert b[j-1]
                                  D[i - 1][j - 1])    # replace
    return D[len(a)][len(b)]


def knapsack_01(weights, values, capacity):
    """Maximum value within `capacity`, each item at most once.

    One row of `capacity + 1` cells, filled from the RIGHT for each item: going
    right to left means best[w - weight] still holds the value WITHOUT this
    item, so it cannot be taken twice. Left to right would be the unbounded
    knapsack. O(len(items) * capacity) time, O(capacity) space.
    """
    best = Array(capacity + 1, fill=0)
    for weight, value in zip(weights, values):
        for w in range(capacity, weight - 1, -1):
            if best[w - weight] + value > best[w]:
                best[w] = best[w - weight] + value
    return best[capacity]


def longest_increasing_subsequence(values):
    """Length of the longest strictly increasing subsequence. O(n log n).

    tails[k] is the smallest value that can end an increasing subsequence of
    length k + 1. Each value replaces the first tail >= it — a lower_bound, as
    in Week 8 — or extends the list when it is larger than every tail.
    """
    tails = Array(len(values))
    size = 0
    for v in values:
        lo, hi = 0, size                     # lower_bound over tails[0:size]
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < v:
                lo = mid + 1
            else:
                hi = mid
        tails[lo] = v
        if lo == size:
            size += 1
    return size
