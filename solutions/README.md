# Worked solutions

Every exercise in this course has a worked solution here, **for after you have
tried**. The folder mirrors the repository:

| Your exercise | Its solution | Checked by |
|---|---|---|
| `dsa/array_ops.py` (Week 2) | [`solutions/dsa/array_ops.py`](dsa/array_ops.py) | `tests/test_array_ops.py` |
| `dsa/recursion.py` (Week 3) | [`solutions/dsa/recursion.py`](dsa/recursion.py) | `tests/test_recursion.py` |
| `dsa/dynamic_array.py` (Week 4) | [`solutions/dsa/dynamic_array.py`](dsa/dynamic_array.py) | `tests/test_dynamic_array.py` |
| `dsa/linked_list.py` (Week 5) | [`solutions/dsa/linked_list.py`](dsa/linked_list.py) | `tests/test_linked_list.py` |
| `dsa/stack.py` (Week 6) | [`solutions/dsa/stack.py`](dsa/stack.py) | `tests/test_stack_queue.py` |
| `evaluate_postfix` in `dsa/translation.py` (Week 6) | [`solutions/dsa/translation.py`](dsa/translation.py) | `tests/test_translation.py -k evaluate_postfix` |
| `dsa/queue.py` (Week 7) | [`solutions/dsa/queue.py`](dsa/queue.py) | `tests/test_stack_queue.py` |
| `dsa/searching.py` (Week 8) | [`solutions/dsa/searching.py`](dsa/searching.py) | `tests/test_searching.py` |
| `dsa/sorting.py` (Weeks 9–10) | [`solutions/dsa/sorting.py`](dsa/sorting.py) | `tests/test_sorting.py` |
| `dsa/tree.py` (Week 11) | [`solutions/dsa/tree.py`](dsa/tree.py) | `tests/test_tree.py` |
| `dsa/heap.py` (Week 12) | [`solutions/dsa/heap.py`](dsa/heap.py) | `tests/test_heap.py` |
| `dsa/hashmap.py` (Week 13) | [`solutions/dsa/hashmap.py`](dsa/hashmap.py) | `tests/test_hashmap.py` |
| `dsa/graph.py` (Week 14) | [`solutions/dsa/graph.py`](dsa/graph.py) | `tests/test_graph.py` |
| the rest of `dsa/translation.py` (Week 15) | [`solutions/dsa/translation.py`](dsa/translation.py) | `tests/test_translation.py` |
| `dsa/dynamic_programming.py` (enrichment) | [`solutions/dsa/dynamic_programming.py`](dsa/dynamic_programming.py) | `tests/test_dynamic_programming.py` |
| `labs/lab01.py` … `lab03.py` | [`solutions/labs/`](labs/) | `tests/test_lab01.py` … `test_lab03.py` |
| `practice/week01.py` … `week15.py` | [`solutions/practice/`](practice/) | `tests/test_practice_week01.py` … |

All fifteen weeks are solved, and so is the enrichment module
`dsa/dynamic_programming.py` — not examined, but worth your weekend.

## How to use them without wasting them

A solution you read before you have struggled teaches you almost nothing: it
looks obvious, you nod, and a week later you cannot write it. The struggle is
where the learning happens. So:

1. **Try first — properly.** Read the docstring, draw the structure on paper,
   write the code, run the tests. Give it at least one real session.
2. **When a test fails, read the test.** `tests/` says exactly what "correct"
   means, often with a comment on the trap it is checking.
3. **Stuck for real?** Read the lecture handout's section on that exercise, then
   the question bank's traces. Ask on the course channel or in the lab.
4. **Only then open the solution** — and read just the one function you need.
   Close it, and write yours again from memory.
5. **After your tests pass**, compare. The solution is not the only correct
   answer; look for what it does more simply than yours, and for the edge case
   you handled differently.

Copying a solution into `dsa/` gets the tests to pass and teaches you nothing.
The exams are written, on paper, with no computer: what you have not written
yourself, you will not be able to write there.

## Run the tests against the solutions

`--solutions` runs the ordinary tests with the solutions in place of your code —
your own files are not touched:

```powershell
pytest --solutions tests/test_stack_queue.py -v     # the reference passes
pytest tests/test_stack_queue.py -v                 # your code, as usual
```

Handy when you are not sure whether a failure is in your code or in your
understanding of the test.

## Run a script with the solutions

```powershell
python tools/with_solutions.py tools/figures_l08.py
```

`tools/with_solutions.py` runs any script with `import dsa...`, `practice...` and
`labs...` resolving to the solutions first. The lecture figures that time a
finished module were made this way.

## How it works

`solutions/__init__.py` puts `solutions/dsa`, `solutions/practice` and
`solutions/labs` at the front of the search path of the `dsa`, `practice` and
`labs` packages. A module found in `solutions/` shadows the skeleton; one that
is not there falls back to the repository. So a solution that says
`from dsa.stack import Stack` gets the solved `Stack`, and `dsa/array.py` — which
was never an exercise — is shared.

The practice solutions are the same code as the answers files in
`docs/question-bank/`, line for line; the answers files add the explanations.
