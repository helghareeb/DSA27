"""Question bank, Week 8 practice. Fail until `practice/week08.py` is written."""

import math

import pytest

from practice.week08 import closest_value, find_peak, integer_sqrt, min_capacity, search_rotated

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


class CountingReads:
    """A read-only list that counts every values[i] — to check O(log n)."""

    def __init__(self, values):
        self.values, self.reads = list(values), 0

    def __len__(self):
        return len(self.values)

    def __getitem__(self, i):
        self.reads += 1
        return self.values[i]


def log_budget(n):
    """Generous: a few reads per halving, never anything like n."""
    return 4 * (math.floor(math.log2(max(n, 1))) + 2)


@pytest.mark.parametrize(
    "values,target,expected",
    [([5, 7, 9, 11, 1, 3], 3, 5), ([5, 7, 9, 11, 1, 3], 5, 0), ([5, 7, 9, 11, 1, 3], 11, 3),
     ([5, 7, 9, 11, 1, 3], 6, -1), ([1, 3, 5], 3, 1), ([3, 1], 1, 1), ([], 4, -1), ([2], 2, 0)],
)
def test_search_rotated(values, target, expected):
    assert search_rotated(values, target) == expected


def test_search_rotated_every_rotation():
    base = list(range(0, 40, 2))
    for k in range(len(base)):
        rotated = base[k:] + base[:k]
        for target in range(-1, 41):
            expected = rotated.index(target) if target in rotated else -1
            assert search_rotated(rotated, target) == expected


def test_search_rotated_is_logarithmic():
    n = 1 << 16
    counted = CountingReads(list(range(n // 3, n)) + list(range(n // 3)))
    assert search_rotated(counted, 12_345) == 12_345 + n - n // 3
    assert counted.reads <= log_budget(n)


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 8, 9, 10, 15, 16, 17, 99, 100, 10**12, 10**18 + 7])
def test_integer_sqrt(n):
    assert integer_sqrt(n) == math.isqrt(n)


def test_integer_sqrt_negative():
    with pytest.raises(ValueError):
        integer_sqrt(-1)


@pytest.mark.parametrize(
    "values", [[1, 3, 20, 4, 1, 0], [5], [1, 2], [2, 1], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1],
               [3, 3, 3], [1, 5, 2, 6, 3, 7, 4]],
)
def test_find_peak(values):
    i = find_peak(values)
    left = values[i - 1] if i > 0 else float("-inf")
    right = values[i + 1] if i + 1 < len(values) else float("-inf")
    assert values[i] >= left and values[i] >= right


def test_find_peak_is_logarithmic():
    n = 1 << 16
    counted = CountingReads(list(range(n)))          # the only peak is the last
    assert find_peak(counted) == n - 1
    assert counted.reads <= log_budget(n)


@pytest.mark.parametrize(
    "values,target,expected",
    [([1, 4, 9, 16], 6, 4), ([1, 4, 9, 16], 7, 9), ([1, 4, 9, 16], 50, 16),
     ([1, 4, 9, 16], -3, 1), ([1, 4, 9, 16], 9, 9), ([1, 3], 2, 1), ([7], 100, 7)],
)
def test_closest_value(values, target, expected):
    assert closest_value(values, target) == expected


def test_closest_value_is_logarithmic():
    n = 1 << 16
    counted = CountingReads(range(0, 3 * n, 3))
    assert closest_value(counted, 3 * 777 + 1) == 3 * 777
    assert counted.reads <= log_budget(n)


@pytest.mark.parametrize(
    "weights,days,expected",
    [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 15), ([3, 2, 2, 4, 1, 4], 3, 6),
     ([1, 2, 3, 1, 1], 4, 3), ([7], 1, 7), ([4, 4, 4], 3, 4), ([4, 4, 4], 1, 12)],
)
def test_min_capacity(weights, days, expected):
    assert min_capacity(weights, days) == expected


def test_min_capacity_is_n_log_s():
    weights = [1_000_000] * 20_000                   # S = 2e10: trying every capacity is hopeless
    assert min_capacity(weights, 7) == 1_000_000 * math.ceil(20_000 / 7)
