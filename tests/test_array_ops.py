"""Array operation exercises. Fail until `dsa/array_ops.py` is written."""

import pytest

from dsa.array import Array
from dsa.array_ops import (
    find,
    insert_at,
    is_sorted,
    merge_sorted,
    remove_at,
    resized,
    reverse_in_place,
    rotate_left,
    transpose_flat,
)

pytestmark = pytest.mark.challenge


def A(*values):
    return Array.from_values(values)


# -- reading ----------------------------------------------------------------


def test_find():
    assert find(A(4, 7, 7), 7) == 1
    assert find(A(4, 7, 7), 4) == 0
    assert find(A(4, 7, 7), 9) == -1
    assert find(Array(0), 1) == -1


def test_find_respects_size():
    arr = A(1, 2, 3, None, None)
    assert find(arr, 3, size=3) == 2
    assert find(arr, None, size=3) == -1
    assert find(arr, None) == 3


def test_is_sorted():
    assert is_sorted(Array(0))
    assert is_sorted(A(5))
    assert is_sorted(A(1, 2, 2, 3))
    assert not is_sorted(A(1, 3, 2))
    assert is_sorted(A(1, 2, 0, 0), size=2)
    assert not is_sorted(A(2, 1, 5), size=2)


# -- writing ----------------------------------------------------------------


def test_insert_at_builds_up_an_array():
    arr = Array(5)
    size = 0
    size = insert_at(arr, size, 0, "b")
    size = insert_at(arr, size, 0, "a")
    size = insert_at(arr, size, 2, "d")
    size = insert_at(arr, size, 2, "c")
    assert size == 4
    assert list(arr) == ["a", "b", "c", "d", None]


def test_insert_at_fills_to_capacity_then_overflows():
    arr = Array(3)
    size = 0
    for value in (1, 2, 3):
        size = insert_at(arr, size, size, value)
    assert list(arr) == [1, 2, 3]
    with pytest.raises(OverflowError):
        insert_at(arr, size, 0, 99)
    assert list(arr) == [1, 2, 3]


@pytest.mark.parametrize("index", [-1, 3, 10])
def test_insert_at_rejects_bad_index(index):
    arr = A(1, 2, None, None)
    with pytest.raises(IndexError):
        insert_at(arr, 2, index, 99)


def test_remove_at():
    arr = A("a", "b", "c", "d", None)
    assert remove_at(arr, 4, 1) == "b"
    assert list(arr) == ["a", "c", "d", None, None]
    assert remove_at(arr, 3, 2) == "d"
    assert list(arr) == ["a", "c", None, None, None]
    assert remove_at(arr, 2, 0) == "a"
    assert list(arr) == ["c", None, None, None, None]


@pytest.mark.parametrize("index", [-1, 2, 5])
def test_remove_at_rejects_bad_index(index):
    with pytest.raises(IndexError):
        remove_at(A(1, 2, None), 2, index)


@pytest.mark.parametrize(
    "values", [(), (1,), (1, 2), (1, 2, 3), (1, 2, 3, 4, 5, 6)]
)
def test_reverse_in_place(values):
    arr = A(*values)
    assert reverse_in_place(arr) is None
    assert list(arr) == list(reversed(values))


@pytest.mark.parametrize(
    "k,expected",
    [(0, [1, 2, 3, 4, 5]), (1, [2, 3, 4, 5, 1]), (2, [3, 4, 5, 1, 2]),
     (5, [1, 2, 3, 4, 5]), (7, [3, 4, 5, 1, 2])],
)
def test_rotate_left(k, expected):
    arr = A(1, 2, 3, 4, 5)
    rotate_left(arr, k)
    assert list(arr) == expected


def test_rotate_left_empty():
    arr = Array(0)
    rotate_left(arr, 3)
    assert list(arr) == []


# -- making new arrays ------------------------------------------------------


def test_resized_grows_and_shrinks():
    arr = A(1, 2, 3)
    bigger = resized(arr, 5)
    smaller = resized(arr, 2)
    assert isinstance(bigger, Array)
    assert list(bigger) == [1, 2, 3, None, None]
    assert list(smaller) == [1, 2]
    assert list(resized(arr, 0)) == []
    assert list(arr) == [1, 2, 3]
    assert bigger is not arr


def test_merge_sorted():
    merged = merge_sorted(A(1, 4, 9), A(2, 3, 10, 11))
    assert isinstance(merged, Array)
    assert list(merged) == [1, 2, 3, 4, 9, 10, 11]
    assert list(merge_sorted(Array(0), A(1, 2))) == [1, 2]
    assert list(merge_sorted(A(1, 2), Array(0))) == [1, 2]
    assert list(merge_sorted(A(2, 2), A(2))) == [2, 2, 2]


# -- two dimensions ---------------------------------------------------------


def test_transpose_flat():
    result = transpose_flat(A(1, 2, 3, 4, 5, 6), 2, 3)
    assert isinstance(result, Array)
    assert list(result) == [1, 4, 2, 5, 3, 6]
    assert list(transpose_flat(result, 3, 2)) == [1, 2, 3, 4, 5, 6]
    assert list(transpose_flat(A(7), 1, 1)) == [7]
    assert list(transpose_flat(A(1, 2, 3), 1, 3)) == [1, 2, 3]


def test_transpose_flat_checks_the_shape():
    with pytest.raises(ValueError):
        transpose_flat(A(1, 2, 3), 2, 2)
