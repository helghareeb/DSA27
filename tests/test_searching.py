"""Searching exercises. These fail until `dsa/searching.py` is written."""

import random

import pytest

from dsa import searching

pytestmark = pytest.mark.challenge

SORTED_SEARCHES = [
    searching.binary_search,
    searching.binary_search_recursive,
    searching.jump_search,
    searching.exponential_search,
    searching.interpolation_search,
]


def test_linear_search_works_on_unsorted_data():
    assert searching.linear_search([5, 2, 9], 9) == 2
    assert searching.linear_search([5, 2, 9], 7) == -1
    assert searching.linear_search([], 1) == -1


@pytest.mark.parametrize("search", SORTED_SEARCHES, ids=lambda f: f.__name__)
@pytest.mark.parametrize("target,expected", [(1, 0), (5, 2), (9, 4), (4, -1)])
def test_finds_target_in_sorted_list(search, target, expected):
    assert search([1, 3, 5, 7, 9], target) == expected


@pytest.mark.parametrize("search", SORTED_SEARCHES, ids=lambda f: f.__name__)
def test_handles_empty_and_single_element(search):
    assert search([], 1) == -1
    assert search([42], 42) == 0
    assert search([42], 7) == -1


@pytest.mark.parametrize("search", SORTED_SEARCHES, ids=lambda f: f.__name__)
def test_finds_first_and_last_element(search):
    values = list(range(0, 100, 2))
    assert search(values, 0) == 0
    assert search(values, 98) == len(values) - 1


@pytest.mark.parametrize("search", SORTED_SEARCHES, ids=lambda f: f.__name__)
def test_agrees_with_linear_search_on_random_data(search):
    rng = random.Random(27)
    for _ in range(30):
        values = sorted(rng.sample(range(200), rng.randint(1, 40)))
        target = rng.randint(0, 200)
        expected = values.index(target) if target in values else -1
        assert search(values, target) == expected


def test_lower_bound():
    values = [1, 2, 2, 2, 5]
    assert searching.lower_bound(values, 2) == 1
    assert searching.lower_bound(values, 0) == 0
    assert searching.lower_bound(values, 6) == 5
    assert searching.lower_bound(values, 3) == 4


def test_upper_bound():
    values = [1, 2, 2, 2, 5]
    assert searching.upper_bound(values, 2) == 4
    assert searching.upper_bound(values, 0) == 0
    assert searching.upper_bound(values, 5) == 5


def test_bounds_count_duplicates():
    """The reason both bounds are worth writing."""
    values = [1, 2, 2, 2, 2, 5]
    count = searching.upper_bound(values, 2) - searching.lower_bound(values, 2)
    assert count == 4


def test_binary_search_does_not_scan_linearly():
    """A 1e6-element search must be fast — catches an accidental O(n) loop."""
    values = list(range(1_000_000))
    assert searching.binary_search(values, 999_999) == 999_999
