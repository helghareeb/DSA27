"""Lab 02 — Control flow, functions, errors and modules.

Lab manual: docs/labs/lab02-control-flow-functions.md
Tests:      tests/test_lab02.py

    pytest tests/test_lab02.py -v

Replace each `raise NotImplementedError` with your own code. When a docstring
says "raise ValueError", the tests check that you do — use
`raise ValueError("a message that says what was wrong")`.
"""

# -- decisions --------------------------------------------------------------


def classify_triangle(a, b, c):
    """Name the triangle with side lengths a, b, c.

    Return "equilateral" (three equal sides), "isosceles" (exactly two) or
    "scalene" (none).

    Raise ValueError if any side is not positive, or if the sides break the
    triangle inequality: each side must be strictly shorter than the sum of
    the other two.

    classify_triangle(3, 3, 3)  -> "equilateral"
    classify_triangle(3, 3, 5)  -> "isosceles"
    classify_triangle(3, 4, 5)  -> "scalene"
    classify_triangle(1, 2, 3)  -> ValueError   (1 + 2 is not > 3)
    """
    raise NotImplementedError


def course_result(coursework, final, attendance):
    """Apply this course's pass rules to one student.

    coursework  marks out of 40
    final       marks out of 60
    attendance  percentage of sessions attended, 0 to 100

    Return, checking in this order:
        "barred"  if attendance is below 75       (محروم — no final exam)
        "fail"    if final is below 18            (under 30% of the final)
        "fail"    if coursework + final is below 60
        "pass"    otherwise

    Raise ValueError if any argument is outside its range.

    course_result(35, 25, 90)  -> "pass"
    course_result(38, 15, 100) -> "fail"     total 53, and final under 18
    course_result(40, 60, 70)  -> "barred"
    """
    raise NotImplementedError


# -- loops ------------------------------------------------------------------


def fizzbuzz(n):
    """The FizzBuzz sequence from 1 to n, as a list of strings.

    Multiples of 3 -> "Fizz", of 5 -> "Buzz", of both -> "FizzBuzz",
    anything else -> the number itself as a string.

    fizzbuzz(5)  -> ["1", "2", "Fizz", "4", "Buzz"]
    fizzbuzz(0)  -> []
    """
    raise NotImplementedError


def is_prime(n):
    """True if n is a prime number.

    Numbers below 2 are not prime. It is enough to try divisors up to and
    including the square root of n — ask yourself why.

    is_prime(2) -> True ;  is_prime(9) -> False ;  is_prime(97) -> True
    """
    raise NotImplementedError


def primes_below(n):
    """Every prime p with 2 <= p < n, in increasing order.

    primes_below(10) -> [2, 3, 5, 7]
    primes_below(2)  -> []
    """
    raise NotImplementedError


def first_repeated(values):
    """The first element that equals an element before it, or None.

    "First" means the repeat that happens earliest in the list.

    first_repeated([3, 1, 4, 1, 5, 9, 5])  -> 1
    first_repeated([1, 2, 3])              -> None

    Use loops and `break` or an early `return`. (In Lab 03 you will do this
    again with a set, and it will be much faster.)
    """
    raise NotImplementedError


def count_pairs(n):
    """How many times does the inner body run in this loop?

        for i in range(n):
            for j in range(i + 1, n):
                ...                       # <- count this

    count_pairs(0) -> 0 ;  count_pairs(4) -> 6 ;  count_pairs(10) -> 45

    First write it with the two loops and a counter. Then find a formula that
    gives the same answer without looping, and use that instead. Both pass —
    only one of them is O(1).
    """
    raise NotImplementedError


def calculator(command):
    """Evaluate a tiny command language with a `match` statement.

    The command is words separated by spaces:

        "add A B"   -> A + B
        "mul A B"   -> A * B
        "neg A"     -> -A
        "sum A B C ..." (one or more numbers) -> their total

    A, B, C are integers written in decimal. Anything else raises ValueError.

    calculator("add 2 3")     -> 5
    calculator("neg 7")       -> -7
    calculator("sum 1 2 3 4") -> 10
    calculator("div 1 2")     -> ValueError
    """
    raise NotImplementedError


# -- functions --------------------------------------------------------------


def parse_int(text, default=None):
    """Convert text to an int; return `default` if it is not a valid integer.

    parse_int("42")        -> 42
    parse_int(" -7 ")      -> -7
    parse_int("4.5")       -> None
    parse_int("abc", 0)    -> 0

    Use try/except — do not test the characters yourself.
    """
    raise NotImplementedError


def stats(*numbers):
    """Return (smallest, largest, mean) of any number of arguments.

    stats(3, 1, 2)  -> (1, 3, 2.0)
    stats(5)        -> (5, 5, 5.0)
    stats()         -> ValueError

    Write the loop yourself — no min(), max() or sum().
    """
    raise NotImplementedError


def append_to(item, target=None):
    """Append item to target and return target.

    If no list is given, start a NEW empty list every call.

    append_to(1)       -> [1]
    append_to(2)       -> [2]          not [1, 2]
    append_to(3, [0])  -> [0, 3]

    This is the mutable-default-argument trap from the manual. Do not write
    `target=[]`.
    """
    raise NotImplementedError


def make_multiplier(k):
    """Return a FUNCTION that multiplies its argument by k.

    triple = make_multiplier(3)
    triple(5)  -> 15
    """
    raise NotImplementedError


def apply_n(f, x, n):
    """Apply f to x, n times: f(f(...f(x)...)).

    apply_n(lambda v: v * 2, 1, 10)  -> 1024
    apply_n(str.upper, "hi", 0)      -> "hi"
    """
    raise NotImplementedError
