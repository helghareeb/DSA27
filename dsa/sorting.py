"""Sorting — basic and advanced.

Each algorithm appears twice:

  * `bubble_sort(values)`       -> returns a new sorted list
  * `bubble_sort_steps(values)` -> *generator* yielding (values, highlight)

The `_steps` form is what makes the animation work. Write it first and get the
plain form by exhausting it — that way there is only one implementation to
keep correct:

    def bubble_sort(values):
        for state, _ in bubble_sort_steps(values):
            pass
        return state

Then:

    from viz.animate import step_slider
    step_slider(bubble_sort_steps([5, 2, 9, 1, 7]))
"""

from __future__ import annotations

__all__ = [
    "bubble_sort", "bubble_sort_steps",
    "selection_sort", "selection_sort_steps",
    "insertion_sort", "insertion_sort_steps",
    "merge_sort", "merge_sort_steps",
    "quick_sort", "quick_sort_steps",
    "heap_sort", "heap_sort_steps",
    "counting_sort",
    "is_sorted",
]


def is_sorted(values):
    """True when `values` is non-decreasing. Handy in tests and assertions."""
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


# -- basic: O(n^2) --------------------------------------------------------


def bubble_sort_steps(values):
    """Yield (list, (i, j)) before each comparison. Target: O(n^2), O(1) space.

    Challenge: stop early when a whole pass makes no swap. What does that do
    to the best case?
    """
    raise NotImplementedError


def bubble_sort(values):
    raise NotImplementedError


def selection_sort_steps(values):
    """Repeatedly select the minimum of the unsorted tail. O(n^2).

    At most n-1 swaps — the fewest writes of any comparison sort, which
    matters when writes are expensive.
    """
    raise NotImplementedError


def selection_sort(values):
    raise NotImplementedError


def insertion_sort_steps(values):
    """Grow a sorted prefix one element at a time. O(n^2), but O(n) when nearly
    sorted — which is why real sorts fall back to it on small subarrays."""
    raise NotImplementedError


def insertion_sort(values):
    raise NotImplementedError


# -- advanced: O(n log n) -------------------------------------------------


def merge_sort_steps(values):
    """Divide, sort each half, merge. O(n log n) always, O(n) extra space.

    Stable, and the stability is a property of *how you break ties in merge* —
    take from the left half when equal.
    """
    raise NotImplementedError


def merge_sort(values):
    raise NotImplementedError


def quick_sort_steps(values, pivot="median3"):
    """Partition around a pivot, recurse. O(n log n) average, O(n^2) worst.

    Try `pivot="first"` on already-sorted input and watch it hit the worst
    case — then switch to "random" or "median3" and watch it recover. That
    experiment is the single best argument for randomisation in the course.
    """
    raise NotImplementedError


def quick_sort(values, pivot="median3"):
    raise NotImplementedError


def heap_sort_steps(values):
    """Build a max-heap in place, then repeatedly swap the root to the back.

    O(n log n) always, O(1) extra space, not stable. Visualise the heap with
    `viz.draw.draw_array_as_tree` — the array *is* the tree.
    """
    raise NotImplementedError


def heap_sort(values):
    raise NotImplementedError


# -- not a comparison sort ------------------------------------------------


def counting_sort(values, max_value=None):
    """Sort small non-negative integers by counting. O(n + k).

    Beats the O(n log n) comparison lower bound because it never compares two
    elements — a good moment to discuss what that lower bound actually assumes.
    """
    raise NotImplementedError
