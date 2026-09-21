"""Measure how your implementations actually scale, and plot it.

Complexity is the topic students find most abstract, so the aim here is to let
them *see* their own code bend: implement linear search and binary search, run
both through `measure`, and plot the two curves on one axis.

    from viz.complexity import measure, plot_growth
    import random

    sizes = [1000, 2000, 4000, 8000, 16000]
    make = lambda n: (sorted(random.random() for _ in range(n)), 0.5)

    linear = measure(lambda a: my_linear_search(*a), sizes, make)
    binary = measure(lambda a: my_binary_search(*a), sizes, make)
    plot_growth({"linear search": linear, "binary search": binary},
                reference=["n", "log n"])
"""

from __future__ import annotations

import time

import matplotlib.pyplot as plt
import numpy as np

__all__ = ["measure", "plot_growth", "REFERENCES"]

#: Reference growth curves available to `plot_growth(reference=...)`.
REFERENCES = {
    "1": lambda n: np.ones_like(n, dtype=float),
    "log n": lambda n: np.log2(n),
    "n": lambda n: n.astype(float),
    "n log n": lambda n: n * np.log2(n),
    "n^2": lambda n: n.astype(float) ** 2,
    "n^3": lambda n: n.astype(float) ** 3,
    "2^n": lambda n: 2.0 ** n,
}


def measure(func, sizes, make_input, repeat=3, warmup=True):
    """Time `func` at each input size and return `(sizes, best_seconds)`.

    func:       callable taking exactly what `make_input(n)` returns
    sizes:      iterable of input sizes
    make_input: n -> the argument passed to func (built fresh, not timed)
    repeat:     runs per size; the *minimum* is kept, since noise only ever
                makes a run slower

    Input construction is excluded from the timing, so what you measure is the
    algorithm rather than the setup.
    """
    sizes = list(sizes)
    timings = []

    for n in sizes:
        if warmup:
            func(make_input(n))
        best = float("inf")
        for _ in range(repeat):
            payload = make_input(n)
            start = time.perf_counter()
            func(payload)
            best = min(best, time.perf_counter() - start)
        timings.append(best)

    return sizes, timings


def plot_growth(results, reference=(), title=None, loglog=False, ax=None):
    """Plot one or more `measure()` results, optionally against reference curves.

    results:   {"label": (sizes, seconds), ...}, or a single (sizes, seconds)
    reference: names from REFERENCES, e.g. ["n", "n log n"]. Each is scaled to
               meet the first measured series at its largest size, so the
               comparison is about *shape*, not absolute time.
    loglog:    log-log axes, where each polynomial complexity is a straight
               line whose slope is its exponent
    """
    if isinstance(results, tuple) and len(results) == 2:
        results = {"measured": results}

    if ax is None:
        _, ax = plt.subplots(figsize=(7.0, 4.5))

    for label, (sizes, timings) in results.items():
        ax.plot(sizes, timings, marker="o", linewidth=1.8, label=label)

    if reference:
        first_sizes, first_timings = next(iter(results.values()))
        anchor_n = np.array(first_sizes, dtype=float)
        anchor_t = first_timings[-1]
        for name in reference:
            if name not in REFERENCES:
                raise KeyError(f"unknown reference {name!r}; choose from {sorted(REFERENCES)}")
            curve = REFERENCES[name](anchor_n)
            if curve[-1] == 0:
                continue
            scaled = curve * (anchor_t / curve[-1])
            ax.plot(first_sizes, scaled, linestyle="--", linewidth=1.2, alpha=0.75,
                    label=f"O({name})")

    if loglog:
        ax.set_xscale("log")
        ax.set_yscale("log")

    ax.set_xlabel("input size n")
    ax.set_ylabel("seconds (best of repeats)")
    ax.set_title(title or "Measured growth", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend()
    return ax
