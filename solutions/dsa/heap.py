"""SOLUTION — try the exercise in `dsa/heap.py` first; see `solutions/README.md`.

Binary heaps and priority queues — where the array *is* the tree.

A heap is a complete binary tree stored in a flat array — the course
`DynamicArray` from Week 4. No nodes, no pointers: the shape is arithmetic.

    parent(i) = (i - 1) // 2      left(i) = 2*i + 1      right(i) = 2*i + 2

The **heap property**: every parent beats its children; siblings are unordered.
That is enough to keep the best element at index 0, and cheap enough to restore
after a change in O(log n). `heapify` builds a heap from arbitrary data in O(n)
by sifting down from the last parent back to the root — the same loop that
opens `heap_sort` in `solutions/dsa/sorting.py`.
"""

from __future__ import annotations

from dsa.dynamic_array import DynamicArray


class MinHeap:
    """Smallest value always at the root. push/pop O(log n), peek O(1)."""

    def __init__(self, values=()):
        self._items = DynamicArray(values)
        if len(self._items):
            self.heapify()

    # -- the comparison that defines the heap -----------------------------

    def _beats(self, child, parent):
        """True when `child` must move above `parent`."""
        return child < parent

    # -- restoring the heap property --------------------------------------

    def _sift_up(self, index):
        """Move the item at `index` up until its parent beats it. O(log n)."""
        items = self._items
        while index > 0:
            parent = (index - 1) // 2
            if not self._beats(items[index], items[parent]):
                return
            items[index], items[parent] = items[parent], items[index]
            index = parent

    def _sift_down(self, index):
        """Move the item at `index` down past its better child. O(log n)."""
        items = self._items
        size = len(items)
        while True:
            best = index
            left, right = 2 * index + 1, 2 * index + 2
            if left < size and self._beats(items[left], items[best]):
                best = left
            if right < size and self._beats(items[right], items[best]):
                best = right
            if best == index:
                return
            items[index], items[best] = items[best], items[index]
            index = best

    # -- the operations ---------------------------------------------------

    def push(self, value):
        """Add a value: append at the end, then sift it up. O(log n)."""
        self._items.append(value)
        self._sift_up(len(self._items) - 1)

    def pop(self):
        """Remove and return the best value. O(log n). IndexError when empty."""
        if len(self._items) == 0:
            raise IndexError("pop from an empty heap")
        last = self._items.pop()              # O(1): the end of the array
        if len(self._items) == 0:
            return last                       # it was the only item
        best = self._items[0]
        self._items[0] = last                 # the last leaf fills the hole
        self._sift_down(0)
        return best

    def peek(self):
        """Return the best value without removing it. O(1). IndexError when empty."""
        if len(self._items) == 0:
            raise IndexError("peek at an empty heap")
        return self._items[0]

    def heapify(self):
        """Rearrange `self._items` in place into a valid heap. O(n)."""
        for index in range(len(self._items) // 2 - 1, -1, -1):
            self._sift_down(index)

    def is_valid(self):
        """True when no child beats its parent. O(n)."""
        items = self._items
        for child in range(1, len(items)):
            if self._beats(items[child], items[(child - 1) // 2]):
                return False
        return True

    # -- plumbing ---------------------------------------------------------

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"{type(self).__name__}({list(self._items)!r})"


class MaxHeap(MinHeap):
    """Largest value at the root. One line different, by design."""

    def _beats(self, child, parent):
        return child > parent


class PriorityQueue:
    """A queue that serves the most urgent item, not the oldest one.

    Lower priority number = served first. Built on MinHeap: each entry is the
    triple (priority, order, item). Tuples compare left to right, and `order`
    is unique, so the comparison is settled before it ever reaches `item` —
    and among equal priorities the earlier arrival wins: first come, first
    served.
    """

    def __init__(self):
        self._heap = MinHeap()
        self._counter = 0

    def enqueue(self, item, priority):
        """Add `item` with the given priority. O(log n)."""
        self._heap.push((priority, self._counter, item))
        self._counter += 1

    def dequeue(self):
        """Remove and return the lowest-priority-number item. O(log n)."""
        if self._heap.is_empty():
            raise IndexError("dequeue from an empty priority queue")
        return self._heap.pop()[2]

    def peek(self):
        """Return the next item without removing it. O(1). IndexError if empty."""
        if self._heap.is_empty():
            raise IndexError("peek at an empty priority queue")
        return self._heap.peek()[2]

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)
