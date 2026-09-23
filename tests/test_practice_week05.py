"""Question bank, Week 5 practice. Fail until `practice/week05.py` is written."""

import pytest

from dsa.linked_list import Node
from practice.week05 import (
    has_cycle,
    kth_from_end,
    merge_sorted_chains,
    middle_value,
    remove_duplicates_sorted,
)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


def chain(*values):
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def values(head, limit=1000):
    out = []
    while head is not None and len(out) < limit:
        out.append(head.value)
        head = head.next
    return out


def nodes(head):
    out = []
    while head is not None:
        out.append(head)
        head = head.next
    return out


@pytest.mark.parametrize(
    "items,expected",
    [((1,), 1), ((1, 2), 2), ((1, 2, 3), 2), ((1, 2, 3, 4), 3), ((1, 2, 3, 4, 5), 3)],
)
def test_middle_value(items, expected):
    assert middle_value(chain(*items)) == expected


def test_middle_value_empty():
    with pytest.raises(ValueError):
        middle_value(None)


def test_has_cycle():
    assert has_cycle(None) is False
    assert has_cycle(chain(1, 2, 3)) is False
    single = Node(1)
    single.next = single
    assert has_cycle(single) is True
    head = chain(1, 2, 3, 4, 5)
    nodes(head)[-1].next = nodes(head)[2]          # 5 -> 3
    assert has_cycle(head) is True


def test_merge_sorted_chains():
    merged = merge_sorted_chains(chain(1, 4, 9), chain(2, 3, 10, 11))
    assert values(merged) == [1, 2, 3, 4, 9, 10, 11]
    assert values(merge_sorted_chains(None, chain(1, 2))) == [1, 2]
    assert values(merge_sorted_chains(chain(1, 2), None)) == [1, 2]
    assert merge_sorted_chains(None, None) is None


def test_merge_sorted_chains_relinks_and_is_stable():
    a, b = chain((1, "a"), (2, "a")), chain((1, "b"), (3, "b"))
    original = {id(n) for n in nodes(a) + nodes(b)}
    merged = merge_sorted_chains(a, b)
    assert values(merged) == [(1, "a"), (1, "b"), (2, "a"), (3, "b")]
    assert {id(n) for n in nodes(merged)} == original


@pytest.mark.parametrize(
    "items,expected",
    [((), []), ((1,), [1]), ((1, 1, 2, 3, 3, 3), [1, 2, 3]), ((5, 5, 5), [5]),
     ((1, 2, 3), [1, 2, 3])],
)
def test_remove_duplicates_sorted(items, expected):
    assert values(remove_duplicates_sorted(chain(*items))) == expected


@pytest.mark.parametrize("k,expected", [(1, 5), (2, 4), (5, 1)])
def test_kth_from_end(k, expected):
    assert kth_from_end(chain(1, 2, 3, 4, 5), k) == expected


@pytest.mark.parametrize("k", [0, 6, -1])
def test_kth_from_end_out_of_range(k):
    with pytest.raises(IndexError):
        kth_from_end(chain(1, 2, 3, 4, 5), k)
    with pytest.raises(IndexError):
        kth_from_end(None, 1)
