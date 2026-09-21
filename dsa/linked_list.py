"""Singly linked list.

The first structure where a picture beats an explanation. Use
`viz.draw.draw_linked_list(list(ll), highlight=i)` while you walk a pointer
along it.
"""

from __future__ import annotations


class Node:
    """One cell: a value, and a reference to the next cell (or None)."""

    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"Node({self.value!r})"


class LinkedList:
    """A singly linked list holding a head reference and a length.

    Keeping `_size` updated as you go is what makes `__len__` O(1) instead of
    O(n) — a small decision worth discussing in class.
    """

    def __init__(self, values=()):
        self.head: Node | None = None
        self._size = 0
        for value in values:
            self.append(value)

    # -- building -------------------------------------------------------

    def push_front(self, value):
        """Insert at the head. Target: O(1)."""
        raise NotImplementedError

    def append(self, value):
        """Insert at the tail. Target: O(n) without a tail pointer.

        Challenge: add a `_tail` reference and get this to O(1). What does
        that cost you in `pop` and in `remove`?
        """
        raise NotImplementedError

    def insert_at(self, index, value):
        """Insert so that the new node ends up at `index`. Target: O(n).

        Raises IndexError unless 0 <= index <= len(self).
        """
        raise NotImplementedError

    # -- removing -------------------------------------------------------

    def pop_front(self):
        """Remove and return the head value. Target: O(1).

        Raises IndexError when empty.
        """
        raise NotImplementedError

    def remove(self, value):
        """Remove the first node holding `value`. Target: O(n).

        Returns True when something was removed, False otherwise.
        """
        raise NotImplementedError

    # -- reading --------------------------------------------------------

    def find(self, value):
        """Return the index of the first node holding `value`, else -1."""
        raise NotImplementedError

    def reverse(self):
        """Reverse the list in place. Target: O(n) time, O(1) extra space.

        The classic three-pointer problem. Draw it before you code it.
        """
        raise NotImplementedError

    # -- Python protocol ------------------------------------------------

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __getitem__(self, index):
        """Positional access. Target: O(n) — and that is the whole lesson.

        Contrast with `dsa.dynamic_array.DynamicArray.__getitem__`, which is
        O(1). Same interface, completely different cost.
        """
        raise NotImplementedError

    def __repr__(self):
        return "LinkedList([" + ", ".join(repr(v) for v in self) + "])"
