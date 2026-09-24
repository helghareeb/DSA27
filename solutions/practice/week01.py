"""SOLUTION — try the problems in `practice/week01.py` first; see `solutions/README.md`.

Question bank, Week 1 — Python basics. Problems W1-C1 to W1-C4.

Questions:  docs/question-bank/week01-questions.md
Tests:      tests/test_practice_week01.py

Use strings, lists, slicing, `while`/`for` and `if`. No imports.
"""


def count_vowels(text):
    """W1-C1. How many of the letters a, e, i, o, u appear in `text`, in
    either case.

    count_vowels("Data Structures") -> 5
    count_vowels("rhythm")          -> 0
    """
    count = 0
    for ch in text.lower():
        if ch in "aeiou":
            count += 1
    return count


def second_largest(values):
    """W1-C2. The largest value that is strictly smaller than the maximum.

    Do it in ONE pass over the list, without sorting.
    Raise ValueError if there is no such value (fewer than two distinct values).

    second_largest([4, 9, 2, 9, 7]) -> 7
    second_largest([5, 5])          -> ValueError
    """
    largest = second = None
    for v in values:
        if largest is None or v > largest:
            if largest is not None:
                second = largest          # the old maximum is now second
            largest = v
        elif v != largest and (second is None or v > second):
            second = v
    if second is None:
        raise ValueError("need at least two distinct values")
    return second


def compress(text):
    """W1-C3. Run-length encoding: each run of a repeated character becomes the
    character followed by the length of the run.

    compress("aaabcc") -> "a3b1c2"
    compress("")       -> ""
    """
    result = ""
    i = 0
    while i < len(text):
        j = i
        while j < len(text) and text[j] == text[i]:
            j += 1                        # j stops at the end of the run
        result += text[i] + str(j - i)
        i = j
    return result


def is_anagram(first, second):
    """W1-C4. True if the two strings use exactly the same letters the same
    number of times, ignoring case and spaces.

    is_anagram("Dormitory", "dirty room") -> True
    is_anagram("abc", "abcc")             -> False
    """
    a = sorted(first.replace(" ", "").lower())
    b = sorted(second.replace(" ", "").lower())
    return a == b
