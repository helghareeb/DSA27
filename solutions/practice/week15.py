"""SOLUTION — try the problems in `practice/week15.py` first; see `solutions/README.md`.

Question bank, Week 15 — the principles of language translation. Problems
W15-C1 to W15-C5.

Questions:  docs/question-bank/week15-questions.md
Tests:      tests/test_practice_week15.py

The trees are the `Num` and `BinOp` nodes of `dsa/translation.py`. Walk them
with recursion; use `Stack` from `dsa/stack.py` where a problem needs a stack,
not a Python list. Lists are fine as inputs and results. Do not use `eval`.
"""

from dsa.array import Array
from dsa.stack import Stack  # noqa: F401  (your Week 6 exercise)
from dsa.translation import BinOp, Num  # noqa: F401  (given to you)

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def number_text(value):
    """Given. 3.0 -> "3", 2.5 -> "2.5": a number as a person would write it."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def to_postfix(node):
    """W15-C1. The postfix token list of an AST, by a post-order walk.

    to_postfix(BinOp("+", Num(3.0), BinOp("*", Num(4.0), Num(2.0))))
        -> ["3", "4", "2", "*", "+"]

    Write numbers with `number_text`. O(n) for n nodes.
    """
    out = []

    def walk(current):
        if isinstance(current, Num):
            out.append(number_text(current.value))
        else:
            walk(current.left)          # left, right ...
            walk(current.right)
            out.append(current.op)      # ... then the node

    walk(node)
    return out


def to_infix(node):
    """W15-C2. Fully parenthesised infix: every operator gets its own pair.

    to_infix(BinOp("+", Num(3.0), BinOp("*", Num(4.0), Num(2.0))))
        -> "(3 + (4 * 2))"
    to_infix(Num(7.0)) -> "7"

    One space either side of each operator; no parentheses around a lone number.
    """
    if isinstance(node, Num):
        return number_text(node.value)
    return f"({to_infix(node.left)} {node.op} {to_infix(node.right)})"


def to_infix_minimal(node):
    """W15-C3. Infix with only the parentheses the grammar needs.

    "3 + 4 * 2" stays "3 + 4 * 2"; the tree of "(3 + 4) * 2" gives
    "(3 + 4) * 2"; the tree of "1 - (2 - 3)" keeps its parentheses, and the
    tree of "(1 - 2) - 3" loses them: "1 - 2 - 3".

    The result must parse back to the SAME tree with `dsa.translation.Parser`.
    Numbers are non-negative. Hint: a child needs parentheses when its operator
    binds more loosely than its parent's — or equally, if it is the RIGHT child.
    """
    if isinstance(node, Num):
        return number_text(node.value)
    mine = PRECEDENCE[node.op]
    left = to_infix_minimal(node.left)
    right = to_infix_minimal(node.right)
    if isinstance(node.left, BinOp) and PRECEDENCE[node.left.op] < mine:
        left = f"({left})"
    if isinstance(node.right, BinOp) and PRECEDENCE[node.right.op] <= mine:
        right = f"({right})"            # equal too: trees lean left
    return f"{left} {node.op} {right}"


def postfix_to_tree(tokens):
    """W15-C4. Build the AST from a postfix token list, with a stack of subtrees.

    postfix_to_tree(["3", "4", "2", "*", "+"])
        -> BinOp("+", Num(3.0), BinOp("*", Num(4.0), Num(2.0)))

    Like `evaluate_postfix`, but push trees instead of numbers. Raise
    ValueError when the tokens are not valid postfix. O(n).
    """
    trees = Stack()
    for token in tokens:
        if token in PRECEDENCE:
            if len(trees) < 2:
                raise ValueError(f"operator {token!r} needs two operands")
            right = trees.pop()         # popped first: the RIGHT one
            left = trees.pop()
            trees.push(BinOp(token, left, right))
        else:
            trees.push(Num(float(token)))
    if len(trees) != 1:
        raise ValueError("malformed postfix expression")
    return trees.pop()


class _PowerParser:
    """W15-C5's parser: the Week 15 grammar with a fifth rule for '^'."""

    def __init__(self, tokens):
        self.tokens = Array.from_values(tokens)
        self.position = 0

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self):
        token = self.peek()
        self.position += 1
        return token

    def expr(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            if self.advance() == "+":
                value = value + self.term()
            else:
                value = value - self.term()
        return value

    def term(self):
        value = self.unary()
        while self.peek() in ("*", "/"):
            if self.advance() == "*":
                value = value * self.unary()
            else:
                value = value / self.unary()
        return value

    def unary(self):
        if self.peek() == "-":
            self.advance()
            return -self.unary()
        return self.power()

    def power(self):
        base = self.atom()
        if self.peek() == "^":
            self.advance()
            return base ** self.unary()         # recursion: leans RIGHT
        return base

    def atom(self):
        token = self.advance()
        if token is None:
            raise ValueError("unexpected end of input")
        if token == "(":
            value = self.expr()
            if self.advance() != ")":
                raise ValueError("missing ')'")
            return value
        if token[0] in "0123456789.":
            return float(token)
        raise ValueError(f"unexpected {token!r}")


def calculate_with_power(tokens):
    """W15-C5. Evaluate a token list that may also contain '^' (power).

    '^' binds tighter than unary minus on its left and is RIGHT-associative,
    as `**` is in Python:

    calculate_with_power(["2", "^", "3", "^", "2"])  -> 512.0   2 ^ (3 ^ 2)
    calculate_with_power(["-", "2", "^", "2"])       -> -4.0    -(2 ^ 2)
    calculate_with_power(["2", "^", "-", "1"])       -> 0.5

    Grammar:
        expr  := term (('+' | '-') term)*
        term  := unary (('*' | '/') unary)*
        unary := '-' unary | power
        power := atom ('^' unary)?
        atom  := NUMBER | '(' expr ')'

    Raise ValueError on malformed input, including tokens left over.

    Hint: a small class like `Parser`, one method per rule, that computes the
    value as it goes instead of building a tree. `power` calls `unary` for its
    right side — recursion, not a loop — and that is what makes '^' lean right.
    """
    parser = _PowerParser(tokens)
    if parser.peek() is None:
        raise ValueError("empty expression")
    value = parser.expr()
    if parser.peek() is not None:
        left_over = parser.peek()
        raise ValueError(f"unexpected {left_over!r} after the expression")
    return value
