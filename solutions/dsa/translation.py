"""SOLUTION — try the exercise in `dsa/translation.py` first; see `solutions/README.md`.

`evaluate_postfix` is the Week 6 exercise (it needs only your `Stack`); the
lexer, the parser and the tree evaluator are Week 15's.

The principles of language translation — how source text becomes a result.

Declared in the bylaw: "an introduction to the principles of language
translation" (IS122, SWE 2013 p. 38 and Medical Informatics 2014 p. 35). For
Software Engineering students this is the foundation SWE141 *Software
Construction* is built on, where it becomes BNF, grammars and parser generators.

Every compiler and interpreter — including the CPython one running this file —
does the same three things to your source code:

    "3 + 4 * 2"
         |  tokenize()          text  ->  tokens
         v
    ["3", "+", "4", "*", "2"]
         |  Parser.parse()      tokens  ->  a tree
         v
            (+)                 the shape of the tree IS the precedence:
           /   \\                * binds tighter, so it sits deeper and
        (3)    (*)               therefore evaluates first
              /   \\
           (4)    (2)
         |  evaluate()          tree  ->  value
         v
           11

This module is the capstone of the course because it needs everything in it:
a **stack** to evaluate postfix, **recursion** to parse, and a **tree** to hold
the result. `dsa.stack.infix_to_postfix` already gives you the other classic
route from infix to a machine-friendly form; this module builds the tree route.

See the tree your parser built:

    from viz.draw import draw_tree
    draw_tree(to_edges(Parser(tokenize("3 + 4 * 2")).parse()))
"""

from __future__ import annotations

from dsa.array import Array


# -- the grammar this module implements -----------------------------------
#
#   expr   := term (('+' | '-') term)*
#   term   := factor (('*' | '/') factor)*
#   factor := NUMBER | '(' expr ')' | '-' factor
#
# One function per rule, each calling the rule below it. Precedence is not a
# table of numbers here -- it is the *shape* of the grammar. `expr` calls
# `term`, so `term` binds tighter, so `*` beats `+`. That is the whole trick.

DIGITS = "0123456789"
OPERATORS = "+-*/"


class Num:
    """A leaf: one number. Given to you."""

    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Num({self.value!r})"

    def __eq__(self, other):
        return isinstance(other, Num) and self.value == other.value


class BinOp:
    """An internal node: left <op> right. Given to you."""

    __slots__ = ("op", "left", "right")

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOp({self.op!r}, {self.left!r}, {self.right!r})"

    def __eq__(self, other):
        return (
            isinstance(other, BinOp)
            and self.op == other.op
            and self.left == other.left
            and self.right == other.right
        )


def to_edges(node):
    """Collect (parent, child) pairs for `viz.draw.draw_tree`. Given to you.

    Each id is "label#n", because one tree can hold the same number twice and
    the two must stay separate nodes. `draw_tree` hides everything after the
    `#`, so the picture shows "2", not "2#3".
    """
    counter = [0]
    edges = []

    def name(current):
        counter[0] += 1
        text = current.value if isinstance(current, Num) else current.op
        return f"{text}#{counter[0]}"

    def walk(current, current_name):
        if isinstance(current, BinOp):
            for child in (current.left, current.right):
                child_name = name(child)
                edges.append((current_name, child_name))
                walk(child, child_name)

    walk(node, name(node))
    return edges


# -- stage 1: text -> tokens ----------------------------------------------


def tokenize(text):
    """Split source text into a list of token strings.

    tokenize("3 + 4")        -> ["3", "+", "4"]
    tokenize("12*(3+4)")     -> ["12", "*", "(", "3", "+", "4", ")"]
    tokenize("  7  ")        -> ["7"]
    tokenize("")             -> []

    Whitespace separates but is never a token. Multi-digit numbers stay whole —
    "12" is one token, not two. A number may contain one decimal point: "3.5".
    Anything that is not a digit, an operator (+ - * /) or a parenthesis raises
    ValueError. Target: O(n).

    This is the *lexer*, and it is the easiest of the three stages. Do not use
    a regular expression — scanning it by hand is the exercise.
    """
    tokens = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():                         # separates tokens, is never one
            i += 1
        elif ch in OPERATORS or ch in "()":
            tokens.append(ch)                    # one character, one token
            i += 1
        elif ch in DIGITS or ch == ".":
            start, points = i, 0
            while i < len(text) and (text[i] in DIGITS or text[i] == "."):
                if text[i] == ".":
                    points += 1
                i += 1                           # keep going: "123" is ONE token
            number = text[start:i]
            if points > 1 or number == ".":
                raise ValueError(f"malformed number {number!r}")
            tokens.append(number)
        else:
            raise ValueError(f"unexpected character {ch!r} at position {i}")
    return tokens


# -- stage 2a: tokens -> value, using a stack -----------------------------


