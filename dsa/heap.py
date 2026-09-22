"""Binary heaps and priority queues — where the array *is* the tree.

A heap is a complete binary tree stored in a flat list. No nodes, no pointers:
the shape is arithmetic.

    parent(i) = (i - 1) // 2      left(i) = 2*i + 1      right(i) = 2*i + 2

The **heap property** is weaker than a BST's: every parent beats its children,
but siblings are unordered. That is exactly enough to know the best element is
at index 0, and cheap enough to restore after a change in O(log n).

Declared in the bylaw: "heaps, priority queues" (CS2101, AI 2020 p. 44).

See your heap as a tree — no conversion needed, because it already is one:

    from viz.draw import draw_array_as_tree
    draw_array_as_tree(heap._items)
"""

from __future__ import annotations


class MinHeap:
    """Smallest value always at the root. push/pop O(log n), peek O(1)."""

    def __init__(self, values=()):
        self._items = []
        if values:
            self._items = list(values)
            self.heapify()

    # -- the comparison that defines the heap -----------------------------

    def _beats(self, child, parent):
        """True when `child` must move above `parent`.

        The **only** difference between a min-heap and a max-heap. Everything
        else in this class is shared, so write the rest once and get MaxHeap
        for free.
        """
        return child < parent

    # -- restoring the heap property --------------------------------------

    def _sift_up(self, index):
        """Move the item at `index` up until its parent beats it. O(log n).

        Used after appending to the end. Walk parent(i) = (i - 1) // 2.
        """
        raise NotImplementedError

    def _sift_down(self, index):
        """Move the item at `index` down past its better child. O(log n).

        Used after replacing the root. Compare against **both** children and
        swap with the better of the two — swapping with the wrong one silently
        breaks the invariant.
        """
        raise NotImplementedError

    # -- the operations ---------------------------------------------------

    def push(self, value):
        """Add a value. Target: O(log n).

        Append to the end, then sift it up.
        """
        raise NotImplementedError

    def pop(self):
        """Remove and return the best value. Target: O(log n).

        Take index 0, move the *last* item into its place, shrink, then sift
        down. Raises IndexError when empty.
        """
        raise NotImplementedError

    def peek(self):
        """Return the best value without removing it. Target: O(1).

        Raises IndexError when empty.
        """
        raise NotImplementedError

    def heapify(self):
        """Rearrange `self._items` in place until it is a valid heap.

        Target: **O(n)**, not O(n log n). Sift *down* from the last parent
        back to index 0. Pushing the items one at a time is O(n log n) and
        misses the point of this exercise.
        """
        raise NotImplementedError

    def is_valid(self):
        """True when every parent beats both its children. Target: O(n)."""
        raise NotImplementedError

    # -- plumbing ---------------------------------------------------------

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"{type(self).__name__}({self._items!r})"


class MaxHeap(MinHeap):
    """Largest value at the root. One line different, by design."""

    def _beats(self, child, parent):
        return child > parent


class PriorityQueue:
    """A queue that serves the most urgent item, not the oldest one.

    Lower priority number = served first.

        pq = PriorityQueue()
        pq.enqueue("write tests", 2)
        pq.enqueue("fix the build", 1)
        pq.dequeue()            # -> "fix the build"

    Build it **on top of** MinHeap rather than re-implementing the sifting.
    Ties may break in any order.
    """

    def __init__(self):
        self._heap = MinHeap()
        self._counter = 0

    def enqueue(self, item, priority):
        """Add `item` with the given priority. Target: O(log n).

        Store whatever the heap can compare. A bare (priority, item) pair
        breaks as soon as two items tie and Python falls through to comparing
        the items themselves — `self._counter` exists to stop that.
        """
        raise NotImplementedError

    def dequeue(self):
        """Remove and return the lowest-priority-number item. O(log n).

        Raises IndexError when empty. Returns the item, not the pair.
        """
        raise NotImplementedError

    def peek(self):
        """Return the next item without removing it. O(1). IndexError if empty."""
        raise NotImplementedError

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)
