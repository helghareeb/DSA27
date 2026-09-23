"""Lab 02 exercises. Fail until `labs/lab02.py` is written."""

import pytest

from labs.lab02 import (
    append_to,
    apply_n,
    calculator,
    classify_triangle,
    count_pairs,
    course_result,
    first_repeated,
    fizzbuzz,
    is_prime,
    make_multiplier,
    parse_int,
    primes_below,
    stats,
)

pytestmark = [pytest.mark.challenge, pytest.mark.lab]


# -- decisions --------------------------------------------------------------


@pytest.mark.parametrize(
    "sides,expected",
    [((3, 3, 3), "equilateral"), ((3, 3, 5), "isosceles"), ((5, 3, 3), "isosceles"),
     ((3, 5, 3), "isosceles"), ((3, 4, 5), "scalene"), ((2.5, 2.5, 4), "isosceles")],
)
def test_classify_triangle(sides, expected):
    assert classify_triangle(*sides) == expected


@pytest.mark.parametrize(
    "sides", [(1, 2, 3), (1, 1, 5), (0, 1, 1), (-3, 4, 5), (5, 1, 1)]
)
def test_classify_triangle_rejects_impossible_sides(sides):
    with pytest.raises(ValueError):
        classify_triangle(*sides)


@pytest.mark.parametrize(
    "cw,final,att,expected",
    [(35, 25, 90, "pass"), (20, 40, 75, "pass"), (40, 20, 100, "pass"),
     (38, 15, 100, "fail"), (40, 17, 100, "fail"), (10, 40, 80, "fail"),
     (40, 60, 70, "barred"), (0, 0, 0, "barred"), (40, 60, 74.9, "barred")],
)
def test_course_result(cw, final, att, expected):
    assert course_result(cw, final, att) == expected


@pytest.mark.parametrize(
    "args", [(41, 30, 90), (-1, 30, 90), (30, 61, 90), (30, -5, 90), (30, 30, 101), (30, 30, -1)]
)
def test_course_result_rejects_out_of_range(args):
    with pytest.raises(ValueError):
        course_result(*args)


# -- loops ------------------------------------------------------------------


def test_fizzbuzz():
    assert fizzbuzz(0) == []
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    result = fizzbuzz(15)
    assert result[-1] == "FizzBuzz"
    assert result[8] == "Fizz" and result[9] == "Buzz"
    assert len(result) == 15


@pytest.mark.parametrize(
    "n,expected",
    [(-7, False), (0, False), (1, False), (2, True), (3, True), (4, False),
     (9, False), (25, False), (97, True), (7919, True), (7917, False)],
)
def test_is_prime(n, expected):
    assert is_prime(n) is expected


def test_primes_below():
    assert primes_below(0) == []
    assert primes_below(2) == []
    assert primes_below(3) == [2]
    assert primes_below(10) == [2, 3, 5, 7]
    assert len(primes_below(1000)) == 168


@pytest.mark.parametrize(
    "values,expected",
    [([3, 1, 4, 1, 5, 9, 5], 1), ([1, 2, 3], None), ([], None),
     ([2, 5, 5, 2], 5), (["a", "b", "a"], "a"), ([0, 0], 0)],
)
def test_first_repeated(values, expected):
    assert first_repeated(values) == expected


@pytest.mark.parametrize("n,expected", [(0, 0), (1, 0), (2, 1), (4, 6), (10, 45), (1000, 499500)])
def test_count_pairs(n, expected):
    assert count_pairs(n) == expected


@pytest.mark.parametrize(
    "command,expected",
    [("add 2 3", 5), ("mul 4 5", 20), ("neg 7", -7), ("neg -7", 7),
     ("sum 1 2 3 4", 10), ("sum 9", 9), ("add -2 2", 0)],
)
def test_calculator(command, expected):
    assert calculator(command) == expected


@pytest.mark.parametrize(
    "command", ["div 1 2", "add 1", "add 1 2 3", "neg", "sum", "", "add x 2"]
)
def test_calculator_rejects_bad_commands(command):
    with pytest.raises(ValueError):
        calculator(command)


# -- functions --------------------------------------------------------------


@pytest.mark.parametrize(
    "args,expected",
    [(("42",), 42), ((" -7 ",), -7), (("4.5",), None), (("abc", 0), 0), (("",), None)],
)
def test_parse_int(args, expected):
    assert parse_int(*args) == expected


def test_stats():
    assert stats(3, 1, 2) == (1, 3, 2.0)
    assert stats(5) == (5, 5, 5.0)
    assert stats(-1, -9, 4, 10) == (-9, 10, 1.0)


def test_stats_needs_at_least_one_number():
    with pytest.raises(ValueError):
        stats()


def test_append_to_starts_fresh_each_call():
    assert append_to(1) == [1]
    assert append_to(2) == [2]


def test_append_to_uses_the_given_list():
    target = [0]
    result = append_to(3, target)
    assert result == [0, 3]
    assert result is target


def test_make_multiplier():
    triple = make_multiplier(3)
    double = make_multiplier(2)
    assert triple(5) == 15
    assert double(5) == 10
    assert make_multiplier("ab")(3) == "ababab"


def test_apply_n():
    assert apply_n(lambda v: v * 2, 1, 10) == 1024
    assert apply_n(str.upper, "hi", 0) == "hi"
    assert apply_n(lambda s: s + "!", "go", 3) == "go!!!"
