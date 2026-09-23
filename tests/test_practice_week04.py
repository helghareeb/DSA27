"""Question bank, Week 4 practice. Fail until `practice/week04.py` is written."""

import pytest

from practice.week04 import ShrinkingArray, capacity_after, copies_for

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


@pytest.mark.parametrize(
    "n,factor,expected",
    [(0, 2, 1), (1, 2, 1), (2, 2, 2), (3, 2, 4), (5, 2, 8), (8, 2, 8), (9, 2, 16),
     (1000, 2, 1024), (5, 3, 9), (10, 3, 27), (2, 4, 4)],
)
def test_capacity_after(n, factor, expected):
    assert capacity_after(n, factor) == expected


def test_copies_for_doubling():
    assert copies_for(0, lambda c: 2 * c) == 0
    assert copies_for(1, lambda c: 2 * c) == 0
    assert copies_for(5, lambda c: 2 * c) == 7
    assert copies_for(100_000, lambda c: 2 * c) == 131_071


def test_copies_for_constant_steps():
    assert copies_for(5, lambda c: c + 1) == 10
    assert copies_for(1000, lambda c: c + 1) == 499_500
    assert copies_for(1000, lambda c: c + 10) == 49_600


def test_shrinking_array_grows_by_doubling():
    a = ShrinkingArray()
    assert len(a) == 0 and a.capacity == 1
    for i in range(5):
        a.append(i * 10)
    assert len(a) == 5
    assert a.capacity == 8
    assert a.resize_count == 3
    assert [a[i] for i in range(5)] == [0, 10, 20, 30, 40]


def test_shrinking_array_bounds():
    a = ShrinkingArray()
    a.append("x")
    with pytest.raises(IndexError):
        a[1]
    with pytest.raises(IndexError):
        a[-1]
    assert a.pop() == "x"
    with pytest.raises(IndexError):
        a.pop()


def test_shrinking_array_halves_at_one_quarter():
    a = ShrinkingArray()
    for i in range(9):
        a.append(i)                      # capacity 16, size 9
    assert a.capacity == 16
    for expected in (8, 7, 6, 5):
        assert a.pop() == expected       # size 8, 7, 6, 5: above 16 // 4
    assert a.capacity == 16
    assert a.pop() == 4                  # size 4 <= 16 // 4: halve
    assert a.capacity == 8
    assert [a[i] for i in range(len(a))] == [0, 1, 2, 3]


def test_shrinking_array_never_below_one():
    a = ShrinkingArray()
    a.append(1)
    a.append(2)
    a.pop()
    a.pop()
    assert len(a) == 0
    assert a.capacity >= 1
    a.append(3)
    assert a[0] == 3


def test_shrinking_array_does_not_thrash():
    """Alternate append and pop at the growth boundary: at most one resize."""
    a = ShrinkingArray()
    for i in range(8):
        a.append(i)                      # full: size 8, capacity 8
    before = a.resize_count
    for _ in range(1000):
        a.append("x")
        a.pop()
    assert a.resize_count - before <= 1
