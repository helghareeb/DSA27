"""Question bank, Week 12 practice. Fail until `practice/week12.py` is written."""

import random
import statistics

import pytest

from practice.week12 import is_min_heap, join_ropes, merge_sorted, running_medians, top_k

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


class Counted:
    """A number that counts every comparison made with it — to check O(n log k)."""

    comparisons = 0

    def __init__(self, value):
        self.value = value

    def _count(self, other):
        Counted.comparisons += 1
        return other.value if isinstance(other, Counted) else other

    def __lt__(self, other):
        return self.value < self._count(other)

    def __gt__(self, other):
        return self.value > self._count(other)

    def __le__(self, other):
        return self.value <= self._count(other)

    def __ge__(self, other):
        return self.value >= self._count(other)

    def __eq__(self, other):
        return self.value == (other.value if isinstance(other, Counted) else other)

    def __hash__(self):
        return hash(self.value)


@pytest.mark.parametrize(
    "values,expected",
    [([], True), ([7], True), ([1, 3, 2, 7, 4], True), ([1, 3, 2, 2, 4], False),
     ([2, 1], False), ([1, 1, 1], True), ([2, 4, 3, 9, 7, 8, 5, 12, 10], True),
     ([2, 4, 3, 9, 7, 8, 5, 12, 1], False), ([1, 2, 3, 4, 5, 6, 0], False)],
)
def test_is_min_heap(values, expected):
    assert is_min_heap(values) is expected


@pytest.mark.parametrize(
    "values,k,expected",
    [([5, 1, 9, 3, 7, 2], 3, [9, 7, 5]), ([4, 1], 5, [4, 1]), ([4, 1], 0, []),
     ([], 3, []), ([3, 3, 1, 3], 2, [3, 3]), ([1, 2, 3, 4, 5], 5, [5, 4, 3, 2, 1])],
)
def test_top_k(values, k, expected):
    assert top_k(values, k) == expected


def test_top_k_negative():
    with pytest.raises(ValueError):
        top_k([1, 2], -1)


def test_top_k_matches_sorting_on_random_data():
    rng = random.Random(12)
    for _ in range(50):
        values = [rng.randint(0, 50) for _ in range(rng.randint(0, 40))]
        k = rng.randint(0, 45)
        assert top_k(values, k) == sorted(values, reverse=True)[:k]


def test_top_k_is_n_log_k():
    rng = random.Random(3)
    n, k = 1 << 14, 8
    values = [Counted(v) for v in rng.sample(range(10 * n), n)]
    Counted.comparisons = 0
    best = top_k(values, k)
    assert [c.value for c in best] == sorted((c.value for c in values), reverse=True)[:k]
    assert Counted.comparisons <= 3 * n      # sorting would need about 14 n


@pytest.mark.parametrize(
    "lists,expected",
    [([[1, 4, 9], [2, 3], [], [5]], [1, 2, 3, 4, 5, 9]), ([], []), ([[], []], []),
     ([[1, 1, 2], [1, 3]], [1, 1, 1, 2, 3]), ([[5, 6, 7]], [5, 6, 7])],
)
def test_merge_sorted(lists, expected):
    assert merge_sorted(lists) == expected


def test_merge_sorted_leaves_the_lists_alone():
    lists = [[1, 5], [2, 3, 8]]
    merge_sorted(lists)
    assert lists == [[1, 5], [2, 3, 8]]


def test_merge_sorted_random():
    rng = random.Random(7)
    for _ in range(30):
        lists = [sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 8)))
                 for _ in range(rng.randint(0, 6))]
        assert merge_sorted(lists) == sorted(v for part in lists for v in part)


def test_merge_sorted_compares_with_few_lists_in_the_heap():
    """Many values, two lists: each value costs O(log 2), not O(log N)."""
    n = 1 << 13
    lists = [[Counted(v) for v in range(0, 2 * n, 2)],
             [Counted(v) for v in range(1, 2 * n, 2)]]
    Counted.comparisons = 0
    merged = merge_sorted(lists)
    assert [c.value for c in merged] == list(range(2 * n))
    assert Counted.comparisons <= 4 * 2 * n


@pytest.mark.parametrize(
    "lengths,expected",
    [([4, 3, 2, 6], 29), ([7], 0), ([], 0), ([1, 1], 2), ([5, 5, 5, 5], 40),
     ([1, 2, 3, 4, 5], 33)],
)
def test_join_ropes(lengths, expected):
    assert join_ropes(lengths) == expected


def test_join_ropes_leaves_the_input_alone():
    lengths = [4, 3, 2, 6]
    join_ropes(lengths)
    assert lengths == [4, 3, 2, 6]


@pytest.mark.parametrize(
    "values,expected",
    [([5, 15, 1, 3], [5, 10.0, 5, 4.0]), ([], []), ([7], [7]), ([2, 2, 2], [2, 2.0, 2]),
     ([1, 2, 3, 4, 5], [1, 1.5, 2, 2.5, 3]), ([5, 4, 3, 2, 1], [5, 4.5, 4, 3.5, 3])],
)
def test_running_medians(values, expected):
    assert running_medians(values) == pytest.approx(expected)


def test_running_medians_random():
    rng = random.Random(5)
    values = [rng.randint(-100, 100) for _ in range(300)]
    expected = [statistics.median(values[:i]) for i in range(1, len(values) + 1)]
    assert running_medians(values) == pytest.approx(expected)
