"""Lab 01 exercises. Fail until `labs/lab01.py` is written."""

import pytest

from labs.lab01 import (
    celsius_to_fahrenheit,
    collatz_steps,
    fib_list,
    initials,
    is_palindrome_word,
    mask_email,
    middle,
    rotate_left,
    seconds_to_hms,
    split_evenly,
)

pytestmark = [pytest.mark.challenge, pytest.mark.lab]


# -- numbers ----------------------------------------------------------------


@pytest.mark.parametrize(
    "seconds,expected",
    [(0, "0:00:00"), (59, "0:00:59"), (60, "0:01:00"), (3725, "1:02:05"),
     (86400, "24:00:00"), (90061, "25:01:01")],
)
def test_seconds_to_hms(seconds, expected):
    assert seconds_to_hms(seconds) == expected


@pytest.mark.parametrize(
    "c,f", [(0, 32.0), (100, 212.0), (-40, -40.0), (36.6, 97.9), (37, 98.6)]
)
def test_celsius_to_fahrenheit(c, f):
    assert celsius_to_fahrenheit(c) == f


@pytest.mark.parametrize(
    "total,people,expected",
    [(100, 3, (33, 1)), (90, 3, (30, 0)), (5, 8, (0, 5)), (0, 4, (0, 0))],
)
def test_split_evenly(total, people, expected):
    assert split_evenly(total, people) == expected


# -- strings ----------------------------------------------------------------


@pytest.mark.parametrize(
    "name,expected",
    [("haitham el-ghareeb", "H.E."), ("  Ada   King  Lovelace ", "A.K.L."),
     ("guido", "G."), ("", ""), ("   ", "")],
)
def test_initials(name, expected):
    assert initials(name) == expected


@pytest.mark.parametrize(
    "word,expected",
    [("Level", True), (" noon ", True), ("python", False), ("", True),
     ("a", True), ("ab", False), ("RaceCar", True)],
)
def test_is_palindrome_word(word, expected):
    assert is_palindrome_word(word) is expected


@pytest.mark.parametrize(
    "email,expected",
    [("haitham@example.com", "h*****m@example.com"), ("ab@x.org", "ab@x.org"),
     ("a@x.org", "a@x.org"), ("abc@mans.edu.eg", "a*c@mans.edu.eg")],
)
def test_mask_email(email, expected):
    assert mask_email(email) == expected


# -- lists ------------------------------------------------------------------


@pytest.mark.parametrize(
    "values,expected",
    [([1, 2, 3], [2]), ([1, 2, 3, 4], [2, 3]), ([], []), ([7], [7]), ([7, 8], [7, 8])],
)
def test_middle(values, expected):
    assert middle(values) == expected


@pytest.mark.parametrize(
    "values,k,expected",
    [([1, 2, 3, 4, 5], 2, [3, 4, 5, 1, 2]), ([1, 2, 3], 4, [2, 3, 1]),
     ([1, 2, 3], 0, [1, 2, 3]), ([1, 2, 3], 3, [1, 2, 3]), ([], 3, [])],
)
def test_rotate_left(values, k, expected):
    assert rotate_left(values, k) == expected


def test_rotate_left_does_not_change_the_original():
    values = [1, 2, 3, 4]
    result = rotate_left(values, 1)
    assert values == [1, 2, 3, 4]
    assert result is not values


@pytest.mark.parametrize(
    "n,expected",
    [(0, []), (1, [0]), (2, [0, 1]), (7, [0, 1, 1, 2, 3, 5, 8])],
)
def test_fib_list(n, expected):
    assert fib_list(n) == expected


def test_fib_list_is_long_enough():
    assert fib_list(50)[-1] == 7778742049


@pytest.mark.parametrize("n,steps", [(1, 0), (2, 1), (6, 8), (7, 16), (27, 111)])
def test_collatz_steps(n, steps):
    assert collatz_steps(n) == steps
