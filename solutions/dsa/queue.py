"""SOLUTION — try the exercise in `dsa/queue.py` first; see `solutions/README.md`.

Queue — first in, first out.

Two implementations worth writing side by side, because the naive one hides an
O(n) cost that only shows up when you measure it:

  * `SlowQueue` dequeues with `DynamicArray.pop(0)` — O(n) per operation
  * `CircularQueue` uses head/tail indices in a fixed `Array` — O(1) per operation

Run both through `viz.complexity.measure` and plot. The gap is the lesson.
"""

from __future__ import annotations

from dsa.array import Array
from dsa.dynamic_array import DynamicArray


class SlowQueue:
    """FIFO on a DynamicArray. Correct, but dequeue is O(n) — prove it."""

    def __init__(self, values=()):
        self._items = DynamicArray(values)

    def enqueue(self, value):
        """Add to the back. O(1)."""
        self._items.append(value)

    def dequeue(self):
        """Remove from the front. O(n) here — every element shifts left."""
        if len(self._items) == 0:
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def __len__(self):
        return len(self._items)


class CircularQueue:
    """FIFO in a fixed-capacity ring buffer. Every operation O(1).

    `head` is where the next dequeue reads, `tail` where the next enqueue
    writes, and both wrap with `% capacity`. Tracking `_size` separately is
    what lets you tell "full" from "empty" when head == tail.
    """

    def __init__(self, capacity=8):
        self._block = Array(capacity)
        self._capacity = capacity
        self._head = 0
        self._size = 0

    def enqueue(self, value):
        """Add to the back. Target: O(1).

        Challenge: grow the ring when it fills, rather than raising. Careful —
        a naive copy scrambles the order once the data has wrapped around.
        """
        if self._size == self._capacity:
            self._grow(max(1, 2 * self._capacity))
        self._block[(self._head + self._size) % self._capacity] = value
        self._size += 1

    def dequeue(self):
        """Remove from the front. Target: O(1). Raises IndexError when empty."""
        if self._size == 0:
            raise IndexError("dequeue from empty queue")
        value = self._block[self._head]
        self._block[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return value

    def _grow(self, capacity):
        """Copy into a bigger block in QUEUE order, so the front lands in slot 0."""
        bigger = Array(capacity)
        for offset in range(self._size):
            bigger[offset] = self._block[(self._head + offset) % self._capacity]
        self._block, self._capacity, self._head = bigger, capacity, 0

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def __len__(self):
        return self._size

    def __iter__(self):
        for offset in range(self._size):
            yield self._block[(self._head + offset) % self._capacity]

    def __repr__(self):
        return "CircularQueue([" + ", ".join(repr(v) for v in self) + "])"
