"""SOLUTION — try the exercise in `dsa/linked_list.py` first; see `solutions/README.md`.

Singly linked list.

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
        self.head = Node(value, self.head)       # the new node points at the old head
        self._size += 1

    def append(self, value):
        """Insert at the tail. Target: O(n) without a tail pointer.

        Challenge: add a `_tail` reference and get this to O(1). What does
        that cost you in `pop_front` and in `remove`?
        """
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:     # walk to the last node: O(n)
                current = current.next
            current.next = node
        self._size += 1

    def insert_at(self, index, value):
        """Insert so that the new node ends up at `index`. Target: O(n).

        Raises IndexError unless 0 <= index <= len(self).
        """
        if not 0 <= index <= self._size:
            raise IndexError(index)
        if index == 0:
            self.push_front(value)
            return
        prev = self.head
        for _ in range(index - 1):               # stop at the node BEFORE the gap
            prev = prev.next
        prev.next = Node(value, prev.next)       # the new node takes prev's link
        self._size += 1

    # -- removing -------------------------------------------------------

    def pop_front(self):
        """Remove and return the head value. Target: O(1).

        Raises IndexError when empty.
        """
        if self.head is None:
            raise IndexError("pop from empty list")
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        return value

    def remove(self, value):
        """Remove the first node holding `value`. Target: O(n).

        Returns True when something was removed, False otherwise.
        """
        if self.head is None:
            return False
        if self.head.value == value:             # the special case: no node before it
            self.head = self.head.next
            self._size -= 1
            return True
        prev = self.head
        while prev.next is not None:
            if prev.next.value == value:
                prev.next = prev.next.next       # bypass the node
                self._size -= 1
                return True
            prev = prev.next
        return False

    # -- reading --------------------------------------------------------

    def find(self, value):
        """Return the index of the first node holding `value`, else -1."""
        index, node = 0, self.head
        while node is not None:
            if node.value == value:
                return index
            node = node.next
            index += 1
        return -1

    def reverse(self):
        """Reverse the list in place. Target: O(n) time, O(1) extra space.

        The classic three-pointer problem. Draw it before you code it.
        """
        prev, current = None, self.head
        while current is not None:
            following = current.next             # remember the rest of the list
            current.next = prev                  # turn this link round
            prev, current = current, following   # step forward
        self.head = prev

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

        Raises IndexError unless 0 <= index < len(self).

        Contrast with `dsa.dynamic_array.DynamicArray.__getitem__`, which is
        O(1). Same interface, completely different cost.
        """
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError(index)
        node = self.head
        for _ in range(index):                   # index steps: there is no jumping ahead
            node = node.next
        return node.value

    def __repr__(self):
        return "LinkedList([" + ", ".join(repr(v) for v in self) + "])"
