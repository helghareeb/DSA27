"""Generate the figures for Lecture 13 — Hash tables.

Run it from the repository root:

    python tools/figures_l13.py                         # uses YOUR dsa/hashmap.py
    python tools/with_solutions.py tools/figures_l13.py # uses solutions/

Same conventions as `tools/figures.py`. Every table drawn here is built by
running a working `dsa/hashmap.py` and reading its slots back, so the pictures
are real states, not drawings of what the state should be. The keys are all
**integers**: `hash(n)` is `n` for every int you will meet in this course, in
every run, on every machine, so the pictures are reproducible. (A `str` key
would land in a different slot every run — Lecture 13, "Same run, same hash".)

Run without a working implementation and only the figures that need none
(the pipeline and the birthday curve) are drawn.
"""

from __future__ import annotations

import math
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import figures as base  # palette, rcParams, save()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "13-hash-tables" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
GREY = "#D6D6D6"
PURPLE = "#7A5195"
PINK = "#F6C9C4"


def box(ax, x, y, text, fill=FILL, w=1.0, h=0.6, fontsize=11, colour=SLATE):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=SLATE, linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=colour)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.4):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text):
    ax.set_title(text, fontsize=12.5, fontweight="bold", color=SLATE, pad=6)


def implemented():
    from dsa.hashmap import ChainingHashMap, OpenAddressingHashMap
    try:
        ChainingHashMap().put(1, 1)
        OpenAddressingHashMap().put(1, 1)
    except NotImplementedError:
        return False
    return True


def chains_of(m):
    """The keys of each bucket of a ChainingHashMap, front of the chain first."""
    result = []
    for head in m._buckets:
        keys, entry = [], head
        while entry is not None:
            keys.append(entry.key)
            entry = entry.next
        result.append(keys)
    return result


def slots_of(m):
    """The key slots of an OpenAddressingHashMap: a key, None, or 'T'."""
    from dsa.hashmap import TOMBSTONE
    return ["T" if k is TOMBSTONE else k for k in m._keys]


# -- the idea -----------------------------------------------------------------


def figure_pipeline():
    """key -> hash(key) -> % capacity -> slot, for three integer keys."""
    keys = [2027305, 2027114, 2026988]
    capacity = 8
    fig, ax = plt.subplots(figsize=(10.4, 3.9))
    ys = [2.4, 1.4, 0.4]
    for key, y in zip(keys, ys):
        h = hash(key)
        i = h % capacity
        box(ax, 0, y, str(key), fill="white", w=1.9, h=0.6, fontsize=10.5)
        arrow(ax, (1.95, y + 0.3), (2.75, y + 0.3), colour=MUTED)
        box(ax, 2.8, y, f"hash = {h}", fill=FILL, w=2.6, h=0.6, fontsize=10)
        arrow(ax, (5.45, y + 0.3), (6.25, y + 0.3), colour=MUTED)
        box(ax, 6.3, y, f"% 8 = {i}", fill=HILITE, w=1.5, h=0.6, fontsize=10.5)
        arrow(ax, (7.85, y + 0.3), (9.3 + i * 0.6 + 0.3, 3.35), colour=AMBER, rad=0.12)
    ax.text(0.95, 3.25, "key", ha="center", fontsize=10, color=MUTED)
    ax.text(4.1, 3.25, "hash(key)", ha="center", fontsize=10, color=MUTED)
    ax.text(7.05, 3.25, "index", ha="center", fontsize=10, color=MUTED)
    for s in range(capacity):
        box(ax, 9.3 + s * 0.6, 3.4, "", fill="white", w=0.6, h=0.6)
        ax.text(9.3 + s * 0.6 + 0.3, 4.15, str(s), ha="center", fontsize=8, color=MUTED)
    ax.text(9.3 + 2.4, 4.45, "the Array: 8 slots", ha="center", fontsize=10, color=SLATE)
    clean(ax, (-0.2, 14.3), (0.2, 4.8))
    title(ax, "Hashing turns any key into an index: hash(key) % capacity")
    return base.save(fig, "pipeline")


