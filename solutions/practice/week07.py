"""SOLUTION — try the problems in `practice/week07.py` first; see `solutions/README.md`.

Question bank, Week 7 — queues. Problems W7-C1 to W7-C5.

Questions:  docs/question-bank/week07-questions.md
Tests:      tests/test_practice_week07.py

Use your own structures as the working storage — `CircularQueue` from
`dsa/queue.py` and `Stack` from `dsa/stack.py` — not a Python list or
`collections.deque`. Lists are fine as inputs and results.
"""

from dsa.queue import CircularQueue  # noqa: F401  (your Week 7 exercise)
from dsa.stack import Stack  # noqa: F401  (your Week 6 exercise)


class StackQueue:
    """W7-C1. A FIFO queue built from two stacks — amortised O(1) per operation.

    enqueue(value); dequeue() -> the oldest value (IndexError when empty);
    len(q).

    Hint: an `inbox` stack for enqueue and an `outbox` stack for dequeue. Pour
    the inbox into the outbox only when the outbox is empty.
    """

    def __init__(self):
        self._inbox = Stack()             # enqueue pushes here
        self._outbox = Stack()            # dequeue pops here; oldest on top

    def enqueue(self, value):
        self._inbox.push(value)

    def dequeue(self):
        if self._outbox.is_empty():       # pour only when the outbox is empty
            while not self._inbox.is_empty():
                self._outbox.push(self._inbox.pop())
        return self._outbox.pop()         # IndexError when both are empty

    def __len__(self):
        return len(self._inbox) + len(self._outbox)


def josephus(names, k):
    """W7-C2. People stand in a circle; counting from the first, every k-th leaves.

    Return the names in the order they leave; the last one in the list is the
    survivor. Counting restarts from the person after the one who left.

    josephus(["A", "B", "C", "D", "E"], 2) -> ["B", "D", "A", "E", "C"]
    josephus([1, 2, 3, 4, 5, 6, 7], 3)     -> [3, 6, 2, 7, 5, 1, 4]

    k >= 1. Use a queue: moving someone from the front to the back is "passing
    them by".
    """
    circle = CircularQueue(max(1, len(names)))
    for name in names:
        circle.enqueue(name)
    order = []
    while len(circle) > 0:
        for _ in range(k - 1):
            circle.enqueue(circle.dequeue())   # passed by: front to back
        order.append(circle.dequeue())          # the k-th leaves
    return order


def moving_averages(values, k):
    """W7-C3. The average of every window of k consecutive values, left to right.

    moving_averages([2, 4, 6, 8, 10], 3) -> [4.0, 6.0, 8.0]
    moving_averages([5, 1], 3)           -> []        (no full window)

    k >= 1; otherwise raise ValueError. O(n), not O(nk): keep the window in a
    `CircularQueue(k)` and a running total — when a value enters, the oldest
    one leaves.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    window = CircularQueue(k)
    total, result = 0, []
    for value in values:
        if len(window) == k:
            total -= window.dequeue()           # the oldest value leaves
        window.enqueue(value)
        total += value
        if len(window) == k:
            result.append(total / k)
    return result


def reverse_first_k(values, k):
    """W7-C4. Put the values through a queue, but reverse the first k of them.

    reverse_first_k([1, 2, 3, 4, 5], 3) -> [3, 2, 1, 4, 5]

    Only a queue and a stack may hold the values while you work. 0 <= k <=
    len(values); otherwise raise ValueError. O(n).
    """
    if not 0 <= k <= len(values):
        raise ValueError(f"k must be between 0 and {len(values)}")
    queue = CircularQueue(max(1, len(values)))
    for value in values:
        queue.enqueue(value)
    stack = Stack()
    for _ in range(k):                          # the first k onto the stack...
        stack.push(queue.dequeue())
    result = []
    while not stack.is_empty():                 # ...come off reversed
        result.append(stack.pop())
    while len(queue) > 0:                       # the rest keep their order
        result.append(queue.dequeue())
    return result


def binary_numbers(n):
    """W7-C5. The binary representations of 1 to n, in order, generated with a queue.

    binary_numbers(5) -> ["1", "10", "11", "100", "101"]
    binary_numbers(0) -> []

    Do not convert numbers with bin() or format(): start from "1", and each time
    you dequeue a string s, enqueue s + "0" and s + "1". O(n).
    """
    result = []
    pending = CircularQueue(2 * n + 1)          # never needs to grow
    pending.enqueue("1")
    while len(result) < n:
        s = pending.dequeue()
        result.append(s)
        pending.enqueue(s + "0")
        pending.enqueue(s + "1")
    return result
