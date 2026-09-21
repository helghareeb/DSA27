"""Dynamic programming exercises. Fail until `dsa/dynamic_programming.py` is written."""

import pytest

from dsa import dynamic_programming as dp

pytestmark = pytest.mark.challenge

FIB = [(0, 0), (1, 1), (2, 1), (3, 2), (10, 55), (20, 6765)]


@pytest.mark.parametrize("n,expected", FIB)
def test_fib_naive(n, expected):
    assert dp.fib_naive(n) == expected


@pytest.mark.parametrize("n,expected", FIB + [(90, 2880067194370816120)])
@pytest.mark.parametrize("func", [dp.fib_memo, dp.fib_table], ids=lambda f: f.__name__)
def test_fib_fast_forms(func, n, expected):
    """n=90 is unreachable for the naive version — that is the point."""
    assert func(n) == expected


def test_fib_memo_cache_does_not_leak_between_calls():
    """A mutable default argument would make the second call wrong."""
    assert dp.fib_memo(10) == 55
    assert dp.fib_memo(5) == 5
    assert dp.fib_memo(10) == 55


def test_grid_paths():
    assert dp.grid_paths(1, 1) == 1
    assert dp.grid_paths(2, 2) == 2
    assert dp.grid_paths(3, 3) == 6
    assert dp.grid_paths(3, 7) == 28


def test_grid_paths_with_obstacles():
    assert dp.grid_paths(2, 2, blocked={(0, 1)}) == 1
    assert dp.grid_paths(2, 2, blocked={(0, 1), (1, 0)}) == 0


@pytest.mark.parametrize(
    "coins,amount,expected",
    [([1, 2, 5], 11, 3), ([2], 3, -1), ([1], 0, 0), ([1, 3, 4], 6, 2)],
)
def test_coin_change(coins, amount, expected):
    assert dp.coin_change(coins, amount) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [("ABCBDAB", "BDCABA", 4), ("", "abc", 0), ("abc", "abc", 3), ("abc", "xyz", 0)],
)
def test_longest_common_subsequence(a, b, expected):
    assert dp.longest_common_subsequence(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [("kitten", "sitting", 3), ("", "abc", 3), ("abc", "abc", 0), ("flaw", "lawn", 2)],
)
def test_edit_distance(a, b, expected):
    assert dp.edit_distance(a, b) == expected


def test_knapsack_01():
    assert dp.knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9
    assert dp.knapsack_01([], [], 10) == 0
    assert dp.knapsack_01([5], [10], 3) == 0


def test_knapsack_takes_each_item_at_most_once():
    """A single high-value item must not be taken twice to fill the capacity."""
    assert dp.knapsack_01([2], [10], 10) == 10


@pytest.mark.parametrize(
    "values,expected",
    [([10, 9, 2, 5, 3, 7, 101, 18], 4), ([], 0), ([7], 1), ([5, 4, 3], 1)],
)
def test_longest_increasing_subsequence(values, expected):
    assert dp.longest_increasing_subsequence(values) == expected
