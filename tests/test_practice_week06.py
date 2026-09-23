"""Question bank, Week 6 practice. Fail until `practice/week06.py` is written."""

import pytest

from practice.week06 import MinStack, decode, next_greater, reverse_words, tags_balanced

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


@pytest.mark.parametrize(
    "sentence,expected",
    [("data structures are fun", "fun are structures data"), ("", ""), ("one", "one"),
     ("  spaced   out  ", "out spaced")],
)
def test_reverse_words(sentence, expected):
    assert reverse_words(sentence) == expected


def test_min_stack():
    s = MinStack()
    for value in (5, 3, 7, 3, 1):
        s.push(value)
    assert len(s) == 5
    assert s.get_min() == 1
    assert s.pop() == 1
    assert s.get_min() == 3
    assert s.pop() == 3
    assert s.get_min() == 3          # the other 3 is still there
    assert s.pop() == 7
    assert s.get_min() == 3
    assert s.pop() == 3
    assert s.get_min() == 5
    assert s.peek() == 5
    assert len(s) == 1


def test_min_stack_empty():
    s = MinStack()
    for method in (s.pop, s.peek, s.get_min):
        with pytest.raises(IndexError):
            method()


@pytest.mark.parametrize(
    "values,expected",
    [([2, 1, 5, 3, 4], [5, 5, -1, 4, -1]), ([], []), ([1], [-1]),
     ([1, 2, 3], [2, 3, -1]), ([3, 2, 1], [-1, -1, -1]), ([2, 2, 3], [3, 3, -1])],
)
def test_next_greater(values, expected):
    assert next_greater(values) == expected


def test_next_greater_is_linear():
    values = list(range(200_000, 0, -1)) + [10**9]
    result = next_greater(values)
    assert result[0] == 10**9 and result[-1] == -1


@pytest.mark.parametrize(
    "html,expected",
    [("<p><b>hi</b></p>", True), ("<p><b>hi</p></b>", False), ("plain text", True),
     ("<p>", False), ("</p>", False), ("<a></a><b><i></i></b>", True), ("", True)],
)
def test_tags_balanced(html, expected):
    assert tags_balanced(html) is expected


@pytest.mark.parametrize(
    "encoded,expected",
    [("3[ab]2[c]", "abababcc"), ("2[a3[b]]", "abbbabbb"), ("xy", "xy"), ("", ""),
     ("10[z]", "z" * 10), ("a2[b]c", "abbc")],
)
def test_decode(encoded, expected):
    assert decode(encoded) == expected
