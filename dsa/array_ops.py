"""Array operations — Week 2, where complexity meets its first structure.

Every function here works on the course `Array` (`dsa/array.py`): fixed size,
O(1) indexing, and nothing else. No slicing, no `append`, no `insert`, no
converting to a `list` and back. You move the elements yourself, one index at a
time — which is exactly how you learn what each operation costs.

Several functions work on a **partly filled** array: `size` says how many slots,
counting from index 0, hold real data. The rest are free. This is the
"capacity versus size" split that a dynamic array (Week 4) is built on.

    arr = Array(5)          # capacity 5
    size = 0                # nothing in use yet
    size = insert_at(arr, size, 0, "b")    # [b, _, _, _, _]  size 1
    size = insert_at(arr, size, 0, "a")    # [a, b, _, _, _]  size 2

Declared in the bylaw: "arrays" (CS2101, AI 2020 p. 44), and "the basics of
algorithmic analysis" (IS122, SWE 2013 p. 38; Medical Informatics 2014 p. 35).
"""

from __future__ import annotations

from dsa.array import Array


# -- reading: no element moves ----------------------------------------------


def find(arr, target, size=None):
    """Index of the first slot equal to `target`, or -1. Linear search.

    Only the first `size` slots are searched (all of them when size is None).

    find(Array.from_values([4, 7, 7]), 7) -> 1

    Best case O(1), worst case O(n). Which inputs give each?
    """
    raise NotImplementedError


def is_sorted(arr, size=None):
    """True when the first `size` slots are in non-decreasing order.

    Empty and one-element arrays are sorted. Target: O(n), and stop at the
    first pair that is out of order.
    """
    raise NotImplementedError


# -- writing: elements shift ------------------------------------------------


def insert_at(arr, size, index, value):
    """Insert `value` at `index` in a partly filled array; return the new size.

    Shift slots index .. size-1 one place RIGHT first — starting from the end,
    or you overwrite what you have not moved yet.

    Raises OverflowError when the array is full (size == len(arr)), and
    IndexError unless 0 <= index <= size. Inserting at index == size appends.

    Target: O(n) — O(size - index) shifts. Inserting at the end costs O(1).
    """
    raise NotImplementedError


def remove_at(arr, size, index):
    """Remove and return the value at `index` from a partly filled array.

    Shift slots index+1 .. size-1 one place LEFT, then set the slot that is
    no longer in use to None. The caller's new size is size - 1.

    Raises IndexError unless 0 <= index < size.

    Target: O(n) — O(size - index - 1) shifts.
    """
    raise NotImplementedError


def reverse_in_place(arr):
    """Reverse the whole array without a second array.

    Two indices, one from each end, swapping as they walk towards each other.
    Target: O(n) time, O(1) extra space.
    """
    raise NotImplementedError


def rotate_left(arr, k):
    """Move every element k places to the left, in place, wrapping around.

    [1, 2, 3, 4, 5] rotated by 2 -> [3, 4, 5, 1, 2]. k may exceed len(arr).

    Target: O(n) time and O(1) extra space. Hint: three reversals. Write a
    helper that reverses the slots between two indices.
    """
    raise NotImplementedError


# -- making new arrays ------------------------------------------------------


def resized(arr, new_length):
    """A NEW Array of `new_length` slots holding arr's values from index 0.

    Values that do not fit are dropped; extra slots are None. `arr` is not
    changed. This is the move a dynamic array makes when it fills up.

    Target: O(new_length).
    """
    raise NotImplementedError


def merge_sorted(a, b):
    """A NEW Array holding every value of the sorted arrays a and b, sorted.

    Walk both with one index each, always taking the smaller front value.
    Target: O(len(a) + len(b)). This is half of merge sort (Week 10).
    """
    raise NotImplementedError


# -- two dimensions in one --------------------------------------------------


def transpose_flat(arr, rows, cols):
    """Transpose a rows x cols matrix stored flat, row by row, in `arr`.

    Element (r, c) lives at index r * cols + c ("row-major order"). Return a
    NEW Array holding the cols x rows transpose, also row-major.

    transpose_flat(Array.from_values([1, 2, 3,
                                      4, 5, 6]), 2, 3)
        -> Array([1, 4, 2, 5, 3, 6])

    Raises ValueError when len(arr) != rows * cols. Target: O(rows * cols).
    """
    raise NotImplementedError
