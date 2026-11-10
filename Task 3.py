"""Lab 03"""


def unique_in_order(values):
    seen = set()
    result = []
    for v in values:
        if v not in seen:
            seen.add(v)
            result.append(v)
    return result


def word_frequencies(text):
    # ASSUMPTION: words are lower-cased. Check the docstring.
    freq = {}
    for word in text.lower().split():
        word = word.strip('.,;:!?')
        if word:
            freq[word] = freq.get(word, 0) + 1
    return freq


def _sort_key(pair):
    # pair = (word, count): highest count first, then A to Z
    return (-pair[1], pair[0])


def top_k(frequencies, k):
    ordered = sorted(frequencies.items(), key=_sort_key)
    return ordered[:k]


def transpose(matrix):
    if not matrix:
        return []
    result = []
    for c in range(len(matrix[0])):
        new_row = []
        for row in matrix:
            new_row.append(row[c])
        result.append(new_row)
    return result


def invert(mapping):
    # value -> sorted list of keys that had that value
    result = {}
    for key, value in mapping.items():
        result.setdefault(value, []).append(key)
    for value in result:
        result[value].sort()
    return result


def common_elements(first, second):
    # ASSUMPTION: sorted list. Return the set itself if the docstring says so.
    return sorted(set(first) & set(second))


def group_by_length(words):
    result = {}
    for word in words:
        result.setdefault(len(word), []).append(word)
    return result


class Bag:
    """A multiset: like a set, but it counts how many copies of each item."""

    def __init__(self, items=()):
        self._counts = {}
        self._total = 0
        for item in items:
            self.add(item)

    def add(self, item, times=1):
        self._counts[item] = self._counts.get(item, 0) + times
        self._total += times

    def remove(self, item, times=1):
        # ASSUMPTION: KeyError if the item is not there. Check the docstring/test.
        if self._counts.get(item, 0) < times:
            raise KeyError(item)
        self._counts[item] -= times
        self._total -= times
        if self._counts[item] == 0:
            del self._counts[item]  # delete the key with the last copy

    def count(self, item):
        return self._counts.get(item, 0)

    def distinct(self):
        # ASSUMPTION: returns a set of the different items.
        return set(self._counts)

    def __len__(self):
        return self._total  # O(1)

    def __contains__(self, item):
        return item in self._counts

    def __iter__(self):
        for item, n in self._counts.items():
            for _ in range(n):
                yield item

    def __eq__(self, other):
        if not isinstance(other, Bag):
            return NotImplemented
        return self._counts == other._counts

    def __repr__(self):
        return f'Bag({sorted(self)!r})'


def countdown(n):
    # ASSUMPTION: yields n, n-1, ..., 1. Check whether 0 is included.
    while n > 0:
        yield n
        n -= 1


def chunks(values, size):
    # The check is inside the generator, so the ValueError is raised
    # on the first next(), not when chunks() is called. Read the test to confirm.
    if size <= 0:
        raise ValueError('size must be positive')
    for start in range(0, len(values), size):
        yield values[start:start + size]