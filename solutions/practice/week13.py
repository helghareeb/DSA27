"""SOLUTION — try the problems in `practice/week13.py` first; see `solutions/README.md`.

Question bank, Week 13 — hash tables. Problems W13-C1 to W13-C5.

Questions:  docs/question-bank/week13-questions.md
Tests:      tests/test_practice_week13.py

Every problem here is O(n) with a hash map and O(n^2) without one — and the
tests use inputs large enough that O(n^2) is painfully slow. Use your own
`ChainingHashMap` from `dsa/hashmap.py` as the working storage, not a Python
`dict` or `set`: `put`, `get(key, default)`, `in` and `len` are all you need.
Lists are fine as inputs and results.
"""

from dsa.hashmap import ChainingHashMap


def two_sum(values, target):
    """W13-C1. Indices (i, j), i < j, with values[i] + values[j] == target."""
    first_seen = ChainingHashMap()              # value -> first index seen
    for j, value in enumerate(values):
        i = first_seen.get(target - value, None)
        if i is not None:
            return (i, j)
        if value not in first_seen:
            first_seen.put(value, j)
    return None


def first_repeated(items):
    """W13-C2. The first item to appear for the second time, or None."""
    seen = ChainingHashMap()                    # used as a set: item -> True
    for item in items:
        if item in seen:
            return item
        seen.put(item, True)
    return None


def group_anagrams(words):
    """W13-C3. Group the words that are anagrams of one another."""
    groups = []
    where = ChainingHashMap()                   # sorted letters -> group index
    for word in words:
        key = "".join(sorted(word))
        i = where.get(key, None)
        if i is None:
            where.put(key, len(groups))
            groups.append([word])
        else:
            groups[i].append(word)
    return groups


def longest_distinct_run(text):
    """W13-C4. The longest stretch of text with no repeated character."""
    last_seen = ChainingHashMap()               # character -> last index
    start = best = 0
    for i, ch in enumerate(text):
        previous = last_seen.get(ch, -1)
        if previous >= start:                   # ch repeats inside the window
            start = previous + 1
        last_seen.put(ch, i)
        best = max(best, i - start + 1)
    return best


def count_subarrays_with_sum(values, k):
    """W13-C5. How many contiguous runs of values add up to k?"""
    seen = ChainingHashMap()                    # prefix sum -> times seen
    seen.put(0, 1)                              # the empty prefix
    total = count = 0
    for value in values:
        total += value
        count += seen.get(total - k, 0)
        seen.put(total, seen.get(total, 0) + 1)
    return count
