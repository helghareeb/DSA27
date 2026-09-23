"""Array — the one storage primitive every structure in this course is built on.

A fixed number of slots, side by side in memory, each reachable in O(1) by its
index. That is all. It cannot grow, it cannot shrink, it cannot insert, it
cannot slice. Everything else — a list that grows, a stack, a queue, a heap, a
hash table — you build on top of it, and so you pay, and see, every cost.

This module is **given to you**, like `viz/`. It is not an exercise.

    from dsa.array import Array

    a = Array(5)            # five slots, every one None
    a[0] = 42               # O(1)
    a[0]                    # O(1) -> 42
    len(a)                  # 5 — the capacity, fixed at creation
    a[5]                    # IndexError: there is no slot 5
    a[-1]                   # IndexError: no negative indices, as in C

    Array.from_values([3, 1, 2])   # a full array, handy in tests and the REPL

Underneath is a real C array of object references, made with `ctypes`, not a
Python `list` in disguise — so the fixed size is genuine, not simulated.

The course rule, from Lecture 02: a data structure in `dsa/` stores its data
only in an `Array`, in node objects, or in another structure you have built in
`dsa/`. Never in a Python `list`, `dict` or `set`.
"""

from __future__ import annotations

import ctypes
import operator


class Array:
    """A fixed-size, C-style array of object references."""

    __slots__ = ("_block", "_length")

    def __init__(self, length, fill=None):
        length = operator.index(length)       # an int, or TypeError
        if length < 0:
            raise ValueError(f"Array length must be >= 0, got {length}")
        self._length = length
        self._block = (length * ctypes.py_object)()
        for i in range(length):               # a fresh ctypes slot is NULL
            self._block[i] = fill

    @classmethod
    def from_values(cls, values):
        """A new Array holding `values`, exactly as many slots as values. O(n)."""
        values = tuple(values)
        result = cls(len(values))
        for i, value in enumerate(values):
            result._block[i] = value
        return result

    def _check(self, index):
        if isinstance(index, slice):
            raise TypeError("Array does not support slicing; copy with a loop")
        index = operator.index(index)
        if not 0 <= index < self._length:
            raise IndexError(
                f"Array index {index} out of range for length {self._length} "
                f"(valid: 0..{self._length - 1}; no negative indices)"
            )
        return index

    def __getitem__(self, index):
        """a[i]. O(1)."""
        return self._block[self._check(index)]

    def __setitem__(self, index, value):
        """a[i] = value. O(1)."""
        self._block[self._check(index)] = value

    def __len__(self):
        """The number of slots — the capacity, never the number "in use"."""
        return self._length

    def __iter__(self):
        for i in range(self._length):
            yield self._block[i]

    def __repr__(self):
        return "Array([" + ", ".join(repr(v) for v in self) + "])"
