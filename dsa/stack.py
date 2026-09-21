"""Stack — last in, first out.

Deliberately a thin structure: the interesting part is what you *do* with it
(balanced brackets, infix to postfix, undo history, DFS without recursion).
"""

from __future__ import annotations


class Stack:
    """LIFO. Every operation should be O(1)."""

    def __init__(self, values=()):
        self._items = []
        for value in values:
            self.push(value)

    def push(self, value):
        """Add to the top. Target: O(1)."""
        raise NotImplementedError

    def pop(self):
        """Remove and return the top. Target: O(1). Raises IndexError when empty."""
        raise NotImplementedError

    def peek(self):
        """Return the top without removing it. Raises IndexError when empty."""
        raise NotImplementedError

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items!r})  # top = {self._items[-1]!r}" if self._items else "Stack([])"


# -- challenges -----------------------------------------------------------


def is_balanced(text):
    """True when every bracket in `text` is closed in the right order.

    "(a[b]{c})" -> True ;  "(a[b)]" -> False ;  "(" -> False

    The canonical first use of a stack. Target: O(n).
    """
    raise NotImplementedError


def infix_to_postfix(tokens):
    """Shunting-yard: ["3","+","4","*","2"] -> ["3","4","2","*","+"].

    Target: O(n). Handles + - * / and parentheses.
    """
    raise NotImplementedError
