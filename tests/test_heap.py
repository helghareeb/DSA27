"""Heap and priority queue exercises. Fail until `dsa/heap.py` is written."""

import random

import pytest

from dsa.heap import MaxHeap, MinHeap, PriorityQueue

pytestmark = pytest.mark.challenge

BOTH = pytest.mark.parametrize("cls", [MinHeap, MaxHeap], ids=lambda c: c.__name__)


def _best(cls, values):
    """The value that should sit at the root for this heap kind."""
    return min(values) if cls is MinHeap else max(values)


def _drain(heap):
    return [heap.pop() for _ in range(len(heap))]


# -- the basic contract ---------------------------------------------------


@BOTH
def test_push_then_peek_gives_the_best(cls):
    heap = cls()
    for value in (5, 3, 8, 1, 9):
        heap.push(value)
    assert heap.peek() == _best(cls, [5, 3, 8, 1, 9])
    assert len(heap) == 5


@BOTH
def test_empty_heap(cls):
    heap = cls()
    assert heap.is_empty()
    assert len(heap) == 0
    with pytest.raises(IndexError):
        heap.pop()
    with pytest.raises(IndexError):
        heap.peek()


@BOTH
def test_pop_returns_sorted_order(cls):
    values = [5, 3, 8, 1, 9, 2, 7]
    heap = cls(values)
    expected = sorted(values) if cls is MinHeap else sorted(values, reverse=True)
    assert _drain(heap) == expected


@BOTH
def test_peek_does_not_remove(cls):
    heap = cls([4, 2, 7])
    assert heap.peek() == heap.peek()
    assert len(heap) == 3


@BOTH
def test_duplicates_are_kept(cls):
    heap = cls([3, 3, 3])
    assert len(heap) == 3
    assert _drain(heap) == [3, 3, 3]


@BOTH
def test_single_element(cls):
    heap = cls()
    heap.push(42)
    assert heap.peek() == 42
    assert heap.pop() == 42
    assert heap.is_empty()


# -- the invariant --------------------------------------------------------


@BOTH
def test_invariant_holds_after_every_push(cls):
    heap = cls()
    for value in random.Random(0).sample(range(100), 40):
        heap.push(value)
        assert heap.is_valid()


@BOTH
def test_invariant_holds_after_every_pop(cls):
    heap = cls(random.Random(1).sample(range(100), 40))
    while len(heap) > 1:
        heap.pop()
        assert heap.is_valid()


@BOTH
def test_heapify_from_arbitrary_order(cls):
    """heapify rearranges whatever was there into a valid heap."""
    values = [9, 4, 7, 1, 8, 2, 6, 3, 5]
    heap = cls(values)
    assert heap.is_valid()
    assert sorted(heap._items) == sorted(values)
    assert heap.peek() == _best(cls, values)


@BOTH
def test_is_valid_rejects_a_broken_array(cls):
    """Plant a violation by hand: is_valid must actually inspect the array."""
    heap = cls([1, 2, 3])
    heap._items[0], heap._items[2] = heap._items[2], heap._items[0]
    assert not heap.is_valid()


@BOTH
def test_interleaved_push_and_pop(cls):
    """Sifting up and sifting down have to cooperate, not just work alone."""
    heap = cls()
    reference = []
    for value in random.Random(2).sample(range(200), 60):
        heap.push(value)
        reference.append(value)
        if len(reference) % 3 == 0:
            expected = _best(cls, reference)
            assert heap.pop() == expected
            reference.remove(expected)
        assert heap.is_valid()
    assert sorted(heap._items) == sorted(reference)


def test_max_heap_differs_from_min_heap():
    """The two classes must not be the same heap wearing two names."""
    values = [5, 1, 9]
    assert MinHeap(values).peek() == 1
    assert MaxHeap(values).peek() == 9


# -- priority queue -------------------------------------------------------


def test_priority_queue_serves_lowest_number_first():
    pq = PriorityQueue()
    pq.enqueue("write tests", 2)
    pq.enqueue("fix the build", 1)
    pq.enqueue("refactor later", 5)
    assert pq.dequeue() == "fix the build"
    assert pq.dequeue() == "write tests"
    assert pq.dequeue() == "refactor later"


def test_priority_queue_is_not_a_fifo():
    """Insert in order and the queue must still reorder by priority."""
    pq = PriorityQueue()
    for index, priority in enumerate([9, 7, 5, 3, 1]):
        pq.enqueue(index, priority)
    assert [pq.dequeue() for _ in range(5)] == [4, 3, 2, 1, 0]


def test_priority_queue_peek_and_len():
    pq = PriorityQueue()
    pq.enqueue("only", 1)
    assert pq.peek() == "only"
    assert len(pq) == 1
    assert not pq.is_empty()


def test_priority_queue_empty():
    pq = PriorityQueue()
    assert pq.is_empty()
    with pytest.raises(IndexError):
        pq.dequeue()
    with pytest.raises(IndexError):
        pq.peek()


def test_priority_queue_handles_unorderable_items():
    """Two items tie on priority. If the heap falls through to comparing the
    items themselves, dicts raise TypeError — which is what the tie-breaking
    counter exists to prevent."""
    pq = PriorityQueue()
    pq.enqueue({"task": "a"}, 1)
    pq.enqueue({"task": "b"}, 1)
    assert pq.dequeue() in ({"task": "a"}, {"task": "b"})
    assert pq.dequeue() in ({"task": "a"}, {"task": "b"})