def figure_birthday():
    """Exact probability of at least one collision, with a simulation on top."""
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    rng = random.Random(13)
    for m, colour in [(365, AMBER), (10_000, SLATE)]:
        xs = list(range(0, 301)) if m > 365 else list(range(0, 81))
        ps = []
        for n in xs:
            p_none = 1.0
            for k in range(n):
                p_none *= (m - k) / m
            ps.append(1 - p_none)
        half = next(n for n, p in zip(xs, ps) if p >= 0.5)
        ax.plot(xs, ps, color=colour, linewidth=2.1,
                label=f"m = {m:,} slots: 50% at n = {half}")
        ax.plot([half], [0.5], "o", color=colour, markersize=6)
        # simulation: 400 trials at a few n, to show the formula is not a trick
        sims = xs[::max(1, len(xs) // 12)]
        freq = []
        for n in sims:
            hits = 0
            for _ in range(400):
                seen = set()
                for _ in range(n):
                    s = rng.randrange(m)
                    if s in seen:
                        hits += 1
                        break
                    seen.add(s)
            freq.append(hits / 400)
        ax.plot(sims, freq, "x", color=colour, markersize=6, alpha=0.8)
    ax.axhline(0.5, color=MUTED, linewidth=0.8, linestyle=":")
    ax.set_xlabel("n, keys placed at random")
    ax.set_ylabel("P(at least one collision)")
    ax.set_ylim(0, 1.02)
    ax.grid(True, alpha=0.25, linewidth=0.7)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, fontsize=9.5, loc="lower right",
              title="line: exact formula · ×: 400 random trials", title_fontsize=8.5)
    title(ax, "The birthday paradox: collisions come long before the table is full")
    fig.tight_layout()
    return base.save(fig, "birthday")


# -- the two tables -----------------------------------------------------------


def figure_chaining():
    from dsa.hashmap import ChainingHashMap
    m = ChainingHashMap()
    for k in [10, 22, 31, 4, 15, 28]:
        m.put(k, str(k))
    chains = chains_of(m)
    fig, ax = plt.subplots(figsize=(9.8, 4.4))
    for i, keys in enumerate(chains):
        x = i * 1.2
        box(ax, x, 3.0, "" if keys else "None", fill=FILL if keys else "white",
            w=1.0, h=0.6, fontsize=8, colour=MUTED)
        ax.text(x + 0.5, 3.75, str(i), ha="center", fontsize=9, color=MUTED)
        y = 3.0
        for j, key in enumerate(keys):
            ny = 1.9 - j * 1.1
            arrow(ax, (x + 0.5, y + 0.05 if j else y + 0.3), (x + 0.5, ny + 0.62),
                  colour=SLATE)
            fill = HILITE if len(keys) > 1 else DONE
            box(ax, x, ny, f"{key}: '{key}'", fill=fill, w=1.0, h=0.6, fontsize=8.5)
            y = ny
    ax.text(10.0, 2.2, "put 10, 22, 31, 4, 15, 28\ninto 8 buckets:\n\n"
            "15 and 31 share bucket 7\n28 and 4 share bucket 4\n\n"
            "a new key goes on the\nFRONT of its chain", va="center",
            fontsize=9.5, color=SLATE)
    clean(ax, (-0.3, 13.2), (0.5, 4.1))
    title(ax, "Chaining: each bucket holds a linked list of Entry nodes")
    return base.save(fig, "chaining")


def figure_probing():
    from dsa.hashmap import OpenAddressingHashMap
    m = OpenAddressingHashMap()
    for k in [10, 22, 31, 4, 15]:
        m.put(k, str(k))
    slots = slots_of(m)
    fig, ax = plt.subplots(figsize=(9.8, 3.0))
    for i, key in enumerate(slots):
        fill = "white" if key is None else (HILITE if key == 15 else FILL)
        box(ax, i * 1.1, 0, "" if key is None else str(key), fill=fill, w=1.0, h=0.7,
            fontsize=12)
        ax.text(i * 1.1 + 0.5, -0.25, str(i), ha="center", fontsize=9, color=MUTED)
    # 15 hashes to 7, finds it taken by 31, wraps to 0
    arrow(ax, (7 * 1.1 + 0.5, 0.75), (7 * 1.1 + 0.5, 1.45), colour=RED)
    ax.text(7 * 1.1 + 0.5, 1.55, "15 % 8 = 7:\ntaken by 31", ha="center", fontsize=9,
            color=RED)
    arrow(ax, (7 * 1.1 + 0.2, 0.72), (0.5, 0.72), colour=AMBER, rad=0.18, lw=1.6)
    ax.text(3.9, 2.25, "probe 7, then (7 + 1) % 8 = 0: free — 15 goes there",
            ha="center", fontsize=9.5, color=AMBER)
    clean(ax, (-0.3, 9.1), (-0.5, 2.6))
    title(ax, "Open addressing, linear probing: one key per slot, step on when taken")
    return base.save(fig, "probing")


def figure_tombstone():
    from dsa.hashmap import OpenAddressingHashMap
    m = OpenAddressingHashMap()
    for k in [3, 11, 19]:
        m.put(k, str(k))
    before = slots_of(m)
    m.delete(11)
    after = slots_of(m)
    assert m.get(19) == "19"
    wrong = list(before)
    wrong[4] = None
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 5.6))
    panels = [
        (before, "3, 11 and 19 all hash to 3: they sit in slots 3, 4, 5", None, None),
        (wrong, "delete 11 by EMPTYING slot 4 — then get(19) probes 3, 4: None, "
                "'not here'. Wrong.", RED, 4),
        (after, "delete 11 with a TOMBSTONE — get(19) probes 3, 4 (skip), 5: found.",
         GREEN, 5),
    ]
    for ax, (slots, text, colour, stop) in zip(axes, panels):
        for i, key in enumerate(slots):
            if key == "T":
                fill, label = GREY, "†"
            elif key is None:
                fill, label = "white", ""
            else:
                fill, label = FILL, str(key)
            if stop is not None and i == stop:
                fill = PINK if colour == RED else DONE
            box(ax, i * 1.1, 0, label, fill=fill, w=1.0, h=0.7, fontsize=12)
            ax.text(i * 1.1 + 0.5, -0.22, str(i), ha="center", fontsize=8, color=MUTED)
        if stop is not None:
            for a, b in zip(range(3, stop), range(4, stop + 1)):
                arrow(ax, (a * 1.1 + 0.6, 0.85), (b * 1.1 + 0.4, 0.85), colour=colour,
                      rad=-0.5)
        ax.text(0, 1.25, text, fontsize=9.8, color=colour or SLATE)
        clean(ax, (-0.3, 9.1), (-0.45, 1.6))
    axes[0].set_title("Why delete cannot just empty a slot", fontsize=12.5,
                      fontweight="bold", color=SLATE, pad=6)
    fig.tight_layout()
    return base.save(fig, "tombstone")


