"""Data structures and algorithms, implemented from scratch.

Every module here is deliberately a **skeleton**. The docstrings state the
contract and the complexity target; the bodies raise `NotImplementedError`.
You fill them in during the lecture, and `tests/` tells you when you are right.

Nothing in this package may use the Python built-in that it is reimplementing.
Writing `list.sort()` inside `dsa/sorting.py` defeats the exercise — the point
is to build the thing, not to call it.

**The storage rule (Lecture 02).** A data structure here keeps its data only in

  * the course `Array` (`dsa/array.py`) — fixed size, O(1) indexing, given;
  * node objects (`Node`, `TreeNode`, `Entry`, ...); or
  * another structure you have already built in `dsa/`.

Never in a Python `list`, `dict`, `set` or `collections.deque`. Those hide
exactly the costs this course is about. Lists remain the *interface*: functions
may take a list as input and return a list as a result, and the tests use them
freely.
"""
