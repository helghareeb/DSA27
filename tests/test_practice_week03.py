"""Question bank, Week 3 practice. Fail until `practice/week03.py` is written."""

import pytest

from dsa.array import Array
from practice.week03 import (
    array_sum,
    count_char,
    is_sorted_rec,
    no_consecutive_ones,
    pascal_row,
)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


def A(*values):
    return Array.from_values(values)


def test_array_sum():
    assert array_sum(A(2, 5, 1)) == 8
    assert array_sum(Array(0)) == 0
    assert array_sum(A(7)) == 7
    assert array_sum(A(1, 2, 3, 4), 2) == 7


@pytest.mark.parametrize(
    "text,ch,expected",
    [("banana", "a", 3), ("", "a", 0), ("banana", "z", 0), ("aaaa", "a", 4)],
)
def test_count_char(text, ch, expected):
    assert count_char(text, ch) == expected


@pytest.mark.parametrize(
    "values,expected",
    [((), True), ((5,), True), ((1, 2, 2, 3), True), ((1, 3, 2), False), ((2, 1), False)],
)
def test_is_sorted_rec(values, expected):
    assert is_sorted_rec(A(*values)) is expected


def test_no_consecutive_ones():
    assert no_consecutive_ones(0) == [""]
    assert no_consecutive_ones(1) == ["0", "1"]
    assert no_consecutive_ones(3) == ["000", "001", "010", "100", "101"]


@pytest.mark.parametrize("n,count", [(1, 2), (2, 3), (3, 5), (4, 8), (5, 13), (10, 144)])
def test_no_consecutive_ones_count(n, count):
    result = no_consecutive_ones(n)
    assert len(result) == count
    assert all("11" not in s and len(s) == n for s in result)


@pytest.mark.parametrize(
    "n,expected",
    [(0, [1]), (1, [1, 1]), (2, [1, 2, 1]), (4, [1, 4, 6, 4, 1]),
     (6, [1, 6, 15, 20, 15, 6, 1])],
)
def test_pascal_row(n, expected):
    assert pascal_row(n) == expected
