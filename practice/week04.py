"""Question bank, Week 4 — dynamic arrays. Problems W4-C1 to W4-C3.

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
    raise NotImplementedError


def copies_for(n, grow):
    """W4-C2. How many elements are copied during n appends.

    Start empty with capacity 1. `grow` is a function from the old capacity to
    the new one, applied when an append finds the array full; that resize copies
    every element already stored.

    copies_for(5, lambda c: 2 * c) -> 7       (resizes copy 1, 2, then 4)
    copies_for(5, lambda c: c + 1) -> 10      (copies 1 + 2 + 3 + 4)

    Count, do not simulate with real arrays: O(n) time, O(1) space.
    """
    raise NotImplementedError


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
        raise NotImplementedError

    @property
    def capacity(self):
        raise NotImplementedError

    def append(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError
