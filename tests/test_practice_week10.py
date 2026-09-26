"""Question bank, Week 10 practice. Fail until `practice/week10.py` is written."""

import math
import random
import sys

import pytest

from practice.week10 import (count_inversions, kth_smallest, merge_k_sorted, merge_sort_bottom_up,
                             sort_colours)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


class Counted:
    """A number that counts every comparison made on it — to check the cost."""

    comparisons = 0

    def __init__(self, value, tag=""):
        self.value, self.tag = value, tag

    def __lt__(self, other):
        Counted.comparisons += 1
        return self.value < other.value

    def __le__(self, other):
        Counted.comparisons += 1
        return self.value <= other.value

    def __gt__(self, other):
        Counted.comparisons += 1
        return self.value > other.value

    def __ge__(self, other):
        Counted.comparisons += 1
        return self.value >= other.value

    def __eq__(self, other):
        Counted.comparisons += 1
        return self.value == other.value

    __hash__ = None


def counted(values):
    Counted.comparisons = 0
    return [Counted(v) for v in values]


def plain(items):
    return [c.value for c in items]


class CountingList(list):
    """A list that counts every values[i] read and every values[i] = x write."""

    def __init__(self, values):
        super().__init__(values)
        self.reads = self.writes = 0

    def __getitem__(self, i):
        self.reads += 1
        return super().__getitem__(i)

    def __setitem__(self, i, value):
        self.writes += 1
        super().__setitem__(i, value)


# -- W10-C1 merge_k_sorted -----------------------------------------------------


@pytest.mark.parametrize(
    "lists,expected",
    [([[1, 4, 9], [2, 3], [], [5]], [1, 2, 3, 4, 5, 9]), ([], []), ([[]], []), ([[], []], []),
     ([[3, 5]], [3, 5]), ([[1, 1], [1], [0, 1]], [0, 1, 1, 1, 1]),
     ([[5], [4], [3], [2], [1]], [1, 2, 3, 4, 5])],
)
def test_merge_k_sorted(lists, expected):
    before = [list(run) for run in lists]
    assert merge_k_sorted(lists) == expected
    assert lists == before, "do not change the input lists"


def test_merge_k_sorted_random():
    rng = random.Random(10)
    for _ in range(50):
        lists = [sorted(rng.choices(range(30), k=rng.randint(0, 8))) for _ in range(rng.randint(1, 9))]
        assert merge_k_sorted(lists) == sorted(v for run in lists for v in run)


def test_merge_k_sorted_is_stable():
    lists = [[Counted(1, "a"), Counted(2, "a")], [Counted(1, "b")], [Counted(1, "c"), Counted(2, "c")]]
    result = merge_k_sorted(lists)
    assert [(c.value, c.tag) for c in result] == [(1, "a"), (1, "b"), (1, "c"), (2, "a"), (2, "c")]


def test_merge_k_sorted_is_n_log_k():
    k, length = 64, 64                               # N = 4096 values in 64 lists
    rng = random.Random(10)
    lists = [sorted(rng.sample(range(100_000), length)) for _ in range(k)]
    items = [counted(run) for run in lists]
    result = merge_k_sorted(items)
    assert plain(result) == sorted(v for run in lists for v in run)
    n = k * length
    assert Counted.comparisons <= n * math.ceil(math.log2(k)) + n, (
        "merging one list after another is O(N k): merge in pairs")


# -- W10-C2 count_inversions ---------------------------------------------------


@pytest.mark.parametrize(
    "values,expected",
    [([2, 4, 1, 3, 5], 3), ([1, 2, 3], 0), ([3, 2, 1], 3), ([], 0), ([7], 0), ([2, 2, 2], 0),
     ([1, 3, 2, 3, 1], 4), ([8, 4, 2, 1], 6)],
)
def test_count_inversions(values, expected):
    assert count_inversions(values) == expected


def test_count_inversions_random_against_brute_force():
    rng = random.Random(10)
    for _ in range(40):
        values = [rng.randint(0, 20) for _ in range(rng.randint(0, 30))]
        brute = sum(1 for i in range(len(values)) for j in range(i + 1, len(values))
                    if values[i] > values[j])
        assert count_inversions(values) == brute


def test_count_inversions_is_n_log_n():
    n = 4096
    items = counted(range(n, 0, -1))                 # reversed: n(n-1)/2 inversions
    assert count_inversions(items) == n * (n - 1) // 2
    assert Counted.comparisons <= 2 * n * math.log2(n), "checking every pair is O(n^2)"


# -- W10-C3 kth_smallest -------------------------------------------------------


@pytest.mark.parametrize("k,expected", [(1, 1), (2, 2), (3, 4), (4, 7), (5, 9)])
def test_kth_smallest(k, expected):
    values = [7, 2, 9, 4, 1]
    assert kth_smallest(values, k) == expected
    assert values == [7, 2, 9, 4, 1], "do not change the caller's list"


def test_kth_smallest_with_duplicates():
    values = [5, 1, 5, 3, 5, 1]
    assert [kth_smallest(values, k) for k in range(1, 7)] == [1, 1, 3, 5, 5, 5]


@pytest.mark.parametrize("k", [0, 6, -1])
def test_kth_smallest_rejects_bad_k(k):
    with pytest.raises(ValueError):
        kth_smallest([7, 2, 9, 4, 1], k)


def test_kth_smallest_random():
    rng = random.Random(10)
    for _ in range(40):
        values = [rng.randint(-50, 50) for _ in range(rng.randint(1, 40))]
        k = rng.randint(1, len(values))
        assert kth_smallest(values, k) == sorted(values)[k - 1]


@pytest.mark.parametrize("order", ["random", "sorted"])
def test_kth_smallest_is_linear_on_average(order):
    n = 4096
    values = random.Random(10).sample(range(10 * n), n)
    if order == "sorted":
        values.sort()
    items = counted(values)
    assert kth_smallest(items, n // 2).value == sorted(values)[n // 2 - 1]
    assert Counted.comparisons <= 8 * n, "sorting first is O(n log n): partition, keep one side"


# -- W10-C4 sort_colours -------------------------------------------------------


@pytest.mark.parametrize(
    "values",
    [[2, 0, 2, 1, 1, 0], [], [1], [2, 1, 0], [0, 0, 0], [2, 2, 2], [1, 0], [2, 0, 1, 2, 0, 1, 1]],
)
def test_sort_colours(values):
    expected = sorted(values)
    assert sort_colours(values) is None, "sort in place and return None, like list.sort"
    assert values == expected


def test_sort_colours_random():
    rng = random.Random(10)
    for _ in range(50):
        values = rng.choices([0, 1, 2], k=rng.randint(0, 40))
        expected = sorted(values)
        sort_colours(values)
        assert values == expected


def test_sort_colours_is_one_pass():
    rng = random.Random(10)
    n = 3000
    values = CountingList(rng.choices([0, 1, 2], k=n))
    expected = sorted(values)
    sort_colours(values)
    assert list(values) == expected
    assert values.reads <= 3 * n and values.writes <= 2 * n, "one pass, O(n): no sorting"


# -- W10-C5 merge_sort_bottom_up ----------------------------------------------


@pytest.mark.parametrize(
    "values",
    [[5, 2, 9, 1, 7], [], [1], [2, 1], [3, 3, 3], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1],
     [0, -3, 7, -1, 2], [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1]],
)
def test_merge_sort_bottom_up(values):
    before = list(values)
    assert merge_sort_bottom_up(values) == sorted(values)
    assert values == before, "return a new list; do not change the caller's"


def test_merge_sort_bottom_up_random():
    rng = random.Random(10)
    for _ in range(60):
        values = [rng.randint(-50, 50) for _ in range(rng.randint(0, 70))]
        assert merge_sort_bottom_up(values) == sorted(values)


def test_merge_sort_bottom_up_is_stable():
    keys = [3, 1, 3, 2, 1, 2, 3, 1, 2]
    items = [Counted(k, str(i)) for i, k in enumerate(keys)]
    result = merge_sort_bottom_up(items)
    expected = sorted(((k, i) for i, k in enumerate(keys)))
    assert [(c.value, int(c.tag)) for c in result] == expected


def test_merge_sort_bottom_up_is_n_log_n():
    n = 3000                                         # not a power of two: short last runs
    values = random.Random(10).sample(range(10 * n), n)
    items = counted(values)
    assert plain(merge_sort_bottom_up(items)) == sorted(values)
    assert Counted.comparisons <= n * math.ceil(math.log2(n))


def test_merge_sort_bottom_up_does_not_recurse():
    """No function may be running twice at once: loops, not recursive calls."""
    active, deepest = {}, [0]

    def watch(frame, event, arg):
        code = frame.f_code
        if event == "call":
            active[code] = active.get(code, 0) + 1
            deepest[0] = max(deepest[0], active[code])
        elif event == "return":
            active[code] -= 1

    values = random.Random(10).sample(range(1000), 64)
    sys.setprofile(watch)
    try:
        result = merge_sort_bottom_up(values)
    finally:
        sys.setprofile(None)
    assert result == sorted(values)
    assert deepest[0] <= 1, "a function called itself: write the passes as loops"
