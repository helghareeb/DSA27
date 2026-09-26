"""SOLUTION — try the exercise in `dsa/hashmap.py` first; see `solutions/README.md`.

Hash map — what Python's `dict` is underneath.

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
        i = self._index(key)
        entry = self._buckets[i]
        while entry is not None:                 # already here? overwrite
            if entry.key == key:
                entry.value = value
                return
            entry = entry.next
        self._buckets[i] = Entry(key, value, self._buckets[i])   # push on front
        self._size += 1
        if self._size / len(self._buckets) > self.max_load:
            self._resize(2 * len(self._buckets))

    def get(self, key, default=_MISSING):
        """Return the value, or `default`. Raises KeyError when neither exists."""
        entry = self._buckets[self._index(key)]
        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next
        if default is _MISSING:
            raise KeyError(key)
        return default

    def delete(self, key):
        """Remove `key`. Raises KeyError when absent."""
        i = self._index(key)
        prev, entry = None, self._buckets[i]
        while entry is not None:
            if entry.key == key:
                if prev is None:                 # first in its chain
                    self._buckets[i] = entry.next
                else:
                    prev.next = entry.next
                self._size -= 1
                return
            prev, entry = entry, entry.next
        raise KeyError(key)

    def _resize(self, capacity):
        """Rebuild into `capacity` buckets.

        Every key must be rehashed — the index depends on the bucket count, so
        you cannot copy buckets across.
        """
        old = self._buckets
        self._buckets = Array(capacity)
        for head in old:
            entry = head
            while entry is not None:
                nxt = entry.next                 # save it: we relink `entry`
                i = self._index(entry.key)       # new capacity, new index
                entry.next = self._buckets[i]
                self._buckets[i] = entry
                entry = nxt

    @property
    def load_factor(self):
        return self._size / len(self._buckets)

    def __len__(self):
        return self._size

    def __contains__(self, key):
        try:
            self.get(key)
        except KeyError:
            return False
        return True

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
        self._tombstones = 0                 # slots holding TOMBSTONE
        self.max_load = max_load

    def _probe(self, key):
        """Yield slot indices to try, in order, for `key`.

        Start at `hash(key) % capacity` and step by 1 (linear probing). Try
        quadratic probing as a challenge and compare the clustering.
        """
        capacity = len(self._keys)
        start = hash(key) % capacity
        for step in range(capacity):
            yield (start + step) % capacity

    def put(self, key, value):
        # Tombstones fill slots too: count them, or probes can find no None.
        capacity = len(self._keys)
        if (self._size + self._tombstones + 1) / capacity > self.max_load:
            if (self._size + 1) / capacity > self.max_load:
                capacity *= 2                    # genuinely fuller: grow
            self._resize(capacity)               # else just sweep tombstones
        first_free = None
        for i in self._probe(key):
            slot = self._keys[i]
            if slot is None:                     # end of the chain: key absent
                if first_free is None:
                    first_free = i
                break
            if slot is TOMBSTONE:
                if first_free is None:
                    first_free = i               # reuse it, but keep looking
            elif slot == key:
                self._values[i] = value          # overwrite
                return
        if self._keys[first_free] is TOMBSTONE:
            self._tombstones -= 1
        self._keys[first_free] = key
        self._values[first_free] = value
        self._size += 1

    def _find(self, key):
        """Slot index holding `key`, or -1."""
        for i in self._probe(key):
            slot = self._keys[i]
            if slot is None:                     # a never-used slot ends the chain
                return -1
            if slot is not TOMBSTONE and slot == key:
                return i
        return -1                                # probed every slot

    def get(self, key, default=_MISSING):
        i = self._find(key)
        if i >= 0:
            return self._values[i]
        if default is _MISSING:
            raise KeyError(key)
        return default

    def delete(self, key):
        """Remove `key`, leaving TOMBSTONE behind rather than None."""
        i = self._find(key)
        if i < 0:
            raise KeyError(key)
        self._keys[i] = TOMBSTONE
        self._values[i] = None
        self._size -= 1
        self._tombstones += 1

    def _resize(self, capacity):
        """Rebuild, dropping tombstones as you go."""
        old_keys, old_values = self._keys, self._values
        self._keys = Array(capacity)
        self._values = Array(capacity)
        self._size = 0
        self._tombstones = 0
        for i in range(len(old_keys)):
            key = old_keys[i]
            if key is not None and key is not TOMBSTONE:
                for j in self._probe(key):       # no tombstones, no duplicates:
                    if self._keys[j] is None:    # the first None is ours
                        self._keys[j] = key
                        self._values[j] = old_values[i]
                        self._size += 1
                        break

    @property
    def load_factor(self):
        return self._size / len(self._keys)

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self._find(key) >= 0

    def __iter__(self):
        for key in self._keys:
            if key is not None and key is not TOMBSTONE:
                yield key
