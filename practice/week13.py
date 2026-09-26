"""Question bank, Week 13 — hash tables. Problems W13-C1 to W13-C5.

Questions:  docs/question-bank/week13-questions.md
Tests:      tests/test_practice_week13.py

Every problem here is O(n) with a hash map and O(n^2) without one — and the
tests use inputs large enough that O(n^2) is painfully slow. Use your own
`ChainingHashMap` from `dsa/hashmap.py` as the working storage, not a Python
`dict` or `set`: `put`, `get(key, default)`, `in` and `len` are all you need.
Lists are fine as inputs and results.
"""

from dsa.hashmap import ChainingHashMap  # noqa: F401  (your Week 13 exercise)


def two_sum(values, target):
    """W13-C1. Indices (i, j), i < j, with values[i] + values[j] == target.

    Scan left to right and return the pair with the smallest j; for that j,
    the smallest i. None when there is no such pair.

    two_sum([2, 7, 11, 15], 9)  -> (0, 1)
    two_sum([3, 2, 4], 6)       -> (1, 2)
    two_sum([3, 3], 6)          -> (0, 1)
    two_sum([1, 2], 10)         -> None

    O(n): remember, for each value seen so far, the first index it was seen at.
    """
    raise NotImplementedError


def first_repeated(items):
    """W13-C2. The first item to appear for the second time, or None.

    "First" means: the item whose SECOND occurrence comes earliest.

    first_repeated(["a", "b", "c", "b", "a"]) -> "b"
    first_repeated([1, 2, 3])                -> None

    O(n). The items are hashable.
    """
    raise NotImplementedError


def group_anagrams(words):
    """W13-C3. Group the words that are anagrams of one another.

    Return a list of groups. The groups come in the order of their first word
    in the input, and each group keeps its words in input order.

    group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        -> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

    O(n k log k) for n words of length at most k. Hint: two words are
    anagrams exactly when their sorted letters are equal — use that string as
    the key, and map it to the position of its group in the result.
    """
    raise NotImplementedError


def longest_distinct_run(text):
    """W13-C4. Length of the longest stretch of text with no repeated character.

    longest_distinct_run("abcabcbb") -> 3     ("abc")
    longest_distinct_run("pwwkew")   -> 3     ("wke")
    longest_distinct_run("")         -> 0

    O(n): slide a window, and remember where each character was last seen.
    """
    raise NotImplementedError


def count_subarrays_with_sum(values, k):
    """W13-C5. How many contiguous, non-empty runs of values add up to k?

    count_subarrays_with_sum([1, 1, 1], 2)  -> 2
    count_subarrays_with_sum([1, 2, 3], 3)  -> 2     ([1, 2] and [3])
    count_subarrays_with_sum([1, -1, 0], 0) -> 3

    Values may be negative. O(n): a run values[i:j] adds up to k exactly when
    prefix[j] - prefix[i] == k — count how often each prefix sum has occurred.
    """
    raise NotImplementedError
