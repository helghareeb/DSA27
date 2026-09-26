"""Question bank, Week 9 practice. Fail until `practice/week09.py` is written."""

import itertools
import random

import pytest

from practice.week09 import (count_inversions, counting_sort_by_key, dutch_flag,
                             sort_by_key, sort_k_sorted)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


class Counted:
    """A value whose comparisons are counted — to check a cost, not only an answer."""

    compares = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        Counted.compares += 1
        return self.v < other.v

    def __gt__(self, other):
        Counted.compares += 1
        return self.v > other.v

    def __le__(self, other):
        Counted.compares += 1
        return self.v <= other.v

    def __ge__(self, other):
        Counted.compares += 1
        return self.v >= other.v


class CountingList:
    """A list that counts every read and write through [] — to check one pass."""

    def __init__(self, values):
        self.values, self.reads, self.writes = list(values), 0, 0

    def __len__(self):
        return len(self.values)

    def __getitem__(self, i):
        self.reads += 1
        return self.values[i]

    def __setitem__(self, i, v):
        self.writes += 1
        self.values[i] = v


class Record:
    """Not comparable at all: a sort that compares items raises TypeError."""

    def __init__(self, name, grade):
        self.name, self.grade = name, grade

    def __repr__(self):
        return f"Record({self.name!r}, {self.grade})"


def brute_inversions(values):
    return sum(1 for i, j in itertools.combinations(range(len(values)), 2)
               if values[i] > values[j])


# -- W9-C1 ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "values,expected",
    [([5, 2, 9, 1, 7, 3], 8), ([1, 2, 3], 0), ([3, 2, 1], 3), ([], 0), ([7], 0),
     ([2, 2, 2], 0), ([1, 3, 2, 3, 1], 4), (list(range(20, 0, -1)), 190)],
)
def test_count_inversions(values, expected):
    assert count_inversions(values) == expected


def test_count_inversions_random():
    rng = random.Random(9)
    for _ in range(30):
        values = [rng.randint(0, 9) for _ in range(rng.randint(0, 25))]
        original = list(values)
        assert count_inversions(values) == brute_inversions(values)
        assert values == original, "count, do not sort: the list must not change"


# -- W9-C2 ----------------------------------------------------------------------


def test_sort_by_key_example():
    assert sort_by_key(["pear", "fig", "apple", "kiwi"], len) == \
        ["fig", "pear", "kiwi", "apple"]


def test_sort_by_key_is_stable_and_compares_keys_only():
    people = [Record("Omar", 2), Record("Sara", 1), Record("Laila", 2), Record("Ali", 1)]
    result = sort_by_key(people, lambda r: r.grade)
    assert [r.name for r in result] == ["Sara", "Ali", "Omar", "Laila"]
    assert [r.name for r in people] == ["Omar", "Sara", "Laila", "Ali"], "do not change items"


def test_sort_by_key_edge_cases():
    assert sort_by_key([], len) == []
    assert sort_by_key(["x"], len) == ["x"]
    assert sort_by_key([3, -1, 2], lambda v: -v) == [3, 2, -1]


def test_sort_by_key_random_matches_stable_sort():
    rng = random.Random(27)
    for _ in range(20):
        items = [(rng.randint(0, 5), i) for i in range(rng.randint(0, 30))]
        assert sort_by_key(items, lambda t: t[0]) == sorted(items, key=lambda t: t[0])


# -- W9-C3 ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "values",
    [[2, 0, 1, 2, 1, 0], [], [1], [2, 2, 0, 0], [0, 0, 0], [2, 1, 0], [1, 1, 2, 0, 2, 1, 0]],
)
def test_dutch_flag(values):
    expected = sorted(values)
    assert dutch_flag(values) is None, "in place: return nothing"
    assert values == expected


def test_dutch_flag_random():
    rng = random.Random(3)
    for _ in range(50):
        values = [rng.randint(0, 2) for _ in range(rng.randint(0, 40))]
        expected = sorted(values)
        dutch_flag(values)
        assert values == expected


def test_dutch_flag_is_one_pass():
    rng = random.Random(1)
    n = 3_000
    counted = CountingList(rng.randint(0, 2) for _ in range(n))
    expected = sorted(counted.values)
    dutch_flag(counted)
    assert counted.values == expected
    assert counted.reads <= 3 * n, "O(n): a few reads per value, never n per value"
    assert counted.writes <= 2 * n


# -- W9-C4 ----------------------------------------------------------------------


def k_sorted(n, k, rng):
    """A list in which every value is at most k places from its sorted place."""
    values = list(range(n))
    for start in range(0, n, k + 1):          # shuffle inside blocks of k + 1
        block = values[start:start + k + 1]
        rng.shuffle(block)
        values[start:start + k + 1] = block
    return values


def test_sort_k_sorted_examples():
    assert sort_k_sorted([2, 1, 4, 3, 6, 5], 1) == [1, 2, 3, 4, 5, 6]
    assert sort_k_sorted([], 3) == []
    assert sort_k_sorted([3, 1, 2], 2) == [1, 2, 3]
    values = [3, 1, 2]
    sort_k_sorted(values, 2)
    assert values == [3, 1, 2], "return a new list"


def test_sort_k_sorted_is_n_times_k():
    rng = random.Random(4)
    n, k = 2_000, 3
    values = k_sorted(n, k, rng)
    Counted.compares = 0
    result = sort_k_sorted([Counted(v) for v in values], k)
    assert [c.v for c in result] == list(range(n))
    assert Counted.compares <= n * (k + 1), "O(nk) comparisons, not O(n^2)"


# -- W9-C5 ----------------------------------------------------------------------


def letter(c):
    return ord(c) - ord("a")


def test_counting_sort_by_key_letters():
    assert counting_sort_by_key(list("banana"), letter, 26) == list("aaabnn")
    assert "".join(counting_sort_by_key(list("mansoura"), letter, 26)) == "aamnorsu"


def test_counting_sort_by_key_is_stable_without_comparing():
    people = [Record("Omar", 2), Record("Sara", 1), Record("Laila", 2), Record("Ali", 1),
              Record("Huda", 0)]
    result = counting_sort_by_key(people, lambda r: r.grade, 3)
    assert [r.name for r in result] == ["Huda", "Sara", "Ali", "Omar", "Laila"]


def test_counting_sort_by_key_edge_cases():
    assert counting_sort_by_key([], letter, 26) == []
    with pytest.raises(ValueError):
        counting_sort_by_key([1, 5], lambda v: v, 5)
    with pytest.raises(ValueError):
        counting_sort_by_key([1, -1], lambda v: v, 5)


def test_counting_sort_by_key_random():
    rng = random.Random(5)
    for _ in range(20):
        items = [(rng.randint(0, 9), i) for i in range(rng.randint(0, 50))]
        assert counting_sort_by_key(items, lambda t: t[0], 10) == \
            sorted(items, key=lambda t: t[0])
