"""Question bank, Week 6 — stacks. Problems W6-C1 to W6-C5.

Questions:  docs/question-bank/week06-questions.md
Tests:      tests/test_practice_week06.py

Use your `Stack` from `dsa/stack.py` as the working storage — not a Python list
used as a stack. Lists are fine as inputs and results.
"""

from dsa.stack import Stack  # noqa: F401  (your Week 6 exercise)


def reverse_words(sentence):
    """W6-C1. The words of `sentence` in reverse order, separated by one space.

    reverse_words("data structures are fun") -> "fun are structures data"
    reverse_words("")                        -> ""
    """
    raise NotImplementedError


class MinStack:
    """W6-C2. A stack that can also report its smallest value — all in O(1).

    push(value); pop() -> value; peek() -> value; get_min() -> the smallest
    value currently in the stack; len(s). pop, peek and get_min raise IndexError
    when empty.

    Hint: a second stack, holding the minimum so far at each level.
    """

    def __init__(self):
        raise NotImplementedError

    def push(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def get_min(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


def next_greater(values):
    """W6-C3. For each element, the first LATER element that is larger, or -1.

    next_greater([2, 1, 5, 3, 4]) -> [5, 5, -1, 4, -1]

    O(n): keep a stack of the indices still waiting for their answer. Each index
    is pushed once and popped at most once.
    """
    raise NotImplementedError


def tags_balanced(html):
    """W6-C4. True if the tags in `html` open and close in the right order.

    Tags look like <name> and </name> (no attributes, no self-closing tags); any
    other text is ignored.

    tags_balanced("<p><b>hi</b></p>") -> True
    tags_balanced("<p><b>hi</p></b>") -> False
    """
    raise NotImplementedError


def decode(encoded):
    """W6-C5. Expand k[text] — text repeated k times — which may nest.

    decode("3[ab]2[c]")  -> "abababcc"
    decode("2[a3[b]]")   -> "abbbabbb"
    decode("xy")         -> "xy"

    k is a positive decimal number, possibly more than one digit.
    """
    raise NotImplementedError
