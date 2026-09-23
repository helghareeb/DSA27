"""Question bank, Week 1 practice. Fail until `practice/week01.py` is written."""

import pytest

from practice.week01 import compress, count_vowels, is_anagram, second_largest

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


@pytest.mark.parametrize(
    "text,expected",
    [("Data Structures", 5), ("rhythm", 0), ("", 0), ("AEIOUaeiou", 10), ("Mansoura", 4)],
)
def test_count_vowels(text, expected):
    assert count_vowels(text) == expected


@pytest.mark.parametrize(
    "values,expected",
    [([4, 9, 2, 9, 7], 7), ([1, 2], 1), ([2, 1], 1), ([-5, -1, -3], -3), ([3, 3, 1, 3], 1)],
)
def test_second_largest(values, expected):
    assert second_largest(values) == expected


@pytest.mark.parametrize("values", [[], [5], [5, 5], [7, 7, 7]])
def test_second_largest_needs_two_distinct_values(values):
    with pytest.raises(ValueError):
        second_largest(values)


@pytest.mark.parametrize(
    "text,expected",
    [("aaabcc", "a3b1c2"), ("", ""), ("a", "a1"), ("abc", "a1b1c1"), ("zzzzzzzzzzzz", "z12"),
     ("aabaa", "a2b1a2")],
)
def test_compress(text, expected):
    assert compress(text) == expected


@pytest.mark.parametrize(
    "first,second,expected",
    [("Dormitory", "dirty room", True), ("listen", "silent", True), ("abc", "abcc", False),
     ("", "", True), ("ab", "a b", True), ("aab", "abb", False)],
)
def test_is_anagram(first, second, expected):
    assert is_anagram(first, second) is expected
