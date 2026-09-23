"""Question bank, Week 2 practice. Fail until `practice/week02.py` is written."""

import pytest

from dsa.array import Array
from practice.week02 import count_occurrences, prefix_sums, remove_all, two_sum_sorted

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


def A(*values):
    return Array.from_values(values)


def test_count_occurrences():
    assert count_occurrences(A(1, 2, 1, 1), 1) == 3
    assert count_occurrences(A(1, 2, 1, 1), 5) == 0
    assert count_occurrences(Array(0), 1) == 0
    assert count_occurrences(A(1, 1, 1, None), 1, size=2) == 2
    assert count_occurrences(A(1, None, None), None, size=1) == 0


def test_remove_all():
    arr = A(3, 1, 3, 2, 3, None)
    assert remove_all(arr, 5, 3) == 2
    assert list(arr) == [1, 2, None, None, None, None]


def test_remove_all_nothing_to_remove():
    arr = A(1, 2, 3)
    assert remove_all(arr, 3, 9) == 3
    assert list(arr) == [1, 2, 3]


def test_remove_all_everything():
    arr = A(7, 7, 7)
    assert remove_all(arr, 3, 7) == 0
    assert list(arr) == [None, None, None]


def test_remove_all_is_one_pass():
    # 20,000 elements, half of them removed. O(n) is instant; removing one at a
    # time with shifting is O(n^2) and takes long enough to notice.
    n = 20_000
    arr = Array(n)
    for i in range(n):
        arr[i] = i % 2
    assert remove_all(arr, n, 0) == n // 2
    assert arr[0] == 1 and arr[n // 2 - 1] == 1 and arr[n // 2] is None


def _check_pair(arr, target, pair):
    i, j = pair
    assert 0 <= i < j < len(arr)
    assert arr[i] + arr[j] == target


def test_two_sum_sorted_finds_a_pair():
    arr = A(1, 3, 4, 6, 8, 11)
    _check_pair(arr, 10, two_sum_sorted(arr, 10))
    _check_pair(arr, 4, two_sum_sorted(arr, 4))
    _check_pair(arr, 19, two_sum_sorted(arr, 19))


def test_two_sum_sorted_none():
    assert two_sum_sorted(A(1, 3, 4, 6), 100) is None
    assert two_sum_sorted(A(5), 10) is None
    assert two_sum_sorted(Array(0), 0) is None


def test_two_sum_sorted_uses_two_different_slots():
    assert two_sum_sorted(A(5, 6), 10) is None
    _check_pair(A(5, 5), 10, two_sum_sorted(A(5, 5), 10))


def test_two_sum_sorted_is_linear():
    n = 20_000
    arr = Array(n)
    for i in range(n):
        arr[i] = 2 * i                      # all even, so an odd target never matches
    assert two_sum_sorted(arr, 7) is None


def test_prefix_sums():
    result = prefix_sums(A(2, 5, 1, 4))
    assert isinstance(result, Array)
    assert list(result) == [2, 7, 8, 12]
    assert list(prefix_sums(Array(0))) == []
    assert list(prefix_sums(A(-1, 1, -1))) == [-1, 0, -1]


def test_prefix_sums_leaves_the_input_alone():
    arr = A(1, 2, 3)
    prefix_sums(arr)
    assert list(arr) == [1, 2, 3]