def evaluate_postfix(tokens):
    """Evaluate tokens already in postfix (reverse Polish) order.

    evaluate_postfix(["3", "4", "+"])            -> 7
    evaluate_postfix(["3", "4", "2", "*", "+"])  -> 11

    Push numbers; on an operator pop **two** values, apply, push the result.
    The second value popped is the left operand — get that backwards and
    subtraction and division silently give wrong answers.

    Leaves exactly one value on the stack, which is the answer; anything else
    means malformed input, so raise ValueError. Division by zero raises
    ZeroDivisionError. Target: O(n).

    Pair this with `dsa.stack.infix_to_postfix` and you have a complete
    calculator without ever building a tree.
    """
    from dsa.stack import Stack

    values = Stack()
    for token in tokens:
        if token in ("+", "-", "*", "/"):
            if len(values) < 2:
                raise ValueError(f"operator {token!r} needs two operands")
            right = values.pop()                     # popped first: the RIGHT operand
            left = values.pop()
            if token == "+":
                values.push(left + right)
            elif token == "-":
                values.push(left - right)
            elif token == "*":
                values.push(left * right)
            else:
                values.push(left / right)            # ZeroDivisionError on 0
        else:
            values.push(float(token) if "." in token else int(token))
    if len(values) != 1:
        raise ValueError("malformed postfix expression")
    return values.pop()


# -- stage 2b: tokens -> tree, using recursion ----------------------------


class Parser:
    """Recursive descent: one method per grammar rule.

        Parser(tokenize("3 + 4 * 2")).parse()
        -> BinOp("+", Num(3.0), BinOp("*", Num(4.0), Num(2.0)))

    "Recursive descent" because the methods call each other downwards and
    recurse back to the top through the parenthesis rule.
    """

    def __init__(self, tokens):
        self.tokens = Array.from_values(tokens)
        self.position = 0

    # -- helpers, given to you --------------------------------------------

    def peek(self):
        """The current token, or None at the end of input."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self):
        """Consume and return the current token."""
        token = self.peek()
        self.position += 1
        return token

    # -- one method per rule ----------------------------------------------

    def parse(self):
        """Parse the whole token list and return the AST root.

        Raises ValueError on empty input, and on trailing tokens that no rule
        consumed — "3 + 4 )" is an error, not the number 7.
        """
        if self.peek() is None:
            raise ValueError("empty expression")
        tree = self.expr()
        if self.peek() is not None:              # something no rule could use
            raise ValueError(f"unexpected {self.peek()!r} after the expression")
        return tree

    def expr(self):
        """expr := term (('+' | '-') term)*

        Parse a term, then keep absorbing `+ term` and `- term` while they are
        there. Build left-associatively: "1 - 2 - 3" must be (1 - 2) - 3 = -4,
        not 1 - (2 - 3) = 2.
        """
        node = self.term()
        while self.peek() in ("+", "-"):
            op = self.advance()
            node = BinOp(op, node, self.term())  # the old tree goes LEFT
        return node

    def term(self):
        """term := factor (('*' | '/') factor)*

        Same shape as `expr`, one precedence level tighter. Left-associative
        again: "8 / 4 / 2" is (8 / 4) / 2 = 1.
        """
        node = self.factor()
        while self.peek() in ("*", "/"):
            op = self.advance()
            node = BinOp(op, node, self.factor())
        return node

    def factor(self):
        """factor := NUMBER | '(' expr ')' | '-' factor

        Three cases:
          * a number          -> Num(float(token))
          * '(' -> call self.expr(), then require the matching ')'
          * '-' -> unary minus; return it as BinOp("-", Num(0.0), factor())

        The parenthesis case is where the recursion closes the loop: `factor`
        calls all the way back up to `expr`. Raise ValueError on anything else,
        including running off the end of the tokens.
        """
        token = self.peek()
        if token is None:
            raise ValueError("unexpected end of input")
        if token == "(":
            self.advance()
            node = self.expr()                   # back to the top rule: recursion
            if self.peek() != ")":
                raise ValueError("missing ')'")
            self.advance()
            return node
        if token == "-":
            self.advance()
            return BinOp("-", Num(0.0), self.factor())   # unary minus: 0 - x
        if token[0] in DIGITS or token[0] == ".":
            self.advance()
            return Num(float(token))
        raise ValueError(f"unexpected {token!r}")


# -- stage 3: tree -> value, by walking it --------------------------------


def evaluate(node):
    """Compute the value of an AST. Target: O(nodes).

    evaluate(Num(3.0))                             -> 3.0
    evaluate(BinOp("+", Num(1.0), Num(2.0)))       -> 3.0

    A post-order traversal wearing a different name: evaluate both children,
    then apply the operator. Compare it to `BinarySearchTree.post_order` in
    `dsa/tree.py` — it is the same walk.

    Division by zero raises ZeroDivisionError. An unknown operator raises
    ValueError.
    """
    if isinstance(node, Num):
        return node.value
    left = evaluate(node.left)                   # both children first ...
    right = evaluate(node.right)
    if node.op == "+":                           # ... then the node: post-order
        return left + right
    if node.op == "-":
        return left - right
    if node.op == "*":
        return left * right
    if node.op == "/":
        return left / right                      # ZeroDivisionError on 0
    raise ValueError(f"unknown operator {node.op!r}")


def calculate(text):
    """The whole pipeline, end to end: text in, number out.

    calculate("3 + 4 * 2")     -> 11.0
    calculate("(3 + 4) * 2")   -> 14.0
    calculate("-5 + 2")        -> -3.0

    Three lines: tokenize, parse, evaluate. Writing it is the moment the three
    stages stop being separate exercises.
    """
    tokens = tokenize(text)
    tree = Parser(tokens).parse()
    return evaluate(tree)
