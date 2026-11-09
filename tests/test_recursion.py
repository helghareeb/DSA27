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
    """Reject linear recursive depth; the next test also checks total work.
    Decrementing needs 4097 frames; halving to zero needs 14."""
    assert power(2, 4096) == 2**4096


def test_power_uses_logarithmically_many_multiplications():
    """Two half-power calls have shallow depth but do linear total work."""
    class CountedNumber:
        multiplications = 0

        def __init__(self, value):
            self.value = value

        def __mul__(self, other):
            type(self).multiplications += 1
            value = other.value if isinstance(other, CountedNumber) else other
            return CountedNumber(self.value * value)

        __rmul__ = __mul__

    exponent = 4096
    result = power(CountedNumber(1), exponent)
    assert result.value == 1
    assert CountedNumber.multiplications <= 2 * exponent.bit_length()


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
    """Compare keys only, then check identities so a tie is really a tie."""
    class Item:
        def __init__(self, key):
            self.key = key

        def __lt__(self, other):
            return self.key < other.key

        def __le__(self, other):
            return self.key <= other.key

        def __eq__(self, other):
            return self.key == other.key

    left = [Item(1), Item(2)]
    right = [Item(1), Item(2)]
    result = merge_sorted(left, right)
    expected = [left[0], right[0], left[1], right[1]]
    assert len(result) == len(expected)
    assert all(actual is wanted for actual, wanted in zip(result, expected))


def test_merge_sorted_does_not_copy_tails_repeatedly():
    """Count input reads and slice copies, rather than machine-dependent time."""
    class CountedList(list):
        work = 0

        def __getitem__(self, index):
            value = super().__getitem__(index)
            if isinstance(index, slice):
                type(self).work += len(value)
                return type(self)(value)
            type(self).work += 1
            return value

    left = CountedList(range(0, 200, 2))
    right = CountedList(range(1, 200, 2))
    assert merge_sorted(left, right) == list(range(200))
    assert CountedList.work <= 4 * (len(left) + len(right))
    assert left == list(range(0, 200, 2))
    assert right == list(range(1, 200, 2))


# -- recursion that branches ----------------------------------------------


def test_hanoi_zero_disks():
    assert hanoi(0) == []


def test_hanoi_custom_pegs_and_independent_results():
    expected = [("start", "spare"), ("start", "finish"), ("spare", "finish")]
    first = hanoi(2, "start", "finish", "spare")
    assert first == expected
    first.clear()
    assert hanoi(2, "start", "finish", "spare") == expected


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
