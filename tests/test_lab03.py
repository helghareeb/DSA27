"""Lab 03 exercises. Fail until `labs/lab03.py` is written."""

import types

import pytest

from labs.lab03 import (
    Bag,
    chunks,
    common_elements,
    countdown,
    group_by_length,
    invert,
    top_k,
    transpose,
    unique_in_order,
    word_frequencies,
)

pytestmark = [pytest.mark.challenge, pytest.mark.lab]


# -- lists, sets, dictionaries ----------------------------------------------


@pytest.mark.parametrize(
    "values,expected",
    [([3, 1, 3, 2, 1], [3, 1, 2]), ("banana", ["b", "a", "n"]), ([], []),
     ([1, 1, 1], [1]), ([None, 0, None], [None, 0])],
)
def test_unique_in_order(values, expected):
    assert unique_in_order(values) == expected


def test_unique_in_order_is_fast():
    # 200 000 distinct values: an O(n^2) `if v not in result` would take minutes.
    values = list(range(200_000)) * 2
    assert len(unique_in_order(values)) == 200_000


def test_word_frequencies():
    assert word_frequencies("The cat. the HAT!") == {"the": 2, "cat": 1, "hat": 1}
    assert word_frequencies("") == {}
    assert word_frequencies("  a  a\n a ") == {"a": 3}
    assert word_frequencies("wait... what?! ok") == {"wait": 1, "what": 1, "ok": 1}
    assert word_frequencies("!!! ? hi") == {"hi": 1}


def test_top_k():
    freqs = {"b": 2, "a": 2, "c": 5, "d": 1}
    assert top_k(freqs, 2) == [("c", 5), ("a", 2)]
    assert top_k(freqs, 3) == [("c", 5), ("a", 2), ("b", 2)]
    assert top_k(freqs, 10) == [("c", 5), ("a", 2), ("b", 2), ("d", 1)]
    assert top_k({}, 3) == []
    assert top_k(freqs, 0) == []


def test_transpose():
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1]]) == [[1]]
    assert transpose([]) == []
    square = [[1, 2], [3, 4]]
    assert transpose(transpose(square)) == square


def test_invert():
    assert invert({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}
    assert invert({}) == {}
    assert invert({"z": 0, "y": 0, "x": 0}) == {0: ["x", "y", "z"]}


def test_common_elements():
    assert common_elements([3, 1, 2, 3], [3, 4, 1]) == [1, 3]
    assert common_elements([1, 2], [3, 4]) == []
    assert common_elements("hello", "world") == ["l", "o"]


def test_group_by_length():
    assert group_by_length(["hi", "sun", "to", "sky"]) == {2: ["hi", "to"], 3: ["sun", "sky"]}
    assert group_by_length([]) == {}


# -- a class: the Bag ADT ---------------------------------------------------


def test_bag_counts():
    b = Bag(["a", "b", "a"])
    assert len(b) == 3
    assert b.count("a") == 2
    assert b.count("b") == 1
    assert b.count("z") == 0
    assert b.distinct() == 2


def test_bag_empty():
    b = Bag()
    assert len(b) == 0
    assert b.distinct() == 0
    assert "a" not in b
    assert list(b) == []
    assert repr(b) == "Bag([])"


def test_bag_add_and_contains():
    b = Bag()
    b.add("x")
    b.add("x")
    assert "x" in b
    assert "y" not in b
    assert len(b) == 2
    assert b.distinct() == 1


def test_bag_remove_one_at_a_time():
    b = Bag("aab")
    b.remove("a")
    assert b.count("a") == 1
    assert len(b) == 2
    b.remove("a")
    assert "a" not in b
    assert b.distinct() == 1


def test_bag_remove_missing_raises_key_error():
    b = Bag("a")
    b.remove("a")
    with pytest.raises(KeyError):
        b.remove("a")
    with pytest.raises(KeyError):
        Bag().remove("anything")


def test_bag_iterates_with_repeats():
    assert sorted(Bag(["b", "a", "b", "c", "b"])) == ["a", "b", "b", "b", "c"]


def test_bag_equality_ignores_order():
    assert Bag("aab") == Bag("aba")
    assert Bag("aab") != Bag("ab")
    b = Bag("ab")
    b.add("a")
    b.remove("a")
    b.remove("a")
    assert b == Bag("b")


def test_bag_repr():
    assert repr(Bag(["b", "a", "b"])) == "Bag(['a', 'b', 'b'])"
    assert repr(Bag([3, 1])) == "Bag([1, 3])"


def test_bags_do_not_share_state():
    first, second = Bag(), Bag()
    first.add("x")
    assert len(second) == 0


# -- generators -------------------------------------------------------------


def test_countdown_is_a_generator():
    assert isinstance(countdown(3), types.GeneratorType)


def test_countdown():
    assert list(countdown(3)) == [3, 2, 1]
    assert list(countdown(1)) == [1]
    assert list(countdown(0)) == []
    assert list(countdown(-2)) == []


def test_chunks_is_a_generator():
    assert isinstance(chunks([1, 2, 3], 2), types.GeneratorType)


def test_chunks():
    assert list(chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(chunks([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]
    assert list(chunks([], 3)) == []
    assert list(chunks([1, 2], 5)) == [[1, 2]]


def test_chunks_rejects_bad_size():
    with pytest.raises(ValueError):
        list(chunks([1, 2, 3], 0))
    with pytest.raises(ValueError):
        list(chunks([1, 2, 3], -1))
