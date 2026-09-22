"""Recursion — a function defined in terms of itself.

Every recursive function needs exactly two things:

1. a **base case** that returns without recursing, and
2. a **recursive case** that moves measurably closer to the base case.

Miss either one and Python gives you a `RecursionError` instead of an answer.
The limit is about 1000 frames deep by default (`sys.getrecursionlimit()`), and
raising it is almost never the right fix — a wrong base case is.

This is the first module where the *technique* is the lesson rather than the
structure. Trees (`dsa/tree.py`), merge sort and quicksort (`dsa/sorting.py`)
and the parser in `dsa/translation.py` all lean on it.

Declared in the bylaw: "Topics include recursion..." (IS122, SWE 2013 p. 38 and
Medical Informatics 2014 p. 35).
"""

from __future__ import annotations


# -- warm-up: one base case, one step -------------------------------------


def factorial(n):
    """n! — the canonical first recursion.

    factorial(0) -> 1 ;  factorial(5) -> 120

    Raises ValueError for negative n. Target: O(n) time, O(n) stack.
    """
    raise NotImplementedError


def sum_digits(n):
    """Add the decimal digits of a non-negative integer.

    sum_digits(0) -> 0 ;  sum_digits(9) -> 9 ;  sum_digits(1234) -> 10

    Target: O(log n) — one frame per digit.
    """
    raise NotImplementedError


def gcd(a, b):
    """Greatest common divisor, by Euclid's algorithm.

    gcd(12, 18) -> 6 ;  gcd(7, 13) -> 1 ;  gcd(5, 0) -> 5

    The oldest algorithm still in use. Target: O(log min(a, b)).
    """
    raise NotImplementedError


def power(base, exponent):
    """base ** exponent by *fast* exponentiation, for exponent >= 0.

    Halve the exponent each step instead of decrementing it:
        x^10 = (x^5)^2        and       x^5 = x * (x^2)^2

    power(2, 10) -> 1024 ;  power(3, 0) -> 1 ;  power(5, 1) -> 5

    Target: **O(log n)**, not O(n). Doing it in O(n) passes none of the point.
    """
    raise NotImplementedError


# -- recursion over sequences ---------------------------------------------


def reverse_string(text):
    """Reverse a string recursively.

    reverse_string("") -> "" ;  reverse_string("abc") -> "cba"

    Slicing is allowed here — the recursion is the exercise, not the slicing.
    """
    raise NotImplementedError


def is_palindrome(text):
    """True when `text` reads the same forwards and backwards.

    Compare the ends, then recurse on the middle. Empty and single-character
    strings are palindromes. Case and punctuation are **not** ignored:
    is_palindrome("aba") -> True ;  is_palindrome("Aba") -> False
    """
    raise NotImplementedError


def flatten(nested):
    """Flatten arbitrarily nested lists into one flat list.

    flatten([1, [2, [3, [4]]], 5]) -> [1, 2, 3, 4, 5]
    flatten([])                    -> []
    flatten([[], [[]]])            -> []

    The shape of the data is recursive, so the function is too. Only `list` is
    treated as nesting — a string is a value, not a sequence to descend into.
    """
    raise NotImplementedError


def merge_sorted(left, right):
    """Merge two already-sorted lists into one sorted list, recursively.

    merge_sorted([1, 4], [2, 3]) -> [1, 2, 3, 4]
    merge_sorted([], [1])        -> [1]

    Keep it **stable**: when the two heads are equal, take from `left` first.
    Target: O(len(left) + len(right)).

    This is the merge step of merge sort. Write it here in week 3 and you have
    already written half of `dsa/sorting.py` week 10.
    """
    raise NotImplementedError


# -- recursion that branches ----------------------------------------------


def hanoi(n, source="A", target="C", spare="B"):
    """Towers of Hanoi: the moves that shift `n` disks from source to target.

    Returns a list of (from_peg, to_peg) pairs, in order.

        hanoi(1) -> [("A", "C")]
        hanoi(2) -> [("A", "B"), ("A", "C"), ("B", "C")]

    Rules: one disk at a time, never a larger disk onto a smaller one.
    The solution is exactly 2**n - 1 moves, which is why n = 64 is not a
    homework question. Target: O(2**n) — unavoidably.
    """
    raise NotImplementedError


def subsets(items):
    """Every subset of `items` (the power set), as a list of lists.

    subsets([])        -> [[]]
    subsets([1, 2])    -> [[], [1], [2], [1, 2]]   (in any order)

    For each item there are two branches: leave it out, or put it in. That is
    2**n subsets, so the output order is up to you — the tests sort before
    comparing.
    """
    raise NotImplementedError


def permutations(items):
    """Every ordering of `items`, as a list of lists.

    permutations([])     -> [[]]
    permutations([1, 2]) -> [[1, 2], [2, 1]]       (in any order)

    n! results. Order is up to you; the tests sort before comparing.
    Do not call itertools — that is the built-in this exercise reimplements.
    """
    raise NotImplementedError
