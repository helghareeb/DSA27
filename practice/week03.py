"""Question bank, Week 3 — recursion. Problems W3-C1 to W3-C5.

Questions:  docs/question-bank/week03-questions.md
Tests:      tests/test_practice_week03.py

Every function must be RECURSIVE: no `for` or `while` loops, except where a
docstring says otherwise. Move an index rather than slicing where the docstring
asks for it.
"""


def array_sum(arr, i=0):
    """W3-C1. The sum of arr[i], arr[i+1], ..., the last slot, of a course Array.

    No slicing: recurse on the index. Target: O(n) time, O(n) stack.
    array_sum(Array.from_values([2, 5, 1])) -> 8 ;  array_sum(Array(0)) -> 0
    """
    raise NotImplementedError


def count_char(text, ch):
    """W3-C2. How many times the single character `ch` appears in `text`.

    count_char("banana", "a") -> 3 ;  count_char("", "a") -> 0
    (Slicing is allowed here.)
    """
    raise NotImplementedError


def is_sorted_rec(arr, i=0):
    """W3-C3. True if the course Array is in non-decreasing order from index i.

    No slicing. Empty and one-element arrays are sorted.
    """
    raise NotImplementedError


def no_consecutive_ones(n):
    """W3-C4. Every binary string of length n with no two 1s next to each other,
    in increasing order.

    no_consecutive_ones(3) -> ["000", "001", "010", "100", "101"]
    no_consecutive_ones(0) -> [""]

    Branch like binary_strings in Lecture 03, but never put a 1 after a 1.
    (Count them for n = 1, 2, 3, 4, 5 — which famous sequence is it?)
    """
    raise NotImplementedError


def pascal_row(n):
    """W3-C5. Row n of Pascal's triangle, as a list (row 0 is [1]).

    pascal_row(4) -> [1, 4, 6, 4, 1]

    Build it from pascal_row(n - 1). A loop (or comprehension) over the previous
    row is allowed; the recursion is on n.
    """
    raise NotImplementedError
