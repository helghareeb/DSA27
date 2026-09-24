"""Dynamic array exercises. Fail until `dsa/dynamic_array.py` is written."""

import pytest

from dsa.dynamic_array import DynamicArray

pytestmark = pytest.mark.challenge


def test_empty():
    arr = DynamicArray()
    assert len(arr) == 0
    assert list(arr) == []


def test_append_and_index():
    arr = DynamicArray()
    for value in (10, 20, 30):
        arr.append(value)
    assert len(arr) == 3
    assert arr[0] == 10
    assert arr[2] == 30
    assert list(arr) == [10, 20, 30]


def test_constructor_takes_an_iterable():
    assert list(DynamicArray([1, 2, 3])) == [1, 2, 3]


def test_negative_indexing():
    arr = DynamicArray([1, 2, 3])
    assert arr[-1] == 3
    assert arr[-3] == 1


@pytest.mark.parametrize("index", [3, -4, 99])
def test_index_out_of_range_raises(index):
    with pytest.raises(IndexError):
        DynamicArray([1, 2, 3])[index]


def test_setitem():
    arr = DynamicArray([1, 2, 3])
    arr[1] = 99
    assert list(arr) == [1, 99, 3]


def test_insert_at_shifts_right():
    arr = DynamicArray([1, 2, 3])
    arr.insert_at(1, 99)
    assert list(arr) == [1, 99, 2, 3]
    assert len(arr) == 4


@pytest.mark.parametrize("index", [-1, 4])
def test_insert_at_out_of_range_raises(index):
    with pytest.raises(IndexError):
        DynamicArray([1, 2, 3]).insert_at(index, 99)


def test_insert_at_grows_when_full():
    """insert_at must resize a full array, just as append does."""
    arr = DynamicArray()
    for value in range(100):
        arr.insert_at(0, value)
    assert list(arr) == list(range(99, -1, -1))


def test_setitem_out_of_range_raises():
    arr = DynamicArray([1, 2, 3])
    with pytest.raises(IndexError):
        arr[3] = 99


def test_pop_from_end_and_middle():
    arr = DynamicArray([1, 2, 3])
    assert arr.pop() == 3
    assert arr.pop(0) == 1
    assert list(arr) == [2]


def test_pop_clears_the_freed_slot():
    """The slot a pop frees must not keep a reference (Lecture 04)."""
    arr = DynamicArray(["a", "b", "c"])
    arr.pop()
    arr.pop(0)
    assert arr._block[len(arr)] is None
    assert arr._block[len(arr) + 1] is None


def test_pop_on_empty_raises():
    with pytest.raises(IndexError):
        DynamicArray().pop()


def test_grows_beyond_initial_capacity():
    """The core of the exercise: reallocation must preserve every element."""
    arr = DynamicArray()
    for value in range(1000):
        arr.append(value)
    assert len(arr) == 1000
    assert list(arr) == list(range(1000))


def test_doubling_keeps_resizes_logarithmic():
    """1000 appends with doubling should reallocate ~10 times, not ~1000.

    This is the difference between amortised O(1) and O(n) — and it is worth
    running with growth=2 and then a constant-growth variant to compare.
    """
    arr = DynamicArray()
    for value in range(1000):
        arr.append(value)
    assert arr.resize_count > 0, "resize_count never went up — increment it in _resize"
    assert arr.resize_count < 20, (
        f"{arr.resize_count} reallocations for 1000 appends — "
        "are you growing by a constant instead of doubling?"
    )
