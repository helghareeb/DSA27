"""Hash map — what Python's `dict` is underneath.

Build it twice. Chaining is easier to get right; open addressing is what
CPython actually does, and its delete is subtly hard (you cannot just blank a
slot, or you break the probe chain that runs through it — hence tombstones).

Watch the load factor: keep it under ~0.7 and lookups stay O(1) on average.
Let it approach 1.0 and you are doing linear search with extra steps. Measure
it — `viz.complexity.measure` over rising load factors makes the cliff visible.

Both are built on the course `Array` (`dsa/array.py`): a fixed row of slots,
reached by index in O(1). Hashing is what turns a key into that index.
"""

from __future__ import annotations

from dsa.array import Array

_MISSING = object()
#: Marks a slot whose key was deleted but which a probe chain still runs through.
TOMBSTONE = object()


class Entry:
    """One key/value pair in a chain. Given to you — a linked-list node."""

    __slots__ = ("key", "value", "next")

    def __init__(self, key, value, next=None):
        self.key = key
        self.value = value
        self.next = next

    def __repr__(self):
        return f"Entry({self.key!r}, {self.value!r})"


class ChainingHashMap:
    """Each bucket is a chain: None, or the first `Entry` of a linked list.

    Average O(1); worst case O(n) when every key lands in one bucket.
    """

    def __init__(self, capacity=8, max_load=0.75):
        self._buckets = Array(capacity)      # every slot starts as None
        self._size = 0
        self.max_load = max_load

    def _index(self, key):
        """Bucket index for `key`. Use Python's `hash()` — you are not writing
        a hash function, you are writing the table around one."""
        return hash(key) % len(self._buckets)

    def put(self, key, value):
        """Insert or overwrite. Resize when size/capacity exceeds max_load."""
        raise NotImplementedError

    def get(self, key, default=_MISSING):
        """Return the value, or `default`. Raises KeyError when neither exists."""
        raise NotImplementedError

    def delete(self, key):
        """Remove `key`. Raises KeyError when absent."""
        raise NotImplementedError

    def _resize(self, capacity):
        """Rebuild into `capacity` buckets.

        Every key must be rehashed — the index depends on the bucket count, so
        you cannot copy buckets across.
        """
        raise NotImplementedError

    @property
    def load_factor(self):
        return self._size / len(self._buckets)

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self.get(key, None) is not None

    def __iter__(self):
        for entry in self._buckets:
            while entry is not None:
                yield entry.key
                entry = entry.next


class OpenAddressingHashMap:
    """One entry per slot; on collision, probe forward for the next free one.

    Better cache behaviour than chaining, but deletion needs TOMBSTONE so that
    probe chains passing through a removed slot are not cut.
    """

    def __init__(self, capacity=8, max_load=0.66):
        self._keys = Array(capacity)         # None marks a never-used slot
        self._values = Array(capacity)
        self._size = 0
        self.max_load = max_load

    def _probe(self, key):
        """Yield slot indices to try, in order, for `key`.

        Start at `hash(key) % capacity` and step by 1 (linear probing). Try
        quadratic probing as a challenge and compare the clustering.
        """
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError

    def get(self, key, default=_MISSING):
        raise NotImplementedError

    def delete(self, key):
        """Remove `key`, leaving TOMBSTONE behind rather than None."""
        raise NotImplementedError

    def _resize(self, capacity):
        """Rebuild, dropping tombstones as you go."""
        raise NotImplementedError

    @property
    def load_factor(self):
        return self._size / len(self._keys)

    def __len__(self):
        return self._size
