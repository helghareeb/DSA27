"""SOLUTION — try the exercise in `dsa/dynamic_array.py` first; see `solutions/README.md`.

Dynamic array — what Python's `list` actually is underneath.

Built on the course `Array` (`dsa/array.py`): a fixed-size block that is
reallocated when it fills. The payoff is
`amortised` O(1) append: most appends are cheap, a few are expensive, and the
average stays constant. Doubling the capacity is what makes that true —
growing by a constant instead gives O(n) amortised, which is worth measuring
with `viz.complexity.measure` rather than just asserting.
"""

from __future__ import annotations

from dsa.array import Array


def make_block(capacity):
    """Allocate a fixed-size block of `capacity` slots, every one None.

    This is the one piece we hand you: an `Array` is a genuinely fixed-size,
    C-style array, so the reallocation you write is real rather than simulated
    on top of another list. Growing means: make a bigger block, copy, switch.
    """
    return Array(capacity)


class DynamicArray:
    """A growable array with O(1) indexing and amortised O(1) append."""

    def __init__(self, values=(), growth=2):
        self._size = 0
        self._capacity = 1
        self._block = make_block(self._capacity)
        self.growth = growth
        #: number of reallocations so far — plot this against n
        self.resize_count = 0
        for value in values:
            self.append(value)

    def append(self, value):
        """Add to the end. Target: amortised O(1).

        Call `_resize(self._capacity * self.growth)` when full.
        """
        if self._size == self._capacity:
            self._resize(self._capacity * self.growth)
        self._block[self._size] = value
        self._size += 1

    def insert_at(self, index, value):
        """Insert at `index`, shifting the rest right. Target: O(n).

        Raises IndexError unless 0 <= index <= len(self), as `insert_at` does
        in Week 2 and in the linked list. Inserting at len(self) appends.
        """
        if not 0 <= index <= self._size:
            raise IndexError(index)
        if self._size == self._capacity:
            self._resize(self._capacity * self.growth)
        for i in range(self._size, index, -1):
            self._block[i] = self._block[i - 1]
        self._block[index] = value
        self._size += 1

    def pop(self, index=-1):
        """Remove and return the value at `index`. Target: O(n), O(1) at the end.

        Raises IndexError when empty.
        """
        if self._size == 0:
            raise IndexError("pop from empty DynamicArray")
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        value = self._block[index]
        for i in range(index, self._size - 1):
            self._block[i] = self._block[i + 1]
        self._size -= 1
        self._block[self._size] = None
        return value

    def _resize(self, capacity):
        """Move every element into a fresh block of `capacity` slots.

        Remember to increment `self.resize_count` — the notebook plots it.
        """
        block = make_block(capacity)
        for i in range(self._size):
            block[i] = self._block[i]
        self._block = block
        self._capacity = capacity
        self.resize_count += 1

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        """Target: O(1). Support negative indices; raise IndexError otherwise."""
        if index < 0:
            index += self._size               # -1 means the last USED slot
        if not 0 <= index < self._size:
            raise IndexError(index)
        return self._block[index]

    def __setitem__(self, index, value):
        """a[index] = value. Target: O(1). Same indices, and errors, as __getitem__."""
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        self._block[index] = value

    def __iter__(self):
        for i in range(self._size):
            yield self._block[i]

    def __repr__(self):
        return "DynamicArray([" + ", ".join(repr(v) for v in self) + "])"
