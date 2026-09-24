# DSA27 Lab Manual — Weeks 1 to 3: Python for Data Structures

The first three labs give everyone in the room the same Python, fast. Some of
you wrote Python last year; some wrote only C++; some of you, in Bio, have not
yet written a class at all. By the end of Week 3 all of you need the same thing:
to be able to read and write the classes in `dsa/`.

These labs follow the official Python tutorial, reorganised for this course and
cut down to what the course actually needs. **Everything you need is in this
folder.** You do not need the tutorial, a textbook or a video to do them.

| Week | Lab | You write | Graded by | PDF |
|---|---|---|---|---|
| **1** | [The interpreter, numbers, strings and lists](lab01-python-basics.md) | `labs/lab01.py` | `tests/test_lab01.py` | [Lab 01](../pdf/DSA27-Lab01.pdf) |
| **2** | [Control flow, functions, errors and modules](lab02-control-flow-functions.md) | `labs/lab02.py` | `tests/test_lab02.py` | [Lab 02](../pdf/DSA27-Lab02.pdf) |
| **3** | [Data structures, classes and generators](lab03-data-structures-classes.md) | `labs/lab03.py` | `tests/test_lab03.py` | [Lab 03](../pdf/DSA27-Lab03.pdf) |
| — | [Notes for teaching assistants](ta-guide.md) | | | [TA guide](../pdf/DSA27-Lab-TA-Guide.pdf) |

## What each lab covers

**Lab 01 — Week 1.** Running Python three ways (REPL, script, notebook). Numbers:
`/` against `//` against `%`, integers that never overflow, floats that are
approximate. Strings: indexing, slicing, methods, f-strings. Lists: indexing,
slicing, mutation, and the one idea that matters most — **a name refers to an
object**, so `b = a` copies nothing. A first `while` loop and a first `if`. How
to run the tests.

**Lab 02 — Week 2.** `if`/`elif`/`else` and truthiness. `for`, `range`,
`enumerate`, `zip`; `break`, `continue` and the loop `else`. The `match`
statement. Functions: scope, how arguments are passed, default values and the
mutable-default trap, keyword arguments, `*args`/`**kwargs`, `lambda`. Errors:
reading a traceback, `try`/`except`/`else`/`finally`, `raise`, `assert`.
Modules and packages, and `if __name__ == "__main__":`. Then counting and timing
loops — the practical side of Lecture 02 on complexity.

**Lab 03 — Week 3.** Every list method **and its cost**. Lists as stacks and
queues, and `deque`. List, set and dictionary comprehensions. Tuples, sets and
dictionaries, and how to choose between them. Classes: `__init__`, `self`,
methods, the shared-class-variable trap, encapsulation, special methods
(`__len__`, `__iter__`, `__eq__`, `__repr__`, ...), inheritance and your own
exceptions. Iterators, generators and `yield`. A bridge into Lecture 03 on
recursion and the call stack.

### What was left out, on purpose

The Python tutorial also covers file input and output, virtual environments in
depth, floating-point representation in depth, the standard library tour,
decimal arithmetic, scopes and namespaces in full, multiple inheritance, and
more. None of it is needed to build the structures in this course, and some of
it you will meet on the way anyway. After Week 3 you can look up anything else
as you need it; `help()` in the REPL is always there.

## How a lab session works

Every lab is **two hours**. Each one runs the same way:

1. **Before the lab**, read the whole lab document. It takes about an hour.
   Come with the environment already working — Part 0 of Lab 01.
2. **In the first 20–30 minutes**, the TA demonstrates the key ideas at the
   REPL and answers questions on the reading.
3. **For the rest of the session**, you work through the examples and the
   **Checkpoints**, then the exercises in `labs/labNN.py`. Ask for help after
   ten minutes stuck, not after an hour.
4. **Before you leave**, show the TA your test results. What you did not finish
   is homework, due before the next lab.

## The exercises

Each lab has a starter file in [`labs/`](../../labs/) and a test file in
[`tests/`](../../tests/). Every function starts as

```python
    raise NotImplementedError
```

and your job is to replace that line with code that makes the tests pass. The
docstring is the contract; the test file is the full specification. From the
`DSA27` folder, with the virtual environment active:

```powershell
pytest tests/test_lab01.py -v           # one lab, one line per test
pytest tests/test_lab01.py -x           # stop at the first failure
pytest tests/test_lab01.py -k initials  # only the tests for one function
pytest -m lab                           # all three labs
```

The lab tests are marked `challenge`, like every other exercise, so the
environment check `pytest -m "not challenge"` does not run them and still passes
before you have written anything.

**Worked solutions** are in [`solutions/labs/`](../../solutions/labs/) — for
after you have tried, as [`solutions/README.md`](../../solutions/README.md)
explains. `pytest --solutions tests/test_lab01.py` runs the tests on them.

**Rules.**

- **Do not edit the test files.** A test you changed proves nothing. The TA runs
  the original tests.
- **Use what the lab has taught.** Lab 01 exercises must not use `for` or
  `import`; Lab 02's `stats` must not use `min`, `max` or `sum`. The point is the
  practice, not the answer.
- **Discuss ideas freely; write your own code.** Explaining an approach to a
  classmate is encouraged. Sending them your file is not — for either of you.
  Every lab ends with the TA asking you to explain a line of your code.

## After the labs

From Week 3 the exercises move into [`dsa/`](../../dsa/) and follow the
[study plan](../course/01-study-plan.md): `dsa/recursion.py` this week, then
dynamic arrays, linked lists, stacks and queues. They look exactly like the
labs — skeleton, docstring, test file — so by then the routine will be
familiar.
