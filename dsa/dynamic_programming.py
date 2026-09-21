"""Dynamic programming.

The teaching arc for each problem is the same three steps, and it is worth
making students walk all three every time:

  1. **naive recursion** — obviously correct, exponentially slow
  2. **memoised** (top-down) — same code, a cache, suddenly polynomial
  3. **tabulated** (bottom-up) — the recursion turned inside out, O(1) space
     where the recurrence allows it

`fib_naive` versus `fib_memo` through `viz.complexity.measure` is the most
convincing thirty seconds in the whole course — just keep n small for the
naive one.
"""

from __future__ import annotations

__all__ = [
    "fib_naive", "fib_memo", "fib_table",
    "grid_paths", "coin_change", "longest_common_subsequence",
    "edit_distance", "knapsack_01", "longest_increasing_subsequence",
]


# -- the three forms, on one problem --------------------------------------


def fib_naive(n):
    """Fibonacci by direct recursion. O(phi^n) — exponential.

    Count the calls. F(30) is roughly 2.7 million, and almost all of them
    recompute something already known.
    """
    raise NotImplementedError


def fib_memo(n, cache=None):
    """Same recursion, results cached. O(n) time, O(n) space."""
    raise NotImplementedError


def fib_table(n):
    """Bottom-up. O(n) time, O(1) space — only the last two values matter."""
    raise NotImplementedError


# -- classic problems ------------------------------------------------------


def grid_paths(rows, cols, blocked=()):
    """Count paths from top-left to bottom-right moving only right or down.

    O(rows * cols). The DP table is literally the grid, so
    `viz.draw.draw_array` on each row shows it filling in.
    """
    raise NotImplementedError


def coin_change(coins, amount):
    """Fewest coins summing to `amount`, or -1 if impossible. O(amount * len(coins)).

    Challenge: return the actual coins, not just the count. That means storing
    a choice alongside each cell and walking it back — the same reconstruction
    idea every DP problem needs.
    """
    raise NotImplementedError


def longest_common_subsequence(a, b):
    """Length of the LCS of two sequences. O(len(a) * len(b)).

    Challenge: return the subsequence itself by backtracking through the table.
    """
    raise NotImplementedError


def edit_distance(a, b):
    """Minimum insert/delete/replace operations turning `a` into `b`.

    O(len(a) * len(b)). This is what spell checkers and `diff` are built on.
    """
    raise NotImplementedError


def knapsack_01(weights, values, capacity):
    """Maximum value within `capacity`, each item taken at most once.

    O(len(items) * capacity) — "pseudo-polynomial", because it is linear in
    the *value* of capacity, not in the number of bits used to write it. A
    genuinely useful distinction to raise here.
    """
    raise NotImplementedError


def longest_increasing_subsequence(values):
    """Length of the longest strictly increasing subsequence.

    O(n^2) with the obvious DP. Challenge: O(n log n) using `lower_bound` from
    `dsa.searching` — a satisfying payoff for having written it earlier.
    """
    raise NotImplementedError
