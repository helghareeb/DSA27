"""Recursion exercises. Fail until `dsa/recursion.py` is written."""

import pytest

from dsa.recursion import (
    factorial,
    flatten,
    gcd,
    hanoi,
    is_palindrome,
    merge_sorted,
    permutations,
    power,
    reverse_string,
    subsets,
    sum_digits,
)

pytestmark = pytest.mark.challenge


# -- one base case, one step ----------------------------------------------


@pytest.mark.parametrize("n,expected", [(0, 1), (1, 1), (5, 120), (10, 3628800)])
def test_factorial(n, expected):
    assert factorial(n) == expected


def test_factorial_rejects_negative():
    with pytest.raises(ValueError):
        factorial(-1)


@pytest.mark.parametrize("n,expected", [(0, 0), (9, 9), (1234, 10), (1000, 1)])
def test_sum_digits(n, expected):
    assert sum_digits(n) == expected


@pytest.mark.parametrize("a,b,expected", [(12, 18, 6), (18, 12, 6), (7, 13, 1), (5, 0, 5), (0, 5, 5)])
def test_gcd(a, b, expected):
    assert gcd(a, b) == expected


@pytest.mark.parametrize("base,exp,expected", [(2, 0, 1), (2, 1, 2), (2, 10, 1024), (3, 5, 243), (5, 4, 625)])
def test_power(base, exp, expected):
    assert power(base, exp) == expected


def test_power_is_logarithmic():
    """This is the test that rejects an O(n) solution. Decrementing the
    exponent needs 4096 stack frames and hits Python's ~1000 frame limit;
    halving it needs 13."""
    assert power(2, 4096) == 2**4096


# -- recursion over sequences ---------------------------------------------


@pytest.mark.parametrize("text,expected", [("", ""), ("a", "a"), ("abc", "cba"), ("abba", "abba")])
def test_reverse_string(text, expected):
    assert reverse_string(text) == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", True),
        ("a", True),
        ("aba", True),
        ("abba", True),
        ("abc", False),
        ("Aba", False),      # case is not ignored
    ],
)
def test_is_palindrome(text, expected):
    assert is_palindrome(text) is expected


@pytest.mark.parametrize(
    "nested,expected",
    [
        ([], []),
        ([1, 2, 3], [1, 2, 3]),
        ([1, [2, [3, [4]]], 5], [1, 2, 3, 4, 5]),
        ([[], [[]]], []),
        ([[1], [2, [3]], []], [1, 2, 3]),
    ],
)
def test_flatten(nested, expected):
    assert flatten(nested) == expected


def test_flatten_treats_a_string_as_a_value():
    """Strings are iterable, so a careless implementation recurses into them
    forever — "a" contains "a" contains "a"."""
    assert flatten(["ab", ["cd"]]) == ["ab", "cd"]


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ([], [], []),
        ([], [1], [1]),
        ([1], [], [1]),
        ([1, 4], [2, 3], [1, 2, 3, 4]),
        ([1, 2, 3], [4, 5], [1, 2, 3, 4, 5]),
    ],
)
def test_merge_sorted(left, right, expected):
    assert merge_sorted(left, right) == expected


def test_merge_sorted_is_stable():
    """On a tie the left list goes first. The pairs let us see which one did."""
    left = [(1, "L"), (2, "L")]
    right = [(1, "R"), (2, "R")]
    assert merge_sorted(left, right) == [(1, "L"), (1, "R"), (2, "L"), (2, "R")]


# -- recursion that branches ----------------------------------------------


def test_hanoi_one_disk():
    assert hanoi(1, "A", "C", "B") == [("A", "C")]


def test_hanoi_two_disks():
    assert hanoi(2, "A", "C", "B") == [("A", "B"), ("A", "C"), ("B", "C")]


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 8])
def test_hanoi_move_count(n):
    assert len(hanoi(n, "A", "C", "B")) == 2**n - 1


def test_hanoi_moves_are_legal():
    """Replay the moves against three real pegs: a disk may never land on a
    smaller one, and everything must end up on the target peg."""
    n = 6
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    for source, target in hanoi(n, "A", "C", "B"):
        assert pegs[source], f"moved from empty peg {source}"
        disk = pegs[source].pop()
        assert not pegs[target] or pegs[target][-1] > disk, "larger disk onto smaller"
        pegs[target].append(disk)
    assert pegs["C"] == list(range(n, 0, -1))
    assert pegs["A"] == [] and pegs["B"] == []


def _normalise(groups):
    return sorted(tuple(group) for group in groups)


@pytest.mark.parametrize(
    "items,expected",
    [
        ([], [()]),
        ([1], [(), (1,)]),
        ([1, 2], [(), (1,), (1, 2), (2,)]),
    ],
)
def test_subsets(items, expected):
    assert _normalise(subsets(items)) == sorted(expected)


@pytest.mark.parametrize("n", [0, 1, 2, 3, 5])
def test_subsets_count(n):
    assert len(subsets(list(range(n)))) == 2**n


@pytest.mark.parametrize(
    "items,expected",
    [
        ([], [()]),
        ([1], [(1,)]),
        ([1, 2], [(1, 2), (2, 1)]),
        ([1, 2, 3], [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]),
    ],
)
def test_permutations(items, expected):
    assert _normalise(permutations(items)) == sorted(expected)


@pytest.mark.parametrize("n,expected", [(0, 1), (1, 1), (2, 2), (3, 6), (4, 24), (5, 120)])
def test_permutations_count(n, expected):
    assert len(permutations(list(range(n)))) == expected
