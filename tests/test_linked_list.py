"""Linked list exercises. These fail until `dsa/linked_list.py` is written."""

import pytest

from dsa.linked_list import LinkedList, Node

pytestmark = pytest.mark.challenge


def test_node_holds_a_value_and_a_link():
    node = Node(1, Node(2))
    assert node.value == 1
    assert node.next.value == 2
    assert node.next.next is None


def test_empty_list():
    ll = LinkedList()
    assert len(ll) == 0
    assert list(ll) == []
    assert ll.head is None


def test_push_front_reverses_insertion_order():
    ll = LinkedList()
    for value in (1, 2, 3):
        ll.push_front(value)
    assert list(ll) == [3, 2, 1]
    assert len(ll) == 3


def test_append_preserves_insertion_order():
    ll = LinkedList()
    for value in (1, 2, 3):
        ll.append(value)
    assert list(ll) == [1, 2, 3]


def test_constructor_takes_an_iterable():
    assert list(LinkedList([1, 2, 3])) == [1, 2, 3]


@pytest.mark.parametrize(
    "index,expected",
    [(0, ["x", 1, 2, 3]), (1, [1, "x", 2, 3]), (3, [1, 2, 3, "x"])],
)
def test_insert_at(index, expected):
    ll = LinkedList([1, 2, 3])
    ll.insert_at(index, "x")
    assert list(ll) == expected
    assert len(ll) == 4


@pytest.mark.parametrize("index", [-1, 5])
def test_insert_at_rejects_out_of_range(index):
    with pytest.raises(IndexError):
        LinkedList([1, 2, 3]).insert_at(index, "x")


def test_pop_front():
    ll = LinkedList([1, 2, 3])
    assert ll.pop_front() == 1
    assert list(ll) == [2, 3]
    assert len(ll) == 2


def test_pop_front_on_empty_raises():
    with pytest.raises(IndexError):
        LinkedList().pop_front()


def test_remove_first_match_only():
    ll = LinkedList([1, 2, 2, 3])
    assert ll.remove(2) is True
    assert list(ll) == [1, 2, 3]


def test_remove_updates_the_length():
    ll = LinkedList([1, 2, 3])
    ll.remove(2)
    ll.remove(1)
    assert len(ll) == 1


def test_remove_head():
    ll = LinkedList([1, 2, 3])
    assert ll.remove(1) is True
    assert list(ll) == [2, 3]
    assert ll.head.value == 2


def test_remove_absent_value():
    ll = LinkedList([1, 2, 3])
    assert ll.remove(99) is False
    assert len(ll) == 3


def test_find():
    ll = LinkedList(["a", "b", "c"])
    assert ll.find("a") == 0
    assert ll.find("c") == 2
    assert ll.find("z") == -1


def test_getitem():
    ll = LinkedList([10, 20, 30])
    assert ll[0] == 10
    assert ll[2] == 30


def test_getitem_out_of_range_raises():
    with pytest.raises(IndexError):
        LinkedList([1])[5]


def test_reverse():
    ll = LinkedList([1, 2, 3, 4])
    ll.reverse()
    assert list(ll) == [4, 3, 2, 1]
    assert ll.head.value == 4


@pytest.mark.parametrize("values", [[], [1], [1, 2]])
def test_reverse_handles_short_lists(values):
    ll = LinkedList(values)
    ll.reverse()
    assert list(ll) == list(reversed(values))


def test_reverse_relinks_rather_than_rebuilding():
    """Reversing must be in place — O(1) extra space, no new Node objects."""
    ll = LinkedList([1, 2, 3])
    last = ll.head.next.next
    original = {id(node) for node in _nodes(ll)}
    ll.reverse()
    assert {id(node) for node in _nodes(ll)} == original
    assert ll.head is last, "the old last node must become the head: relink, do not copy values"


def _nodes(ll):
    node = ll.head
    while node is not None:
        yield node
        node = node.next
