"""Generate every figure used in the course documents.

Run it from the repository root:

    python tools/figures.py

Figures are written as **PNG at 300 DPI**. SVG renders on GitHub but not in
XeLaTeX; PDF renders in XeLaTeX but not on GitHub. PNG is the only format both
consumers read, so the Markdown needs one path and one file.

Nothing here is borrowed. Every figure is drawn from the course's own tooling,
which means they are reproducible, they match the palette in `viz/style.py`,
and there is no licence to worry about.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = ROOT / "docs" / "lectures" / "01-why-this-course" / "figures"

SLATE = "#233A3E"
AMBER = "#C8860D"
PAPER = "#FAFAF8"
MUTED = "#5B6B6E"
FILL = "#E8EEF7"
HILITE = "#FFE3B0"
DONE = "#D8EFD8"
FONT = "DejaVu Sans"

plt.rcParams.update({
    "font.family": FONT,
    "font.size": 11,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": SLATE,
    "text.color": SLATE,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.png"
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print(f"  {path.relative_to(ROOT)}")


def save_dot(dot, name):
    """Render a graphviz object to PNG and drop the intermediate .gv file."""
    OUT.mkdir(parents=True, exist_ok=True)
    dot.attr(dpi="200", bgcolor="white")
    dot.render(str(OUT / name), format="png", cleanup=True)
    print(f"  {(OUT / (name + '.png')).relative_to(ROOT)}")


# -- Part 1: the languages ------------------------------------------------

LANGUAGES = [
    (1972, "C", "Dennis Ritchie", "a portable assembler"),
    (1985, "C++", "Bjarne Stroustrup", "no room for a lower level"),
    (1991, "Python", "Guido van Rossum", "readability is worth paying for"),
    (1995, "Java", "James Gosling", "write once, run anywhere"),
    (1995, "JavaScript", "Brendan Eich", "ten days, and it stayed"),
    (2009, "Go", "Pike, Thompson, Griesemer", "fewer features, faster builds"),
    (2015, "Rust", "Graydon Hoare", "safety without a collector"),
]


def figure_timeline():
    """One lane per language, so nothing can collide however close the years."""
    fig, ax = plt.subplots(figsize=(11, 5.0))
    rows = len(LANGUAGES)

    for index, (year, name, who, idea) in enumerate(LANGUAGES):
        y = rows - index
        ax.plot([1968, 2022], [y, y], color="#ECECEA", linewidth=1, zorder=0)
        ax.scatter([year], [y], s=90, color=AMBER, zorder=3,
                   edgecolor="white", linewidth=1.4)
        # Labels sit to the right, and flip left for the late languages so
        # they never run off the axis.
        right = year < 2005
        ax.annotate(f"  {name} ({year})  ", (year, y),
                    ha="left" if right else "right", va="center",
                    fontsize=11.5, fontweight="bold", color=SLATE,
                    xytext=(10 if right else -10, 7), textcoords="offset points")
        ax.annotate(f"  {who} — {idea}  ", (year, y),
                    ha="left" if right else "right", va="center",
                    fontsize=9, color=MUTED, style="italic",
                    xytext=(10 if right else -10, -8), textcoords="offset points")

    ax.set_xlim(1968, 2022)
    ax.set_ylim(0.4, rows + 0.8)
    ax.set_yticks([])
    ax.set_xticks([1970, 1980, 1990, 2000, 2010, 2020])
    ax.tick_params(axis="x", labelsize=10)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#D8DCDA")
    ax.set_title("Every language is a decision, and every decision has an author",
                 fontsize=13, fontweight="bold", color=SLATE, pad=16)
    return save(fig, "pl-timeline")


PARADIGMS = ["Procedural", "Object-oriented", "Functional", "Declarative"]
PARADIGM_SUPPORT = {
    "C":          [1, 0, 0, 0],
    "C++":        [1, 1, 0.5, 0],
    "Java":       [1, 1, 0.5, 0],
    "Python":     [1, 1, 0.5, 0.5],
    "JavaScript": [1, 0.5, 0.5, 0],
    "Rust":       [1, 0.5, 0.5, 0],
    "Haskell":    [0, 0, 1, 0.5],
    "SQL":        [0, 0, 0, 1],
    "Prolog":     [0, 0, 0, 1],
}


def figure_paradigms():
    names = list(PARADIGM_SUPPORT)
    fig, ax = plt.subplots(figsize=(9, 5.4))

    for row, name in enumerate(names):
        for col, level in enumerate(PARADIGM_SUPPORT[name]):
            colour = {0: "#F0F0EE", 0.5: HILITE, 1: DONE}[level]
            ax.add_patch(FancyBboxPatch(
                (col, len(names) - row - 1), 0.92, 0.88,
                boxstyle="round,pad=0.02,rounding_size=0.06",
                facecolor=colour, edgecolor=MUTED, linewidth=0.8))
            if level:
                ax.text(col + 0.46, len(names) - row - 1 + 0.44,
                        "core" if level == 1 else "supported",
                        ha="center", va="center", fontsize=8, color=SLATE)

    ax.set_xlim(-0.05, len(PARADIGMS))
    ax.set_ylim(-0.05, len(names))
    ax.set_xticks([i + 0.46 for i in range(len(PARADIGMS))])
    ax.set_xticklabels(PARADIGMS, fontsize=10.5, color=SLATE)
    ax.set_yticks([len(names) - i - 0.56 for i in range(len(names))])
    ax.set_yticklabels(names, fontsize=10.5, color=SLATE)
    ax.xaxis.tick_top()
    for side in ("left", "right", "top", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Most languages are multi-paradigm — so the choice of style is yours",
                 fontsize=12, fontweight="bold", color=SLATE, pad=34)
    return save(fig, "paradigms")


TYPED = [
    ("Java", 1, 1), ("C#", 1, 1), ("Rust", 1, 1), ("Haskell", 1, 1),
    ("Python", -1, 1), ("Ruby", -1, 1),
    ("C", 1, -1), ("C++", 1, -1),
    ("JavaScript", -1, -1), ("PHP", -1, -1),
]


def figure_type_systems():
    fig, ax = plt.subplots(figsize=(9.2, 6.2))
    ax.axhline(0, color=MUTED, linewidth=1.2, zorder=1)
    ax.axvline(0, color=MUTED, linewidth=1.2, zorder=1)

    # Stack each quadrant's languages downwards from its own centre, so the
    # boxes never land on the axis labels.
    for quadrant in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        members = [name for name, x, y in TYPED if (x, y) == quadrant]
        x_sign, y_sign = quadrant
        top = 2.15 if y_sign > 0 else -0.62
        for step, name in enumerate(members):
            ax.text(x_sign * 0.85, top - step * 0.42, name,
                    ha="center", va="center", fontsize=11.5, color=SLATE, zorder=4,
                    fontweight="bold" if name == "Python" else "normal",
                    bbox=dict(boxstyle="round,pad=0.36",
                              facecolor=HILITE if name == "Python" else FILL,
                              edgecolor=MUTED, linewidth=0.9))

    ax.text(0, 2.72, "STRONG — refuses to guess", ha="center", fontsize=11.5,
            fontweight="bold", color=SLATE)
    ax.text(0, -2.30, "WEAK — converts silently", ha="center", fontsize=11.5,
            fontweight="bold", color=SLATE)
    ax.text(-2.45, 0.16, "DYNAMIC\nchecked at run time", ha="center", va="bottom",
            fontsize=10.5, fontweight="bold", color=SLATE)
    ax.text(2.45, 0.16, "STATIC\nchecked at compile time", ha="center", va="bottom",
            fontsize=10.5, fontweight="bold", color=SLATE)

    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-2.7, 3.1)
    ax.axis("off")
    ax.set_title("Two independent axes, not one",
                 fontsize=13, fontweight="bold", color=SLATE, pad=16)
    return save(fig, "type-systems")


def figure_memory():
    fig, ax = plt.subplots(figsize=(10, 3.9))
    models = [
        ("Manual", "C, C++", "you allocate,\nyou free", "fastest\nand most dangerous", FILL),
        ("Garbage collected", "Python, Java, Go", "the runtime frees\nwhat you cannot reach",
         "safe, at the cost of\ncontrol and pauses", DONE),
        ("Ownership", "Rust", "the compiler proves it\nis freed exactly once",
         "safe and fast, at the cost\nof a harder compiler", HILITE),
    ]
    for index, (name, langs, how, cost, colour) in enumerate(models):
        ax.add_patch(FancyBboxPatch(
            (index * 3.4, 0), 3.0, 2.5,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            facecolor=colour, edgecolor=MUTED, linewidth=1.1))
        ax.text(index * 3.4 + 1.5, 2.16, name, ha="center", fontsize=12,
                fontweight="bold", color=SLATE)
        ax.text(index * 3.4 + 1.5, 1.84, langs, ha="center", fontsize=9.5, color=MUTED)
        ax.text(index * 3.4 + 1.5, 1.28, how, ha="center", fontsize=10, color=SLATE)
        ax.text(index * 3.4 + 1.5, 0.45, cost, ha="center", fontsize=9,
                color=MUTED, style="italic")

    ax.annotate("", xy=(10.2, -0.42), xytext=(0, -0.42),
                arrowprops=dict(arrowstyle="->", color=AMBER, linewidth=1.6))
    ax.text(0, -0.72, "more control", fontsize=9.5, color=MUTED)
    ax.text(10.2, -0.72, "more safety", fontsize=9.5, color=MUTED, ha="right")

    ax.set_xlim(-0.3, 10.5)
    ax.set_ylim(-1.1, 2.8)
    ax.axis("off")
    ax.set_title("Who cleans up the memory?", fontsize=13,
                 fontweight="bold", color=SLATE, pad=12)
    return save(fig, "memory-models")


# -- Part 4: from a variable to a structure -------------------------------


def figure_ladder():
    from graphviz import Digraph

    dot = Digraph(graph_attr={"rankdir": "LR", "nodesep": "0.5"})
    dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica",
             fontsize="11", color=MUTED, penwidth="1.1")
    dot.attr("edge", color=AMBER, penwidth="1.4", arrowsize="0.8")

    steps = [
        ("v", "variable\ni = 42", FILL),
        ("o", "object\nthe 42 in memory", FILL),
        ("c", "class\nint, str, your own", FILL),
        ("k", "collection\n[42, \"hello\", 3.14]", HILITE),
        ("d", "data structure\nyou build this", DONE),
    ]
    for name, label, colour in steps:
        dot.node(name, label, fillcolor=colour)
    for (a, *_), (b, *_) in zip(steps, steps[1:]):
        dot.edge(a, b)
    return save_dot(dot, "variable-to-structure")


def figure_adt():
    from graphviz import Digraph

    dot = Digraph(graph_attr={"rankdir": "TB", "nodesep": "0.7", "ranksep": "0.6"})
    dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica",
             fontsize="11", color=MUTED, penwidth="1.1")
    dot.attr("edge", color=AMBER, penwidth="1.4", arrowsize="0.8")

    dot.node("adt", "Stack  (the ADT)\n\npush  -  add to the top\npop   -  remove the top\npeek  -  look at the top\nall O(1)", fillcolor=HILITE)
    dot.node("arr", "on a dynamic array\n\ncontiguous, cache-friendly\none push in n is slow (resize)", fillcolor=FILL)
    dot.node("lst", "on a linked list\n\nevery push is O(1), always\na pointer per element", fillcolor=FILL)
    dot.edge("adt", "arr", label="  implemented by", fontsize="9", fontcolor=MUTED)
    dot.edge("adt", "lst", label="  or by", fontsize="9", fontcolor=MUTED)
    return save_dot(dot, "adt-vs-structure")


# -- Part 5: cost ---------------------------------------------------------


def figure_growth():
    import numpy as np

    from viz.complexity import REFERENCES

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    sizes = np.arange(1, 65)          # REFERENCES curves are numpy-vectorised
    order = ["1", "log n", "n", "n log n", "n^2", "2^n"]
    colours = ["#7FB069", "#4C9F70", AMBER, "#D96C3F", "#C1443C", SLATE]

    for name, colour in zip(order, colours):
        ax.plot(sizes, REFERENCES[name](sizes), label=f"O({name})",
                color=colour, linewidth=2.1)

    ax.set_xlim(1, 64)
    ax.set_ylim(0.5, 1000)
    ax.set_yscale("log")
    ax.set_xlabel("input size  n")
    ax.set_ylabel("operations (log scale)")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("The gap is not small — note the logarithmic axis",
                 fontsize=13, fontweight="bold", color=SLATE, pad=12)
    return save(fig, "growth-curves")


def figure_search_crossover():
    """Real timings, from the course's own `viz.complexity.measure`.

    The two searches below are reference implementations so the figure can be
    generated before anyone has written `dsa/searching.py`. Swap in your own
    and re-run this script to compare.
    """
    import random

    from viz.complexity import measure

    def linear_search(values, target):
        for index, value in enumerate(values):
            if value == target:
                return index
        return -1

    def binary_search(values, target):
        low, high = 0, len(values) - 1
        while low <= high:
            mid = (low + high) // 2
            if values[mid] == target:
                return mid
            if values[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    sizes = [500, 1000, 2000, 4000, 8000, 16000, 32000]
    rng = random.Random(0)

    def make(n):
        return (sorted(rng.random() for _ in range(n)), 2.0)   # always a miss

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    for name, func, colour in [("linear search", linear_search, "#C1443C"),
                               ("binary search", binary_search, AMBER)]:
        measured_sizes, seconds = measure(lambda a, f=func: f(*a), sizes, make)
        ax.plot(measured_sizes, [s * 1e6 for s in seconds], "o-",
                label=name, color=colour, linewidth=2.1, markersize=5)

    ax.set_xlabel("input size  n")
    ax.set_ylabel("microseconds (log scale)")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.25, linewidth=0.7)
    ax.legend(frameon=False, fontsize=10)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("Measured, not asserted — the same machine, the same data",
                 fontsize=13, fontweight="bold", color=SLATE, pad=12)
    return save(fig, "search-crossover")


def figure_ast():
    from viz.draw import draw_tree

    dot = draw_tree([
        ("+#1", "3#2"),
        ("+#1", "*#3"),
        ("*#3", "4#4"),
        ("*#3", "2#5"),
    ], highlight={"*#3"})
    dot.attr(label="3 + 4 * 2   —   '*' binds tighter, so it sits deeper",
             labelloc="b", fontsize="11", fontname="Helvetica")
    return save_dot(dot, "ast-example")


# -- Part 6: the course ---------------------------------------------------

WEEKS = [
    (1, "Why this course"), (2, "Complexity & the Array"), (3, "Recursion"),
    (4, "Dynamic arrays"), (5, "Linked lists"), (6, "Stacks"),
    (7, "Queues"), (8, "Searching"), (9, "Basic sorting"),
    (10, "Advanced sorting"), (11, "Trees"), (12, "Heaps"),
    (13, "Hash tables"), (14, "Graphs"), (15, "Language translation"),
]
DEPENDS = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9),
           (9, 10), (3, 11), (11, 12), (10, 12), (7, 13), (11, 14), (6, 15),
           (11, 15), (3, 15)]


def figure_course_map():
    from graphviz import Digraph

    dot = Digraph(graph_attr={"rankdir": "LR", "nodesep": "0.22", "ranksep": "0.55"})
    dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica",
             fontsize="10", color=MUTED, penwidth="1.0")
    dot.attr("edge", color=MUTED, penwidth="1.0", arrowsize="0.6")

    new = {3, 11, 12, 14, 15}
    for number, name in WEEKS:
        dot.node(f"w{number}", f"{number}. {name}",
                 fillcolor=HILITE if number in new else FILL)
    for source, target in DEPENDS:
        dot.edge(f"w{source}", f"w{target}")
    return save_dot(dot, "course-map")


FIGURES = [
    figure_timeline, figure_paradigms, figure_type_systems, figure_memory,
    figure_ladder, figure_adt, figure_growth, figure_search_crossover,
    figure_ast, figure_course_map,
]


def main():
    print(f"Generating {len(FIGURES)} figures into {OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        builder()
    print("Done.")


if __name__ == "__main__":
    main()
