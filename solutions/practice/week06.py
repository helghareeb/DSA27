"""SOLUTION — try the problems in `practice/week06.py` first; see `solutions/README.md`.

Question bank, Week 6 — stacks. Problems W6-C1 to W6-C5.

Questions:  docs/question-bank/week06-questions.md
Tests:      tests/test_practice_week06.py

Use your `Stack` from `dsa/stack.py` as the working storage — not a Python list
used as a stack. Lists are fine as inputs and results.
"""

from dsa.stack import Stack  # noqa: F401  (your Week 6 exercise)


def reverse_words(sentence):
    """W6-C1. The words of `sentence` in reverse order, separated by one space.

    reverse_words("data structures are fun") -> "fun are structures data"
    reverse_words("")                        -> ""
    """
    words = Stack(sentence.split())
    out = []
    while not words.is_empty():
        out.append(words.pop())
    return " ".join(out)


class MinStack:
    """W6-C2. A stack that can also report its smallest value — all in O(1).

    push(value); pop() -> value; peek() -> value; get_min() -> the smallest
    value currently in the stack; len(s). pop, peek and get_min raise IndexError
    when empty.

    Hint: a second stack, holding the minimum so far at each level.
    """

    def __init__(self):
        self._values = Stack()
        self._mins = Stack()              # _mins.peek() is the minimum so far

    def push(self, value):
        self._values.push(value)
        if self._mins.is_empty() or value < self._mins.peek():
            self._mins.push(value)
        else:
            self._mins.push(self._mins.peek())

    def pop(self):
        self._mins.pop()                  # IndexError when empty, as required
        return self._values.pop()

    def peek(self):
        return self._values.peek()

    def get_min(self):
        return self._mins.peek()

    def __len__(self):
        return len(self._values)


def next_greater(values):
    """W6-C3. For each element, the first LATER element that is larger, or -1.

    next_greater([2, 1, 5, 3, 4]) -> [5, 5, -1, 4, -1]

    O(n): keep a stack of the indices still waiting for their answer. Each index
    is pushed once and popped at most once.
    """
    result = [-1] * len(values)
    waiting = Stack()                     # indices still waiting for an answer
    for i, value in enumerate(values):
        while not waiting.is_empty() and values[waiting.peek()] < value:
            result[waiting.pop()] = value
        waiting.push(i)
    return result


def tags_balanced(html):
    """W6-C4. True if the tags in `html` open and close in the right order.

    Tags look like <name> and </name> (no attributes, no self-closing tags); any
    other text is ignored.

    tags_balanced("<p><b>hi</b></p>") -> True
    tags_balanced("<p><b>hi</p></b>") -> False
    """
    open_tags = Stack()
    i = 0
    while True:
        start = html.find("<", i)
        if start == -1:
            break
        end = html.find(">", start)
        if end == -1:
            return False
        tag = html[start + 1:end]
        if tag.startswith("/"):
            if open_tags.is_empty() or open_tags.pop() != tag[1:]:
                return False
        else:
            open_tags.push(tag)
        i = end + 1
    return open_tags.is_empty()


def decode(encoded):
    """W6-C5. Expand k[text] — text repeated k times — which may nest.

    decode("3[ab]2[c]")  -> "abababcc"
    decode("2[a3[b]]")   -> "abbbabbb"
    decode("xy")         -> "xy"

    k is a positive decimal number, possibly more than one digit.
    """
    counts, texts = Stack(), Stack()
    current, number = "", 0
    for ch in encoded:
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch == "[":
            counts.push(number)
            texts.push(current)           # save what came before this group
            current, number = "", 0
        elif ch == "]":
            current = texts.pop() + current * counts.pop()
        else:
            current += ch
    return current
