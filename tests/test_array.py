"""The course Array. It is given to you, so these tests pass from day one.

They run with the environment check (`pytest -m "not challenge"`), and they are
also the clearest description of what an Array will and will not do.
"""

import pytest

from dsa.array import Array


def test_new_array_is_full_of_the_fill_value():
    assert list(Array(3)) == [None, None, None]
    assert list(Array(2, fill=0)) == [0, 0]
    assert list(Array(0)) == []


def test_length_is_the_capacity():
    a = Array(5)
    assert len(a) == 5
    a[0] = 1
    assert len(a) == 5


def test_get_and_set():
    a = Array(3)
    a[0], a[2] = "x", "z"
    assert a[0] == "x"
    assert a[1] is None
    assert a[2] == "z"


def test_from_values():
    a = Array.from_values([3, 1, 2])
    assert len(a) == 3
    assert list(a) == [3, 1, 2]
    assert list(Array.from_values(x * x for x in range(4))) == [0, 1, 4, 9]


@pytest.mark.parametrize("index", [3, 99, -1, -3])
def test_out_of_range_and_negative_indices_raise(index):
    a = Array(3)
    with pytest.raises(IndexError):
        a[index]
    with pytest.raises(IndexError):
        a[index] = 0


def test_no_slicing():
    with pytest.raises(TypeError):
        Array(3)[0:2]


def test_no_growing():
    a = Array(2)
    for method in ("append", "insert", "pop", "extend", "remove"):
        assert not hasattr(a, method)
    with pytest.raises(AttributeError):
        a.size = 10                     # no new attributes either


def test_bad_lengths():
    with pytest.raises(ValueError):
        Array(-1)
    with pytest.raises(TypeError):
        Array(2.5)


def test_holds_any_object_by_reference():
    inner = [1, 2]
    a = Array(1)
    a[0] = inner
    inner.append(3)
    assert a[0] is inner


def test_repr():
    assert repr(Array.from_values([1, "a"])) == "Array([1, 'a'])"
    assert repr(Array(0)) == "Array([])"
