"""Question bank, Week 13 practice. Fail until `practice/week13.py` is written."""

import random

import pytest

from practice.week13 import (count_subarrays_with_sum, first_repeated, group_anagrams,
                             longest_distinct_run, two_sum)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


# -- brute-force references: obviously right, and O(n^2) ----------------------

def slow_two_sum(values, target):
    for j in range(len(values)):
        for i in range(j):
            if values[i] + values[j] == target:
                return (i, j)
    return None


def slow_first_repeated(items):
    for j in range(len(items)):
        if items[j] in items[:j]:
            return items[j]
    return None


def slow_longest(text):
    best = 0
    for i in range(len(text)):
        for j in range(i, len(text) + 1):
            if len(set(text[i:j])) == j - i:
                best = max(best, j - i)
    return best


def slow_count(values, k):
    return sum(1 for i in range(len(values)) for j in range(i + 1, len(values) + 1)
               if sum(values[i:j]) == k)


# -- W13-C1 -------------------------------------------------------------------

@pytest.mark.parametrize(
    "values,target,expected",
    [([2, 7, 11, 15], 9, (0, 1)), ([3, 2, 4], 6, (1, 2)), ([3, 3], 6, (0, 1)),
     ([1, 2], 10, None), ([], 0, None), ([5], 10, None), ([1, 5, 5, 1], 6, (0, 1)),
     ([4, 4, 4], 8, (0, 1)), ([-3, 7, 10], 7, (0, 2))],
)
def test_two_sum(values, target, expected):
    assert two_sum(values, target) == expected


def test_two_sum_agrees_with_brute_force():
    rng = random.Random(13)
    for _ in range(300):
        values = [rng.randint(-10, 10) for _ in range(rng.randint(0, 12))]
        target = rng.randint(-15, 15)
        assert two_sum(values, target) == slow_two_sum(values, target), (values, target)


def test_two_sum_is_linear():
    n = 20_000
    values = list(range(n))
    assert two_sum(values, 2 * n - 3) == (n - 2, n - 1)   # the only pair: the last two
    assert two_sum(values, -1) is None


# -- W13-C2 -------------------------------------------------------------------

@pytest.mark.parametrize(
    "items,expected",
    [(["a", "b", "c", "b", "a"], "b"), ([1, 2, 3], None), ([], None), ([7, 7], 7),
     ([1, 2, 3, 4, 1, 2], 1), ([(1, 2), (2, 1), (1, 2)], (1, 2))],
)
def test_first_repeated(items, expected):
    assert first_repeated(items) == expected


def test_first_repeated_agrees_with_brute_force():
    rng = random.Random(1300)
    for _ in range(300):
        items = [rng.randint(0, 15) for _ in range(rng.randint(0, 10))]
        assert first_repeated(items) == slow_first_repeated(items), items


def test_first_repeated_is_linear():
    n = 30_000
    assert first_repeated(list(range(n)) + [n - 1]) == n - 1


# -- W13-C3 -------------------------------------------------------------------

def test_group_anagrams_example():
    assert group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [
        ["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]


@pytest.mark.parametrize(
    "words,expected",
    [([], []), (["a"], [["a"]]), (["", ""], [["", ""]]),
     (["listen", "silent", "enlist", "google"], [["listen", "silent", "enlist"], ["google"]]),
     (["ab", "ba", "abc", "ab"], [["ab", "ba", "ab"], ["abc"]])],
)
def test_group_anagrams(words, expected):
    assert group_anagrams(words) == expected


def test_group_anagrams_is_fast():
    words = [chr(0x4E00 + i) + "ab" for i in range(20_000)] * 2   # 20,000 groups of two
    groups = group_anagrams(words)
    assert len(groups) == 20_000
    assert groups[123] == [chr(0x4E00 + 123) + "ab"] * 2


# -- W13-C4 -------------------------------------------------------------------

@pytest.mark.parametrize(
    "text,expected",
    [("abcabcbb", 3), ("pwwkew", 3), ("", 0), ("bbbbb", 1), ("abcdef", 6),
     ("abba", 2), ("dvdf", 3), ("tmmzuxt", 5)],
)
def test_longest_distinct_run(text, expected):
    assert longest_distinct_run(text) == expected


def test_longest_distinct_run_agrees_with_brute_force():
    rng = random.Random(7)
    for _ in range(300):
        text = "".join(rng.choice("abcde") for _ in range(rng.randint(0, 14)))
        assert longest_distinct_run(text) == slow_longest(text), text


def test_longest_distinct_run_is_linear():
    text = "".join(chr(0x4E00 + i) for i in range(20_000))   # 20,000 distinct characters
    assert longest_distinct_run(text + text) == 20_000


# -- W13-C5 -------------------------------------------------------------------

@pytest.mark.parametrize(
    "values,k,expected",
    [([1, 1, 1], 2, 2), ([1, 2, 3], 3, 2), ([1, -1, 0], 0, 3), ([], 0, 0), ([5], 5, 1),
     ([0, 0, 0], 0, 6), ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4)],
)
def test_count_subarrays_with_sum(values, k, expected):
    assert count_subarrays_with_sum(values, k) == expected


def test_count_subarrays_agrees_with_brute_force():
    rng = random.Random(31)
    for _ in range(300):
        values = [rng.randint(-3, 3) for _ in range(rng.randint(0, 10))]
        k = rng.randint(-4, 4)
        assert count_subarrays_with_sum(values, k) == slow_count(values, k), (values, k)


def test_count_subarrays_is_linear():
    n = 20_000
    assert count_subarrays_with_sum([0] * n, 0) == n * (n + 1) // 2
