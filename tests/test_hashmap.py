"""Hash map exercises. Fail until `dsa/hashmap.py` is written."""

import pytest

from dsa.hashmap import ChainingHashMap, OpenAddressingHashMap

pytestmark = pytest.mark.challenge

MAPS = [ChainingHashMap, OpenAddressingHashMap]
ids = lambda c: c.__name__  # noqa: E731


@pytest.mark.parametrize("cls", MAPS, ids=ids)
def test_put_then_get(cls):
    m = cls()
    m.put("a", 1)
    assert m.get("a") == 1
    assert len(m) == 1


@pytest.mark.parametrize("cls", MAPS, ids=ids)
def test_put_overwrites_without_growing(cls):
    m = cls()
    m.put("a", 1)
    m.put("a", 2)
    assert m.get("a") == 2
    assert len(m) == 1


@pytest.mark.parametrize("cls", MAPS, ids=ids)
def test_get_missing_key(cls):
    m = cls()
    assert m.get("nope", "fallback") == "fallback"
    with pytest.raises(KeyError):
        m.get("nope")


@pytest.mark.parametrize("cls", MAPS, ids=ids)
def test_delete(cls):
    m = cls()
    m.put("a", 1)
    m.delete("a")
    assert len(m) == 0
    with pytest.raises(KeyError):
        m.get("a")


@pytest.mark.parametrize("cls", MAPS, ids=ids)
def test_delete_missing_key_raises(cls):
    with pytest.raises(KeyError):
        cls().delete("nope")


@pytest.mark.parametrize("cls", MAPS, ids=ids)
def test_survives_many_keys_and_resizes(cls):
    m = cls()
    for i in range(500):
        m.put(f"key{i}", i)
    assert len(m) == 500
    for i in range(500):
        assert m.get(f"key{i}") == i


@pytest.mark.parametrize("cls", MAPS, ids=ids)
def test_load_factor_stays_bounded(cls):
    """If the table never resizes, lookups degrade to a linear scan."""
    m = cls()
    for i in range(500):
        m.put(i, i)
    assert m.load_factor <= m.max_load + 0.05


@pytest.mark.parametrize("cls", MAPS, ids=ids)
def test_collisions_are_handled(cls):
    """Keys engineered to share a bucket must all remain retrievable."""
    m = cls()
    capacity = len(getattr(m, "_buckets", None) or m._keys)
    colliding = [i * capacity for i in range(1, 6)]
    for key in colliding:
        m.put(key, f"v{key}")
    for key in colliding:
        assert m.get(key) == f"v{key}"


def test_open_addressing_delete_preserves_probe_chain():
    """The subtle one: deleting a key must not orphan what probed past it.

    Insert two colliding keys, delete the first, and the second must still be
    findable. Blanking the slot instead of leaving a tombstone breaks this.
    """
    m = OpenAddressingHashMap(capacity=8)
    a, b = 0, 8            # both hash to slot 0
    m.put(a, "first")
    m.put(b, "second")
    m.delete(a)
    assert m.get(b) == "second"
