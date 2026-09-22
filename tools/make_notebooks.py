"""Scaffold one notebook per teaching week, into `notebooks/`.

Run from the repository root:

    python tools/make_notebooks.py

Every notebook gets the same shape as `notebooks/00-environment-check.ipynb`:
a `sys.path` bootstrap, the week's objective, an import cell, a place to try
things, and a `viz/` demo wired to that week's structure.

**Existing notebooks are never overwritten.** Once you have put real content in
one, re-running this script leaves it alone. Delete a file first if you want it
regenerated.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "notebooks"

# week number, slug, title, module, objective, demo cell
WEEKS = [
    (1, "why-this-course", "Why this course, and why Python", None,
     "Meet the tools. Nothing to implement yet — read Lecture 01 alongside this.",
     'from viz.draw import draw_array\n\n'
     'draw_array([42, "hello", 3.14], title="A list holds references, not values")'),

    (2, "complexity", "Complexity — measure, do not assert", None,
     "Say what an algorithm costs, then check yourself against a clock.",
     'from viz.complexity import measure, plot_growth\nimport random\n\n'
     'def linear_search(values, target):\n'
     '    for index, value in enumerate(values):\n'
     '        if value == target:\n'
     '            return index\n'
     '    return -1\n\n'
     'sizes = [1000, 2000, 4000, 8000, 16000]\n'
     'make = lambda n: (sorted(random.random() for _ in range(n)), 2.0)\n\n'
     'plot_growth({"linear": measure(lambda a: linear_search(*a), sizes, make)},\n'
     '            reference=["n"])'),

    (3, "recursion", "Recursion", "dsa.recursion",
     "Base case, recursive case, and the call stack that holds it all up.",
     'import sys\nprint("recursion limit:", sys.getrecursionlimit())\n\n'
     '# hanoi(n) is exactly 2**n - 1 moves. Try n = 3, then n = 20.\n'
     '# from dsa.recursion import hanoi\n'
     '# len(hanoi(3))'),

    (4, "dynamic-array", "Arrays and dynamic arrays", "dsa.dynamic_array",
     "Contiguous memory, O(1) indexing, and why append is *amortised* O(1).",
     'from viz.draw import draw_array\n\n'
     'draw_array([5, 2, 9, 1, 7], highlight=2, done=[0, 1])\n\n'
     '# Once DynamicArray works, plot resize_count against the number of appends\n'
     '# and watch the doubling show up as a staircase.'),

    (5, "linked-list", "Linked lists", "dsa.linked_list",
     "Nodes and references. O(1) at the head, O(n) to index — the mirror of an array.",
     'from viz.draw import draw_linked_list\n\n'
     'draw_linked_list(["a", "b", "c", "d"], highlight=1)'),

    (6, "stacks", "Stacks", "dsa.stack",
     "LIFO, and the two applications that justify it.",
     'from viz.draw import draw_array\n\n'
     '# A stack drawn as an array: the top is the last cell.\n'
     'draw_array([3, 1, 4], highlight=2, title="top of stack")'),

    (7, "queues", "Queues", "dsa.queue",
     "FIFO, and the O(n) vs O(1) demonstration you measure yourself.",
     'from viz.complexity import measure, plot_growth\n\n'
     '# Once both queues work, time them against each other:\n'
     '# plot_growth({"SlowQueue": ..., "CircularQueue": ...}, reference=["n", "1"])'),

    (8, "searching", "Searching", "dsa.searching",
     "Eight functions, one idea: what a sorted invariant buys you.",
     'from viz.draw import draw_array\n\n'
     'draw_array([1, 3, 5, 7, 9, 11, 13], highlight=3, done=[0, 1, 2],\n'
     '           title="binary search: mid, and the half already discarded")'),

    (9, "sorting-basic", "Basic sorting", "dsa.sorting",
     "Bubble, selection, insertion — and counting sort, which does not compare.",
     'from viz.animate import step_slider\n\n'
     'def bubble_sort_steps(values):\n'
     '    values = list(values)\n'
     '    for i in range(len(values)):\n'
     '        for j in range(len(values) - i - 1):\n'
     '            yield values, (j, j + 1)\n'
     '            if values[j] > values[j + 1]:\n'
     '                values[j], values[j + 1] = values[j + 1], values[j]\n'
     '    yield values, ()\n\n'
     'step_slider(bubble_sort_steps([5, 2, 9, 1, 7]))'),

    (10, "sorting-advanced", "Advanced sorting", "dsa.sorting",
     "Merge, quick and heap sort — and why the pivot decides quicksort's fate.",
     'from viz.animate import animate_bars\nfrom IPython.display import HTML\n\n'
     '# Write merge_sort_steps as a generator and it animates for free:\n'
     '# HTML(animate_bars(merge_sort_steps([5, 2, 9, 1, 7, 3])).to_jshtml())'),

    (11, "trees", "Trees and traversals", "dsa.tree",
     "Binary search trees, the three delete cases, and the four walks.",
     'from viz.draw import draw_tree\nfrom dsa.tree import BinarySearchTree, to_edges\n\n'
     '# bst = BinarySearchTree([8, 3, 10, 1, 6, 14, 4, 7, 13])\n'
     '# draw_tree(to_edges(bst.root), highlight={"6"})'),

    (12, "heaps", "Heaps and priority queues", "dsa.heap",
     "The array *is* the tree. Sift up, sift down, and heapify in O(n).",
     'from viz.draw import draw_array_as_tree\n\n'
     '# The same list, seen both ways — no conversion needed.\n'
     'draw_array_as_tree([1, 3, 2, 7, 4, 9, 5], highlight=0)'),

    (13, "hash-tables", "Hash tables", "dsa.hashmap",
     "Hashing, collisions, load factor — and what breaks \"O(1) average\".",
     'from viz.draw import draw_array\n\n'
     '# A chaining table is an array of buckets. Draw the bucket lengths and\n'
     '# watch them even out as the table resizes.\n'
     'draw_array([2, 0, 1, 3, 0, 1, 0, 2], title="bucket occupancy")'),

    (14, "graphs", "Graphs and graph searches", "dsa.graph",
     "Adjacency list vs matrix, then BFS and DFS over both.",
     'from viz.draw import draw_graph\nfrom dsa.graph import Graph, to_networkx\n\n'
     '# g = Graph()\n'
     '# for a, b in [("A","B"), ("A","C"), ("B","C"), ("B","D")]:\n'
     '#     g.add_edge(a, b)\n'
     '# draw_graph(to_networkx(g), highlight_nodes=["A"])'),

    (15, "language-translation", "The principles of language translation", "dsa.translation",
     "Text to tokens to a tree to an answer. A stack, recursion and a tree at once.",
     'from viz.draw import draw_tree\nfrom dsa.translation import Parser, tokenize, to_edges\n\n'
     '# ast = Parser(tokenize("3 + 4 * 2")).parse()\n'
     '# draw_tree(to_edges(ast))   # * sits deeper than + — that IS the precedence'),
]


# Module -> the test file that grades it. Explicit, because it does not follow
# from the slug: stacks and queues share one test file, both sorting weeks
# share another, and several modules are singular where the week is plural.
TESTS = {
    "dsa.recursion": "test_recursion.py",
    "dsa.dynamic_array": "test_dynamic_array.py",
    "dsa.linked_list": "test_linked_list.py",
    "dsa.stack": "test_stack_queue.py",
    "dsa.queue": "test_stack_queue.py",
    "dsa.searching": "test_searching.py",
    "dsa.sorting": "test_sorting.py",
    "dsa.tree": "test_tree.py",
    "dsa.heap": "test_heap.py",
    "dsa.hashmap": "test_hashmap.py",
    "dsa.graph": "test_graph.py",
    "dsa.translation": "test_translation.py",
}


# nbformat 4.5 requires every cell to carry a unique id. Counting rather than
# using uuid4 keeps regeneration deterministic, so a rebuild is not a diff.
_cell_number = 0


def _next_id():
    global _cell_number
    _cell_number += 1
    return f"cell{_cell_number:03d}"


def markdown(text):
    return {"cell_type": "markdown", "id": _next_id(), "metadata": {},
            "source": text.split("\n")}


def code(text):
    return {"cell_type": "code", "id": _next_id(), "execution_count": None,
            "metadata": {}, "outputs": [], "source": text.split("\n")}


BOOTSTRAP = (
    "# Put the repository root on sys.path so `import dsa` and `import viz` work.\n"
    "import sys\n"
    "from pathlib import Path\n"
    "\n"
    "ROOT = Path.cwd().parent if Path.cwd().name == \"notebooks\" else Path.cwd()\n"
    "if str(ROOT) not in sys.path:\n"
    "    sys.path.insert(0, str(ROOT))\n"
    "\n"
    "print(\"python :\", sys.version.split()[0])\n"
    "print(\"root   :\", ROOT)"
)


def build(number, slug, title, module, objective, demo):
    global _cell_number
    _cell_number = 0            # ids restart per notebook, so they stay stable
    cells = [
        markdown(
            f"# Week {number:02d} — {title}\n"
            f"\n"
            f"**{objective}**\n"
            f"\n"
            f"- Plan: [`docs/course/01-study-plan.md`](../docs/course/01-study-plan.md)\n"
            f"- Which bylaw asks for this: [`docs/course/02-coverage.md`](../docs/course/02-coverage.md)\n"
            + (f"- Implement: `{module.replace('.', '/')}.py`\n"
               f"- Graded by: `tests/{TESTS[module]}`\n" if module else "")
        ),
        code(BOOTSTRAP),
    ]

    if module:
        cells += [
            markdown("## The contract\n\nRead the docstrings before you write anything — they state the\ncomplexity target, not just the behaviour."),
            code(f"import {module}\n\nhelp({module})"),
        ]

    cells += [
        markdown("## Try it\n\n" + ("Run this once your implementation works." if module
                                    else "Nothing to implement this week — read and run.")),
        code(demo),
        markdown("## Your scratch space\n\nBreak things here. Nothing below is graded."),
        code("# ..."),
    ]

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "DSA27 (Python 3.13)",
                           "language": "python", "name": "dsa27"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main():
    OUT.mkdir(exist_ok=True)
    created = skipped = 0
    for number, slug, title, module, objective, demo in WEEKS:
        path = OUT / f"{number:02d}-{slug}.ipynb"
        if path.exists():
            print(f"  skip    {path.name}  (already exists)")
            skipped += 1
            continue
        path.write_text(
            json.dumps(build(number, slug, title, module, objective, demo),
                       indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print(f"  created {path.name}")
        created += 1
    print(f"\n{created} created, {skipped} left alone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
