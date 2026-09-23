# DSA27 — Data Structures & Algorithms

**CS2101** (AI) · **IS122** (Bioinformatics, Software Engineering)
Faculty of Computers and Information Sciences, Mansoura University

Course repository. We **implement the structures ourselves** rather than reach
for Python's built-ins — the point is to build the thing, not to call it.

**The storage rule.** Every structure in `dsa/` keeps its data only in the course
`Array` (`dsa/array.py`: fixed size, O(1) indexing, nothing else), in node
objects, or in another structure you built — never in a Python `list`, `dict` or
`set`. Lists are for passing data in and out, not for storing it. Why:
[Lecture 02](docs/lectures/02-complexity-and-arrays/lecture.md).

Topics: complexity, recursion, arrays and dynamic arrays, linked lists, stacks,
queues, searching, sorting (basic and advanced), trees and traversals, heaps and
priority queues, hash maps, graphs and graph searches, and the principles of
language translation — the union of what all three program bylaws declare.
Dynamic programming is included as enrichment.

---

## Course material

| | |
|---|---|
| **[Course documentation](docs/)** | Start here — guide, plan, lectures, regulations |
| [Course guide](docs/course/00-course-guide.md) | What the course is, how you are assessed, what fails you |
| [Study plan — 15 weeks](docs/course/01-study-plan.md) | Every week, and the file that grades it |
| [Coverage matrix](docs/course/02-coverage.md) | Every topic the لائحة declares → module → test |
| [Lecture 01 — Why This Course, and Why Python](docs/lectures/01-why-this-course/lecture.md) | [handout PDF](docs/pdf/DSA27-L01-handout.pdf) · [slides PDF](docs/pdf/DSA27-L01-slides.pdf) |
| [Lecture 02 — Complexity, and the Array](docs/lectures/02-complexity-and-arrays/lecture.md) | [handout PDF](docs/pdf/DSA27-L02-handout.pdf) · [slides PDF](docs/pdf/DSA27-L02-slides.pdf) |
| [Lecture 03 — Recursion](docs/lectures/03-recursion/lecture.md) | [handout PDF](docs/pdf/DSA27-L03-handout.pdf) · [slides PDF](docs/pdf/DSA27-L03-slides.pdf) |
| [Lecture 04 — Dynamic Arrays](docs/lectures/04-dynamic-arrays/lecture.md) | [handout PDF](docs/pdf/DSA27-L04-handout.pdf) · [slides PDF](docs/pdf/DSA27-L04-slides.pdf) |
| [Lecture 05 — Linked Lists](docs/lectures/05-linked-lists/lecture.md) | [handout PDF](docs/pdf/DSA27-L05-handout.pdf) · [slides PDF](docs/pdf/DSA27-L05-slides.pdf) |
| **[Question bank](docs/question-bank/)** | MCQ, essay, trace, complexity, proofs, bugs and code — with answers, and a mock exam |
| **[Lab manual — weeks 1–3](docs/labs/)** | Python for this course: [Lab 01](docs/labs/lab01-python-basics.md) · [Lab 02](docs/labs/lab02-control-flow-functions.md) · [Lab 03](docs/labs/lab03-data-structures-classes.md) · [TA notes](docs/labs/ta-guide.md) |
| [Official regulations](docs/course/regulations/) | The bylaws, and what they say about CS201 |
| [Links](docs/links.md) | WhatsApp channel, YouTube |

