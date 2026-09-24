"""Question bank, Week 7 practice. Fail until `practice/week07.py` is written."""

import pytest

from practice.week07 import (StackQueue, binary_numbers, josephus, moving_averages,
                             reverse_first_k)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


def test_stack_queue_is_fifo():
    q = StackQueue()
    for value in (1, 2, 3):
        q.enqueue(value)
    assert q.dequeue() == 1
    q.enqueue(4)                     # arrives while 2 and 3 are already poured
    assert [q.dequeue() for _ in range(3)] == [2, 3, 4]
    assert len(q) == 0


def test_stack_queue_empty():
    q = StackQueue()
    with pytest.raises(IndexError):
        q.dequeue()
    q.enqueue("x")
    q.dequeue()
    with pytest.raises(IndexError):
        q.dequeue()


def test_stack_queue_is_amortised_constant():
    q = StackQueue()
    for i in range(200_000):         # pouring back after every dequeue takes hours
        q.enqueue(i)
        if i % 3 == 2:
            q.dequeue()
    assert len(q) == 200_000 - 66_666
    assert q.dequeue() == 66_666


@pytest.mark.parametrize(
    "names,k,expected",
    [(["A", "B", "C", "D", "E"], 2, ["B", "D", "A", "E", "C"]),
     ([1, 2, 3, 4, 5, 6, 7], 3, [3, 6, 2, 7, 5, 1, 4]),
     ([1, 2, 3], 1, [1, 2, 3]),
     (["solo"], 5, ["solo"]),
     ([], 3, [])],
)
def test_josephus(names, k, expected):
    assert josephus(names, k) == expected


@pytest.mark.parametrize(
    "values,k,expected",
    [([2, 4, 6, 8, 10], 3, [4.0, 6.0, 8.0]), ([5, 1], 3, []), ([1, 2, 3], 1, [1, 2, 3]),
     ([1, 2, 3, 4], 4, [2.5]), ([], 2, [])],
)
def test_moving_averages(values, k, expected):
    assert moving_averages(values, k) == pytest.approx(expected)


def test_moving_averages_bad_k():
    with pytest.raises(ValueError):
        moving_averages([1, 2, 3], 0)


def test_moving_averages_is_linear():
    n, k = 100_000, 20_000           # O(nk) would be 1.6 billion additions
    result = moving_averages(list(range(n)), k)
    assert len(result) == n - k + 1
    assert result[0] == pytest.approx((k - 1) / 2)
    assert result[-1] == pytest.approx(n - 1 - (k - 1) / 2)


@pytest.mark.parametrize(
    "values,k,expected",
    [([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]), ([1, 2, 3], 3, [3, 2, 1]),
     ([1, 2, 3], 0, [1, 2, 3]), ([], 0, []), (["a", "b"], 1, ["a", "b"])],
)
def test_reverse_first_k(values, k, expected):
    assert reverse_first_k(values, k) == expected


@pytest.mark.parametrize("k", [-1, 4])
def test_reverse_first_k_bad_k(k):
    with pytest.raises(ValueError):
        reverse_first_k([1, 2, 3], k)


@pytest.mark.parametrize("n", [0, 1, 2, 5, 16, 100])
def test_binary_numbers(n):
    assert binary_numbers(n) == [bin(i)[2:] for i in range(1, n + 1)]
