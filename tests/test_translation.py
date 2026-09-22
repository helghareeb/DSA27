"""Language translation exercises. Fail until `dsa/translation.py` is written.

Three stages, tested separately and then end to end:
text -> tokenize -> tokens -> Parser -> tree -> evaluate -> value.
"""

import pytest

from dsa.translation import (
    BinOp,
    Num,
    Parser,
    calculate,
    evaluate,
    evaluate_postfix,
    to_edges,
    tokenize,
)

pytestmark = pytest.mark.challenge


# -- stage 1: the lexer ---------------------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", []),
        ("3", ["3"]),
        ("  7  ", ["7"]),
        ("3 + 4", ["3", "+", "4"]),
        ("3+4", ["3", "+", "4"]),
        ("12*(3+4)", ["12", "*", "(", "3", "+", "4", ")"]),
        ("1 - 2 / 3", ["1", "-", "2", "/", "3"]),
        ("-5", ["-", "5"]),
    ],
)
def test_tokenize(text, expected):
    assert tokenize(text) == expected


def test_tokenize_keeps_multi_digit_numbers_whole():
    """"12" is one token, not "1" and "2". Getting this wrong makes
    12 + 1 evaluate to 4."""
    assert tokenize("123 + 45") == ["123", "+", "45"]


def test_tokenize_accepts_a_decimal_point():
    assert tokenize("3.5 + 1") == ["3.5", "+", "1"]


@pytest.mark.parametrize("text", ["3 $ 4", "a + 1", "3 & 4"])
def test_tokenize_rejects_unknown_characters(text):
    with pytest.raises(ValueError):
        tokenize(text)


# -- stage 2a: postfix evaluation, with a stack ---------------------------


@pytest.mark.parametrize(
    "tokens,expected",
    [
        (["3"], 3),
        (["3", "4", "+"], 7),
        (["3", "4", "2", "*", "+"], 11),
        (["3", "4", "+", "2", "*"], 14),
    ],
)
def test_evaluate_postfix(tokens, expected):
    assert evaluate_postfix(tokens) == expected


def test_evaluate_postfix_operand_order():
    """The test that catches a swapped pop. "5 3 -" is 5 - 3 = 2, not -2,
    and "8 2 /" is 4, not 0.25."""
    assert evaluate_postfix(["5", "3", "-"]) == 2
    assert evaluate_postfix(["8", "2", "/"]) == 4


@pytest.mark.parametrize("tokens", [[], ["3", "4"], ["+"], ["3", "+"]])
def test_evaluate_postfix_rejects_malformed_input(tokens):
    with pytest.raises(ValueError):
        evaluate_postfix(tokens)


def test_evaluate_postfix_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate_postfix(["1", "0", "/"])


def test_postfix_pairs_with_the_stack_exercise():
    """`dsa.stack.infix_to_postfix` and this function are the two halves of a
    calculator that never builds a tree."""
    from dsa.stack import infix_to_postfix

    assert evaluate_postfix(infix_to_postfix(tokenize("3 + 4 * 2"))) == 11


# -- stage 2b: the parser -------------------------------------------------


def parse(text):
    return Parser(tokenize(text)).parse()


def test_parse_single_number():
    assert parse("3") == Num(3.0)


def test_parse_flat_expression():
    assert parse("3 + 4") == BinOp("+", Num(3.0), Num(4.0))


def test_precedence_is_the_shape_of_the_tree():
    """"*" binds tighter, so it must sit *deeper* than "+" — that is how the
    grammar encodes precedence, with no table of numbers anywhere."""
    assert parse("3 + 4 * 2") == BinOp("+", Num(3.0), BinOp("*", Num(4.0), Num(2.0)))


def test_parentheses_override_precedence():
    assert parse("(3 + 4) * 2") == BinOp("*", BinOp("+", Num(3.0), Num(4.0)), Num(2.0))


def test_subtraction_is_left_associative():
    """1 - 2 - 3 is (1 - 2) - 3 = -4, not 1 - (2 - 3) = 2. Building this
    right-associatively is the most common recursive-descent bug."""
    assert parse("1 - 2 - 3") == BinOp("-", BinOp("-", Num(1.0), Num(2.0)), Num(3.0))


def test_division_is_left_associative():
    assert parse("8 / 4 / 2") == BinOp("/", BinOp("/", Num(8.0), Num(4.0)), Num(2.0))


def test_unary_minus():
    assert parse("-5") == BinOp("-", Num(0.0), Num(5.0))


def test_nested_parentheses():
    assert parse("((7))") == Num(7.0)


@pytest.mark.parametrize("text", ["", "3 +", "(3 + 4", "3 + 4 )", "* 3", "()"])
def test_parser_rejects_malformed_input(text):
    with pytest.raises(ValueError):
        parse(text)


# -- stage 3: walking the tree --------------------------------------------


def test_evaluate_a_leaf():
    assert evaluate(Num(3.0)) == 3.0


def test_evaluate_a_hand_built_tree():
    """No parser involved — evaluate works on any tree of the right shape."""
    assert evaluate(BinOp("+", Num(1.0), BinOp("*", Num(2.0), Num(3.0)))) == 7.0


def test_evaluate_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate(BinOp("/", Num(1.0), Num(0.0)))


def test_evaluate_rejects_unknown_operator():
    with pytest.raises(ValueError):
        evaluate(BinOp("^", Num(2.0), Num(3.0)))


# -- end to end -----------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        ("3", 3.0),
        ("3 + 4", 7.0),
        ("3 + 4 * 2", 11.0),
        ("(3 + 4) * 2", 14.0),
        ("-5 + 2", -3.0),
        ("1 - 2 - 3", -4.0),
        ("8 / 4 / 2", 1.0),
        ("2 * (3 + (4 - 1))", 12.0),
        ("10 / 4", 2.5),
    ],
)
def test_calculate(text, expected):
    assert calculate(text) == pytest.approx(expected)


def test_both_routes_agree():
    """The tree route and the stack route are two ways to the same answer —
    which is the point of the whole module."""
    from dsa.stack import infix_to_postfix

    for text in ["3 + 4 * 2", "(3 + 4) * 2", "1 - 2 - 3", "8 / 4 / 2"]:
        tokens = tokenize(text)
        assert calculate(text) == pytest.approx(evaluate_postfix(infix_to_postfix(tokens)))


# -- the bridge to viz ----------------------------------------------------


def test_to_edges_keeps_duplicate_values_apart():
    """Given to you. "2 + 2" has two distinct leaves that happen to share a
    label, so the ids must differ or the drawing collapses them into one."""
    edges = to_edges(parse("2 + 2"))
    assert len(edges) == 2
    children = [child for _, child in edges]
    assert len(set(children)) == 2
    assert all(child.split("#")[0] == "2.0" for child in children)


def test_to_edges_of_a_leaf_is_empty():
    assert to_edges(Num(3.0)) == []