Announcements: **[WhatsApp channel](https://whatsapp.com/channel/0029Vb8XynEFy72KWbH6vS2V)** ·
Video: **[youtube.com/@0xHGH](https://www.youtube.com/@0xHGH)**

---

## Setup

You need **Python 3.10 or newer** and **[Graphviz](https://graphviz.org/download/)**
(the `dot` binary, not only the pip package).

```powershell
git clone https://github.com/helghareeb/DSA27.git
cd DSA27

py -3.13 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, use `python3 -m venv .venv` and `source .venv/bin/activate`.

**Check your setup before anything else:**

```powershell
pytest -m "not challenge"
```

All of these must pass. They verify your interpreter, the plotting stack,
Graphviz, and the drawing helpers. If one fails, the message tells you exactly
what is missing — fix that before blaming your own code.

> **Windows note:** if `python` opens the Microsoft Store instead of running,
> turn off the Store aliases under *Settings → Apps → Advanced app settings →
> App execution aliases* for `python.exe` and `python3.exe`.

---

## Layout

| Path | What it is |
|---|---|
| `dsa/` | The structures and algorithms — **you implement these** |
| `tools/` | Build the PDFs and figures — not needed for the exercises |
| `viz/` | Drawing, animation and timing helpers — already written, just use them |
| `labs/` | Weeks 1–3 Python lab exercises — **you implement these first** |
| `practice/` | Question-bank coding problems — ungraded, checked by `pytest -m practice` |
| `tests/` | The exercises, as tests. Make them pass. |
| `notebooks/` | One notebook per lecture topic |

---

## How the exercises work

Every function in `dsa/` is a skeleton: the docstring states the contract and
the complexity target, and the body raises `NotImplementedError`. The tests in
`tests/` define exactly what "correct" means.

```powershell
pytest tests/test_linked_list.py -v     # one topic
pytest -m challenge                     # every exercise
pytest -m lab                           # only the weeks 1-3 labs
pytest -m practice                      # only the question-bank problems
pytest -x                               # stop at the first failure
```

They all fail on day one. That is the assignment.

---

## Visualising your own code

The helpers in `viz/` take plain Python data, so they work with whatever you
write — they never import `dsa/`.

**Draw a structure:**

```python
from viz.draw import draw_array, draw_linked_list, draw_tree, draw_array_as_tree

draw_array([5, 2, 9, 1], highlight=2, done=[0])
draw_linked_list(["a", "b", "c"], highlight=1)
draw_tree([("8", "3"), ("8", "10"), ("3", "1")], highlight={"1"})
draw_array_as_tree([9, 7, 5, 3, 1])      # a heap: the array IS the tree
```

**Step through an algorithm.** Write your sort as a generator that yields a
snapshot, and you get animation and scrubbing for free:

```python
def bubble_sort_steps(values):
    values = list(values)
    for i in range(len(values)):
        for j in range(len(values) - i - 1):
            yield values, (j, j + 1)          # about to compare these two
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
    yield values, ()
```

```python
from viz.animate import step_slider, animate_bars
from IPython.display import HTML

step_slider(bubble_sort_steps([5, 2, 9, 1, 7]))        # slider, you set the pace
HTML(animate_bars(bubble_sort_steps([5, 2, 9, 1])).to_jshtml())   # plays itself
```

**Measure complexity** instead of asserting it:

```python
from viz.complexity import measure, plot_growth
import random

sizes = [1000, 2000, 4000, 8000, 16000]
make = lambda n: (sorted(random.random() for _ in range(n)), 0.5)

plot_growth(
    {"linear": measure(lambda a: linear_search(*a), sizes, make),
     "binary": measure(lambda a: binary_search(*a), sizes, make)},
    reference=["n", "log n"],
)
```

---

## Notebooks

```powershell
jupyter lab
```

Select the **DSA27 (Python 3.13)** kernel, or in VS Code pick the interpreter
at `.venv\Scripts\python.exe`.

Notebook **outputs are stripped automatically on commit** via `nbstripout`, so
diffs stay readable and re-running a cell does not create a conflict. Your
outputs stay visible locally — only what gets committed is cleaned. After
cloning, activate it once:

```powershell
nbstripout --install
```

---

## Debugging your implementations

This is the most useful habit in the course. Set a breakpoint in the gutter of
`dsa/linked_list.py`, press **F5**, and choose *pytest: current test file* —
then watch `node.next` change in the Variables panel as you step with **F10**.

Seeing a pointer move beats any diagram, including the ones in `viz/`.
