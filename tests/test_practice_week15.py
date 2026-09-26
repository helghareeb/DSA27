"""Question bank, Week 15 practice. Fail until `practice/week15.py` is written."""

import random

import pytest

from dsa.translation import BinOp, Num
from practice.week15 import (calculate_with_power, postfix_to_tree, to_infix,
                             to_infix_minimal, to_postfix)

pytestmark = [pytest.mark.challenge, pytest.mark.practice]


def tree_of(text):
    """The parser's tree — used only by the round-trip tests."""
    from dsa.translation import Parser, tokenize
    return Parser(tokenize(text)).parse()


# 3 + 4 * 2, built by hand so the first tests do not need your parser
T_PREC = BinOp("+", Num(3.0), BinOp("*", Num(4.0), Num(2.0)))
T_PAREN = BinOp("*", BinOp("+", Num(3.0), Num(4.0)), Num(2.0))
T_LEFT = BinOp("-", BinOp("-", Num(1.0), Num(2.0)), Num(3.0))
T_RIGHT = BinOp("-", Num(1.0), BinOp("-", Num(2.0), Num(3.0)))


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        return Num(float(rng.randint(0, 9)))
    return BinOp(rng.choice("+-*/"), random_tree(rng, depth - 1), random_tree(rng, depth - 1))


# -- W15-C1 ---------------------------------------------------------------


@pytest.mark.parametrize(
    "tree,expected",
    [(Num(7.0), ["7"]), (Num(2.5), ["2.5"]), (T_PREC, ["3", "4", "2", "*", "+"]),
     (T_PAREN, ["3", "4", "+", "2", "*"]), (T_LEFT, ["1", "2", "-", "3", "-"]),
     (T_RIGHT, ["1", "2", "3", "-", "-"])],
)
def test_to_postfix(tree, expected):
    assert to_postfix(tree) == expected


def test_to_postfix_agrees_with_the_stack_route():
    """Post-order of the parser's tree IS the shunting-yard output."""
    from dsa.stack import infix_to_postfix
    from dsa.translation import tokenize

    for text in ["3 + 4 * 2", "(3 + 4) * 2", "1 - 2 - 3", "8 / 4 / 2", "2 * (3 + (4 - 1))"]:
        assert to_postfix(tree_of(text)) == infix_to_postfix(tokenize(text))


# -- W15-C2 ---------------------------------------------------------------


@pytest.mark.parametrize(
    "tree,expected",
    [(Num(7.0), "7"), (T_PREC, "(3 + (4 * 2))"), (T_PAREN, "((3 + 4) * 2)"),
     (T_LEFT, "((1 - 2) - 3)"), (T_RIGHT, "(1 - (2 - 3))"),
     (BinOp("/", Num(1.5), Num(2.0)), "(1.5 / 2)")],
)
def test_to_infix(tree, expected):
    assert to_infix(tree) == expected


# -- W15-C3 ---------------------------------------------------------------


@pytest.mark.parametrize(
    "tree,expected",
    [(Num(7.0), "7"), (T_PREC, "3 + 4 * 2"), (T_PAREN, "(3 + 4) * 2"),
     (T_LEFT, "1 - 2 - 3"), (T_RIGHT, "1 - (2 - 3)"),
     (BinOp("/", Num(8.0), BinOp("/", Num(4.0), Num(2.0))), "8 / (4 / 2)"),
     (BinOp("+", Num(1.0), BinOp("+", Num(2.0), Num(3.0))), "1 + (2 + 3)"),
     (BinOp("*", BinOp("*", Num(2.0), Num(3.0)), BinOp("+", Num(4.0), Num(5.0))), "2 * 3 * (4 + 5)"),
     (BinOp("-", BinOp("*", Num(2.0), Num(3.0)), BinOp("/", Num(4.0), Num(5.0))), "2 * 3 - 4 / 5")],
)
def test_to_infix_minimal(tree, expected):
    assert to_infix_minimal(tree) == expected


def test_to_infix_minimal_round_trips():
    """Whatever the tree, printing it and parsing it back gives the same tree."""
    rng = random.Random(15)
    for _ in range(300):
        tree = random_tree(rng, 5)
        assert tree_of(to_infix_minimal(tree)) == tree


# -- W15-C4 ---------------------------------------------------------------


@pytest.mark.parametrize(
    "tokens,expected",
    [(["7"], Num(7.0)), (["3", "4", "2", "*", "+"], T_PREC), (["3", "4", "+", "2", "*"], T_PAREN),
     (["1", "2", "-", "3", "-"], T_LEFT), (["1", "2", "3", "-", "-"], T_RIGHT)],
)
def test_postfix_to_tree(tokens, expected):
    assert postfix_to_tree(tokens) == expected


@pytest.mark.parametrize("tokens", [[], ["+"], ["3", "+"], ["3", "4"], ["3", "4", "+", "-"]])
def test_postfix_to_tree_rejects_malformed_input(tokens):
    with pytest.raises(ValueError):
        postfix_to_tree(tokens)


def test_postfix_to_tree_inverts_to_postfix():
    rng = random.Random(6)
    for _ in range(300):
        tree = random_tree(rng, 6)
        assert postfix_to_tree(to_postfix(tree)) == tree


# -- W15-C5 ---------------------------------------------------------------


@pytest.mark.parametrize(
    "tokens,expected",
    [(["7"], 7.0), (["2", "^", "3"], 8.0), (["2", "^", "3", "^", "2"], 512.0),
     (["(", "2", "^", "3", ")", "^", "2"], 64.0), (["-", "2", "^", "2"], -4.0),
     (["2", "^", "-", "1"], 0.5), (["2", "*", "3", "^", "2"], 18.0),
     (["1", "+", "2", "^", "2", "*", "3"], 13.0), (["-", "-", "3"], 3.0),
     (["1", "-", "2", "-", "3"], -4.0), (["8", "/", "4", "/", "2"], 1.0)],
)
def test_calculate_with_power(tokens, expected):
    assert calculate_with_power(tokens) == pytest.approx(expected)


def test_calculate_with_power_matches_python():
    """Python's ** has exactly this precedence and associativity."""
    cases = ["2 ^ 3 ^ 2", "-2 ^ 2", "2 ^ -1", "3 * 2 ^ 2 - 1", "-(2 + 1) ^ 2", "2 ^ 2 ^ -1"]
    for text in cases:
        tokens = text.replace("(", " ( ").replace(")", " ) ").replace("-", " - ").split()
        python = eval(text.replace("^", "**"))    # the oracle, in the test only
        assert calculate_with_power(tokens) == pytest.approx(python)


@pytest.mark.parametrize("tokens", [[], ["2", "^"], ["^", "2"], ["(", "2"], ["2", ")"], ["2", "3"]])
def test_calculate_with_power_rejects_malformed_input(tokens):
    with pytest.raises(ValueError):
        calculate_with_power(tokens)