def figure_clustering():
    """A real 64-slot linear-probing table at load 0.625, runs coloured."""
    from dsa.hashmap import OpenAddressingHashMap
    rng = random.Random(1300)
    m = OpenAddressingHashMap(capacity=64, max_load=0.99)
    for k in rng.sample(range(10**6), 40):
        m.put(k, k)
    slots = slots_of(m)
    runs, start = [], None
    for i, k in enumerate(slots + [None]):
        if k is not None and start is None:
            start = i
        if k is None and start is not None:
            runs.append((start, i - start))
            start = None
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][0] + runs[-1][1] == 64:
        last = runs.pop()                    # the table is a ring: a run that
        runs[0] = (last[0], last[1] + runs[0][1])   # ends at 63 goes on at 0
    longest = max(r[1] for r in runs)
    fig, ax = plt.subplots(figsize=(11.2, 2.3))
    w = 0.17
    for i, k in enumerate(slots):
        fill = "white"
        for s, length in runs:
            if s <= i < s + length or s <= i + 64 < s + length:
                fill = PINK if length == longest else (HILITE if length >= 4 else FILL)
        ax.add_patch(Rectangle((i * w, 0), w, 0.5, facecolor=fill, edgecolor=MUTED,
                               linewidth=0.6))
    s, length = next(r for r in runs if r[1] == longest)
    ax.text((s + length / 2) * w, 0.7, f"a run of {length}", ha="center", fontsize=9.5,
            color=RED)
    lengths = sorted((r[1] for r in runs), reverse=True)
    ax.text(0, -0.35, f"40 random keys in 64 slots (load 0.625): {len(runs)} runs; "
            f"the longest are {', '.join(map(str, lengths[:4]))}. A key that hashes "
            "anywhere into a run lands at its end — and makes it longer.",
            fontsize=9, color=SLATE, va="top")
    ax.set_xlim(-0.1, 64 * w + 0.1)
    ax.set_ylim(-0.75, 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    title(ax, "Primary clustering: occupied slots clump into runs")
    print(f"    runs: {lengths}")
    return base.save(fig, "clustering")


# -- measured -----------------------------------------------------------------


def figure_resize():
    """Load factor after each put, and the total rehash work per key."""
    from dsa.hashmap import ChainingHashMap, OpenAddressingHashMap

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.3))
    n = 3000
    rng = random.Random(4)
    keys = rng.sample(range(10**9), n)
    for cls, colour in [(ChainingHashMap, SLATE), (OpenAddressingHashMap, AMBER)]:
        moved = [0]
        original = cls._resize

        def counting(self, capacity, original=original, moved=moved):
            moved[0] += len(self)
            return original(self, capacity)

        cls._resize = counting
        try:
            m = cls()
            loads, per_key = [], []
            for i, k in enumerate(keys, 1):
                m.put(k, i)
                loads.append(m.load_factor)
                per_key.append(moved[0] / i)
        finally:
            cls._resize = original
        label = f"{cls.__name__} (max_load {m.max_load})"
        axes[0].plot(range(1, n + 1), loads, color=colour, linewidth=1.3, label=label)
        axes[1].plot(range(1, n + 1), per_key, color=colour, linewidth=1.6, label=label)
        print(f"    {cls.__name__}: {moved[0]} rehash moves for {n} puts; "
              f"final capacity {int(round(len(m) / m.load_factor))}")
    axes[0].set_xlabel("keys inserted")
    axes[0].set_ylabel("load factor = size / capacity")
    axes[0].set_title("the load factor saw-tooths: each resize halves it",
                      fontsize=11, color=SLATE)
    axes[0].set_ylim(0, 1)
    axes[1].set_xlabel("keys inserted")
    axes[1].set_ylabel("keys rehashed so far ÷ keys inserted")
    axes[1].set_title("rehashing costs at most 2 moves per key: amortised O(1)",
                      fontsize=11, color=SLATE)
    axes[1].set_ylim(0, 2.2)
    for ax in axes:
        ax.set_xscale("log")
        ax.grid(True, alpha=0.25, linewidth=0.7)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    axes[0].legend(frameon=False, fontsize=8.5, loc="upper left")
    axes[1].legend(frameon=False, fontsize=8.5, loc="lower right")
    fig.suptitle("Measured: doubling keeps the table short, and pays for itself",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "resize")


