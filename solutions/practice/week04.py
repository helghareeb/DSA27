"""SOLUTION — try the problems in `practice/week04.py` first; see `solutions/README.md`.

Question bank, Week 4 — dynamic arrays. Problems W4-C1 to W4-C3.

Questions:  docs/question-bank/week04-questions.md
Tests:      tests/test_practice_week04.py

W4-C3 is a class: store its data only in the course `Array` — no Python list.
"""

from dsa.array import Array


def capacity_after(n, factor=2):
    """W4-C1. The capacity of a dynamic array after n appends.

    It starts empty with capacity 1, and when an append finds it full the
    capacity is multiplied by `factor` (a whole number >= 2) first.

    capacity_after(0) -> 1 ;  capacity_after(5) -> 8 ;  capacity_after(5, 3) -> 9
    """
    capacity, size = 1, 0
    for _ in range(n):
        if size == capacity:
            capacity *= factor
        size += 1
    return capacity


def copies_for(n, grow):
    """W4-C2. How many elements are copied during n appends.

    Start empty with capacity 1. `grow` is a function from the old capacity to
    the new one, applied when an append finds the array full; that resize copies
    every element already stored.

    copies_for(5, lambda c: 2 * c) -> 7       (resizes copy 1, 2, then 4)
    copies_for(5, lambda c: c + 1) -> 10      (copies 1 + 2 + 3 + 4)

    Count, do not simulate with real arrays: O(n) time, O(1) space.
    """
    capacity, size, copies = 1, 0, 0
    for _ in range(n):
        if size == capacity:
            copies += size               # the resize copies everything stored
            capacity = grow(capacity)
        size += 1
    return copies


class ShrinkingArray:
    """W4-C3. A dynamic array that also gives memory back.

    - append(value): if full, double the capacity first. Amortised O(1).
    - pop(): remove and return the LAST value (IndexError if empty). Afterwards,
      if size <= capacity // 4 and capacity > 1, halve the capacity.
    - len(a), a[i] for 0 <= i < len(a) (IndexError otherwise), a.capacity,
      a.resize_count (grows and shrinks both count).

    Starts empty with capacity 1. Store the data in an `Array`.
    """

    def __init__(self):
        self._block = Array(1)
        self._size = 0
        self.resize_count = 0

    @property
    def capacity(self):
        return len(self._block)

    def _resize(self, capacity):
        block = Array(capacity)
        for i in range(self._size):
            block[i] = self._block[i]
        self._block = block
        self.resize_count += 1

    def append(self, value):
        if self._size == self.capacity:
            self._resize(2 * self.capacity)
        self._block[self._size] = value
        self._size += 1

    def pop(self):
        if self._size == 0:
            raise IndexError("pop from empty array")
        self._size -= 1
        value = self._block[self._size]
        self._block[self._size] = None           # let the object be collected
        if self._size <= self.capacity // 4 and self.capacity > 1:
            self._resize(self.capacity // 2)
        return value

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        if not 0 <= index < self._size:
            raise IndexError(index)
        return self._block[index]
