"""SOLUTION — try the exercise in `dsa/stack.py` first; see `solutions/README.md`.

Stack — last in, first out.

Deliberately a thin structure: the interesting part is what you *do* with it
(balanced brackets, infix to postfix, undo history, DFS without recursion).

Built on your own `DynamicArray` (Week 4): the top of the stack is the END of
the array, where append and pop are O(1). Put the top at index 0 instead and
every push shifts the whole stack — try it, and measure it.
"""

from __future__ import annotations

from dsa.dynamic_array import DynamicArray


class Stack:
    """LIFO. Every operation should be O(1)."""

    def __init__(self, values=()):
        self._items = DynamicArray()
        for value in values:
            self.push(value)

    def push(self, value):
        """Add to the top. Target: O(1) amortised."""
        self._items.append(value)                # the top is the END of the array

    def pop(self):
        """Remove and return the top. Target: O(1). Raises IndexError when empty."""
        if len(self._items) == 0:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top without removing it. Raises IndexError when empty."""
        if len(self._items) == 0:
            raise IndexError("peek at empty stack")
        return self._items[len(self._items) - 1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        if not len(self._items):
            return "Stack([])"
        return f"Stack({list(self._items)!r})  # top = {self._items[len(self._items) - 1]!r}"


# -- challenges -----------------------------------------------------------


def is_balanced(text):
    """True when every bracket in `text` is closed in the right order.

    "(a[b]{c})" -> True ;  "(a[b)]" -> False ;  "(" -> False

    The canonical first use of a stack. Target: O(n).
    """
    partner = {")": "(", "]": "[", "}": "{"}
    openers = Stack()
    for ch in text:
        if ch in "([{":
            openers.push(ch)
        elif ch in partner:
            if openers.is_empty():               # a closer with nothing open
                return False
            if openers.pop() != partner[ch]:     # the wrong partner
                return False
    return openers.is_empty()                    # nothing left open


def infix_to_postfix(tokens):
    """Shunting-yard: ["3","+","4","*","2"] -> ["3","4","2","*","+"].

    Target: O(n). Handles + - * / and parentheses.
    """
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output, operators = [], Stack()
    for token in tokens:
        if token in precedence:
            # higher OR EQUAL precedence leaves first: left associativity
            while (not operators.is_empty() and operators.peek() in precedence
                   and precedence[operators.peek()] >= precedence[token]):
                output.append(operators.pop())
            operators.push(token)
        elif token == "(":
            operators.push(token)
        elif token == ")":
            while operators.peek() != "(":
                output.append(operators.pop())
            operators.pop()                      # discard the "("
        else:
            output.append(token)                 # a number goes straight through
    while not operators.is_empty():
        output.append(operators.pop())
    return output