def figure_probes():
    """Average probes per lookup against load factor, measured and predicted."""
    from dsa.hashmap import ChainingHashMap, OpenAddressingHashMap

    class Counting(OpenAddressingHashMap):
        probes = 0

        def _probe(self, key):
            for i in super()._probe(key):
                Counting.probes += 1
                yield i

    capacity = 1 << 14
    rng = random.Random(13)
    alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95]
    universe = rng.sample(range(10**9), capacity + 2000)
    present_all, absent = universe[:capacity], universe[capacity:]
    series = {k: [] for k in ("lp_hit", "lp_miss", "ch_hit", "ch_miss")}
    for a in alphas:
        n = int(a * capacity)
        present = present_all[:n]
        oa = Counting(capacity=capacity, max_load=0.99)
        ch = ChainingHashMap(capacity=capacity, max_load=1.0)
        for k in present:
            oa.put(k, k)
            ch.put(k, k)
        sample = present[:: max(1, n // 2000)]
        Counting.probes = 0
        for k in sample:
            oa.get(k)
        series["lp_hit"].append(Counting.probes / len(sample))
        Counting.probes = 0
        for k in absent:
            oa.get(k, None)
        series["lp_miss"].append(Counting.probes / len(absent))
        # chaining: compare against every entry walked
        chains = chains_of(ch)
        where = {}
        for keys in chains:
            for pos, k in enumerate(keys):
                where[k] = pos + 1
        series["ch_hit"].append(sum(where[k] for k in sample) / len(sample))
        series["ch_miss"].append(
            sum(len(chains[k % capacity]) for k in absent) / len(absent))
    fine = [i / 100 for i in range(5, 96)]
    fig, ax = plt.subplots(figsize=(9.8, 4.9))
    theory = {
        "lp_hit": [0.5 * (1 + 1 / (1 - a)) for a in fine],
        "lp_miss": [0.5 * (1 + 1 / (1 - a) ** 2) for a in fine],
        "ch_hit": [1 + a / 2 for a in fine],
        "ch_miss": [a for a in fine],
    }
    for key, label, colour, marker in [
        ("lp_miss", "linear probing, key absent", RED, "s"),
        ("lp_hit", "linear probing, key present", AMBER, "o"),
        ("ch_hit", "chaining, key present", GREEN, "o"),
        ("ch_miss", "chaining, key absent", SLATE, "s"),
    ]:
        ax.plot(fine, theory[key], color=colour, linewidth=1.2, alpha=0.7, linestyle="--")
        ax.plot(alphas, series[key], marker, color=colour, label=label, markersize=6)
    ax.set_yscale("log")
    ax.set_ylim(0.08, 300)
    ax.set_xlabel("load factor α = n / capacity")
    ax.set_ylabel("slots or entries examined per lookup (log scale)")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, fontsize=9, loc="upper left",
              title="markers: measured (16,384 slots) · dashed: Knuth's formulas",
              title_fontsize=8.5)
    ax.axvline(0.66, color=MUTED, linewidth=0.8, linestyle=":")
    ax.axvline(0.75, color=MUTED, linewidth=0.8, linestyle=":")
    ax.text(0.655, 150, "0.66", ha="right", fontsize=8, color=MUTED)
    ax.text(0.755, 150, "0.75", ha="left", fontsize=8, color=MUTED)
    title(ax, "Measured: lookups stay cheap until the table is nearly full")
    fig.tight_layout()
    for key in series:
        print(f"    {key:8s}", [round(v, 2) for v in series[key]])
    return base.save(fig, "probes")


def figure_adversarial():
    """Time per get, ordinary keys against keys that all share a bucket."""
    from dsa.hashmap import ChainingHashMap, OpenAddressingHashMap

    sizes = [250, 500, 1000, 2000, 4000]
    rng = random.Random(7)
    results = {}

    def timed(cls, keys):
        if cls is dict:
            m = {}
            for k in keys:
                m[k] = k
            lookup = m.__getitem__
        else:
            m = cls()
            for k in keys:
                m.put(k, k)
            lookup = m.get
        sample = keys[:: max(1, len(keys) // 200)]
        best = float("inf")
        for _ in range(3):
            start = time.perf_counter()
            for k in sample:
                lookup(k)
            best = min(best, time.perf_counter() - start)
        return best / len(sample)

    cases = [
        ("ChainingHashMap, bad keys i × 2²⁰", ChainingHashMap, True, RED, "o-"),
        ("OpenAddressingHashMap, bad keys", OpenAddressingHashMap, True, PURPLE, "s-"),
        ("ChainingHashMap, random keys", ChainingHashMap, False, GREEN, "o-"),
        ("OpenAddressingHashMap, random keys", OpenAddressingHashMap, False, AMBER, "s-"),
        ("Python dict, bad keys", dict, True, SLATE, "^-"),
    ]
    fig, ax = plt.subplots(figsize=(9.8, 4.8))
    for label, cls, bad, colour, style in cases:
        ys = []
        for n in sizes:
            keys = [i << 20 for i in range(n)] if bad else rng.sample(range(10**9), n)
            ys.append(timed(cls, keys) * 1e6)
        results[label] = ys
        ax.plot(sizes, ys, style, color=colour, label=label, linewidth=2.0, markersize=5)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("n, keys in the table (log scale)")
    ax.set_ylabel("microseconds per get (log scale)")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, fontsize=8.8, loc="upper left")
    ax.set_ylim(0.02, 3e4)
    title(ax, "Measured: O(1) average is a promise about the keys")
    fig.tight_layout()
    for key, ys in results.items():
        print(f"    {key:38s}", [round(v, 2) for v in ys])
    return base.save(fig, "adversarial")


DIAGRAMS = [figure_pipeline, figure_birthday]
NEEDS_CODE = [figure_chaining, figure_probing, figure_tombstone, figure_clustering,
              figure_resize, figure_probes, figure_adversarial]


def main():
    print(f"Generating figures into {base.OUT.relative_to(ROOT)}")
    for builder in DIAGRAMS:
        builder()
    if not implemented():
        print("  (skipped the rest: dsa/hashmap.py is not implemented yet)")
        return
    for builder in NEEDS_CODE:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
