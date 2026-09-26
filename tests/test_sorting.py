"""Sorting exercises. These fail until `dsa/sorting.py` is written.

Every algorithm is held to the same contract, so the parametrised tests below
cover all of them at once — add a new sort to the list and it is tested.
"""

import random

import pytest

from dsa import sorting

pytestmark = pytest.mark.challenge

SORTS = [
    sorting.bubble_sort,
    sorting.selection_sort,
    sorting.insertion_sort,
    sorting.merge_sort,
    sorting.quick_sort,
    sorting.heap_sort,
]

STEP_SORTS = [
    sorting.bubble_sort_steps,
    sorting.selection_sort_steps,
    sorting.insertion_sort_steps,
    sorting.merge_sort_steps,
    sorting.quick_sort_steps,
    sorting.heap_sort_steps,
]

CASES = [
    [],
    [1],
    [2, 1],
    [5, 2, 9, 1, 7],
    [3, 3, 3],
    [1, 2, 3, 4, 5],           # already sorted
    [5, 4, 3, 2, 1],           # reversed — quicksort's worst case if pivot=first
    [0, -3, 7, -1, 2],         # negatives
]


def test_is_sorted_helper():
    assert sorting.is_sorted([1, 2, 2, 3])
    assert not sorting.is_sorted([2, 1])
    assert sorting.is_sorted([])


@pytest.mark.parametrize("sort", SORTS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("values", CASES, ids=str)
def test_sorts_correctly(sort, values):
    assert sort(values) == sorted(values)


@pytest.mark.parametrize("sort", SORTS, ids=lambda f: f.__name__)
def test_does_not_mutate_the_input(sort):
    values = [5, 2, 9, 1]
    original = list(values)
    sort(values)
    assert values == original, "sort a copy — callers do not expect their list changed"


@pytest.mark.parametrize("sort", SORTS, ids=lambda f: f.__name__)
def test_sorts_random_lists(sort):
    rng = random.Random(27)
    for _ in range(20):
        values = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        assert sort(values) == sorted(values)


@pytest.mark.parametrize("steps", STEP_SORTS, ids=lambda f: f.__name__)
def test_step_form_is_a_generator_ending_sorted(steps):
    """The `_steps` form must yield snapshots and finish in sorted order."""
    from viz.animate import normalise_frames

    frames = normalise_frames(steps([5, 2, 9, 1, 7]))
    assert len(frames) >= 1, "yield at least one snapshot"
    final, _ = frames[-1]
    assert final == [1, 2, 5, 7, 9]


@pytest.mark.parametrize("steps", STEP_SORTS, ids=lambda f: f.__name__)
def test_step_frames_are_independent_snapshots(steps):
    """Each frame must be its own list, or the animation shows one static state."""
    from viz.animate import normalise_frames

    frames = normalise_frames(steps([4, 3, 2, 1]))
    states = [tuple(values) for values, _ in frames]
    assert len(set(states)) > 1, "frames never change — are you yielding the same list?"


def test_quick_sort_survives_its_worst_case_input():
    """Sorted input with a bad pivot is O(n^2); it must still return correctly."""
    values = list(range(200))
    assert sorting.quick_sort(values) == values


def test_counting_sort():
    assert sorting.counting_sort([3, 1, 4, 1, 5, 0]) == [0, 1, 1, 3, 4, 5]
    assert sorting.counting_sort([]) == []


class Card:
    """Compared by `key` only, so two cards with the same key are EQUAL to the
    sort while their labels still tell them apart. (Plain tuples would not do:
    (1, "a") < (1, "c"), so tuples with equal first items are not equal, and a
    sort that loses stability would still return the right list.)"""

    def __init__(self, key, label):
        self.key, self.label = key, label

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __le__(self, other):
        return self.key <= other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __repr__(self):
        return f"{self.key}{self.label}"


def test_insertion_sort_is_stable():
    """Equal keys keep their original relative order."""
    cards = [Card(1, "a"), Card(0, "b"), Card(1, "c"), Card(0, "d")]
    result = sorting.insertion_sort(cards)
    assert [repr(c) for c in result] == ["0b", "0d", "1a", "1c"]
