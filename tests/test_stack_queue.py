"""Stack and queue exercises. Fail until `dsa/stack.py` and `dsa/queue.py` are written."""

import pytest

from dsa.queue import CircularQueue, SlowQueue
from dsa.stack import Stack, infix_to_postfix, is_balanced

pytestmark = pytest.mark.challenge


# -- stack ----------------------------------------------------------------


def test_stack_is_lifo():
    s = Stack()
    for value in (1, 2, 3):
        s.push(value)
    assert s.pop() == 3
    assert s.pop() == 2
    assert len(s) == 1


def test_stack_peek_does_not_remove():
    s = Stack([1, 2])
    assert s.peek() == 2
    assert len(s) == 2


def test_stack_empty_behaviour():
    s = Stack()
    assert s.is_empty()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", True),
        ("()", True),
        ("(a[b]{c})", True),
        ("([)]", False),
        ("(", False),
        (")", False),
        ("no brackets at all", True),
    ],
)
def test_is_balanced(text, expected):
    assert is_balanced(text) is expected


def test_infix_to_postfix():
    assert infix_to_postfix("3 + 4 * 2".split()) == ["3", "4", "2", "*", "+"]
    assert infix_to_postfix("( 3 + 4 ) * 2".split()) == ["3", "4", "+", "2", "*"]


def test_infix_to_postfix_is_left_associative():
    """Equal precedence pops too: 8 - 3 - 2 is (8 - 3) - 2, not 8 - (3 - 2)."""
    assert infix_to_postfix("8 - 3 - 2".split()) == ["8", "3", "-", "2", "-"]
    assert infix_to_postfix("8 / 4 / 2".split()) == ["8", "4", "/", "2", "/"]


# -- queue ----------------------------------------------------------------


@pytest.mark.parametrize("cls", [SlowQueue, CircularQueue], ids=lambda c: c.__name__)
def test_queue_is_fifo(cls):
    q = cls()
    for value in (1, 2, 3):
        q.enqueue(value)
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert len(q) == 1


@pytest.mark.parametrize("cls", [SlowQueue, CircularQueue], ids=lambda c: c.__name__)
def test_dequeue_on_empty_raises(cls):
    with pytest.raises(IndexError):
        cls().dequeue()


def test_circular_queue_wraps_around():
    """The whole point: reuse slots freed at the front."""
    q = CircularQueue(capacity=3)
    for value in (1, 2, 3):
        q.enqueue(value)
    assert q.is_full()
    assert q.dequeue() == 1
    q.enqueue(4)               # must land in the slot 1 vacated
    assert list(q) == [2, 3, 4]


def test_circular_queue_interleaved_operations():
    """Enqueue/dequeue repeatedly so the ring wraps several times over."""
    q = CircularQueue(capacity=4)
    seen = []
    for value in range(10):
        q.enqueue(value)
        if len(q) == 3:
            seen.append(q.dequeue())
    # Values 0 and 1 only fill the queue; from value 2 onward every iteration
    # dequeues one, so 0..7 come out and 8, 9 are still held.
    assert seen == [0, 1, 2, 3, 4, 5, 6, 7]
    assert list(q) == [8, 9]
