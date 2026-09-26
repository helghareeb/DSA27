"""Generate the figures for Lecture 15 — The principles of language translation.

Run it from the repository root:

    python tools/figures_l15.py                            # uses YOUR dsa/translation.py
    python tools/with_solutions.py tools/figures_l15.py    # uses solutions/

Same conventions as `tools/figures.py`. Every tree in these figures is the tree
the parser actually builds: the script parses the expression with
`dsa.translation` and draws the result, so it needs a working implementation
(the lecture's copies were made from the instructor's reference solution). The
measured figure times the three stages and the stack route, and records the
real depth of the Python call stack while parsing and evaluating.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import figures as base  # palette, rcParams, save()

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

base.OUT = ROOT / "docs" / "lectures" / "15-language-translation" / "figures"

SLATE, AMBER, MUTED = base.SLATE, base.AMBER, base.MUTED
FILL, HILITE, DONE = base.FILL, base.HILITE, base.DONE
RED = "#C1443C"
GREEN = "#4C9F70"
PURPLE = "#7A5195"
GREY = "#D6D6D6"
PINK = "#F6C9C4"


# -- drawing helpers ----------------------------------------------------------


def box(ax, x, y, text, fill=FILL, w=1.0, h=0.6, fontsize=11, colour=SLATE,
        family=None, round_=False, lw=1.2):
    style = "round,pad=0.02,rounding_size=0.08" if round_ else "square,pad=0"
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, facecolor=fill,
                                edgecolor=SLATE, linewidth=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=colour, family=family)


def arrow(ax, start, end, colour=SLATE, rad=0.0, lw=1.4):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11,
                                 color=colour, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def title(ax, text, size=12.5):
    ax.set_title(text, fontsize=size, fontweight="bold", color=SLATE, pad=6)


def number_text(value):
    """3.0 -> "3", 2.5 -> "2.5": what a person would write."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def parse(text):
    from dsa.translation import Parser, tokenize
    return Parser(tokenize(text)).parse()


def layout(node):
    """Positions for a tree: x is the in-order rank, y is minus the depth."""
    from dsa.translation import BinOp

    pos = {}
    rank = [0]

    def walk(current, depth):
        if isinstance(current, BinOp):
            walk(current.left, depth + 1)
        pos[id(current)] = (rank[0], -depth)
        rank[0] += 1
        if isinstance(current, BinOp):
            walk(current.right, depth + 1)

    walk(node, 0)
    return pos


def draw_ast(ax, node, x0=0.0, y0=0.0, sx=0.9, sy=1.0, r=0.32, fills=None,
             labels=None, notes=None, fontsize=12):
    """Draw an AST with matplotlib. Returns the bounding box (xmin, xmax, ymin)."""
    from dsa.translation import BinOp

    pos = layout(node)
    fills = fills or {}
    labels = labels or {}
    notes = notes or {}

    def xy(n):
        x, y = pos[id(n)]
        return x0 + x * sx, y0 + y * sy

    def edges(current):
        if isinstance(current, BinOp):
            for child in (current.left, current.right):
                (x1, y1), (x2, y2) = xy(current), xy(child)
                ax.plot([x1, x2], [y1, y2], color=SLATE, linewidth=1.3, zorder=1)
                edges(child)

    def nodes(current):
        x, y = xy(current)
        is_op = isinstance(current, BinOp)
        fill = fills.get(id(current), HILITE if is_op else FILL)
        ax.add_patch(Circle((x, y), r, facecolor=fill, edgecolor=SLATE, linewidth=1.3,
                            zorder=2))
        text = labels.get(id(current),
                          current.op if is_op else number_text(current.value))
        ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, color=SLATE,
                zorder=3, fontweight="bold" if is_op else None)
        if id(current) in notes:
            note, colour = notes[id(current)]
            ax.text(x, y - r - 0.06, note, ha="center", va="top",
                    fontsize=9, color=colour, zorder=3)
        if is_op:
            nodes(current.left)
            nodes(current.right)

    edges(node)
    nodes(node)
    xs = [x0 + p[0] * sx for p in pos.values()]
    ys = [y0 + p[1] * sy for p in pos.values()]
    return min(xs), max(xs), min(ys)


def post_order(node):
    from dsa.translation import BinOp
    out = []

    def walk(current):
        if isinstance(current, BinOp):
            walk(current.left)
            walk(current.right)
        out.append(current)

    walk(node)
    return out


# -- the pipeline -------------------------------------------------------------


def figure_pipeline():
    from dsa.translation import evaluate, tokenize

    text = "3 + 4 * 2"
    tokens = tokenize(text)
    tree = parse(text)
    value = evaluate(tree)

    fig, ax = plt.subplots(figsize=(11.2, 3.9))
    # stage boxes
    box(ax, 0.0, 1.2, f'"{text}"', fill="white", w=2.1, h=0.8, fontsize=12,
        family="monospace", round_=True)
    ax.text(1.05, 2.25, "source text", ha="center", fontsize=10, color=MUTED)

    x = 3.2
    for i, t in enumerate(tokens):
        box(ax, x + i * 0.52, 1.3, t, fill=FILL, w=0.52, h=0.6, fontsize=11.5,
            family="monospace")
    ax.text(x + 1.3, 2.25, "tokens", ha="center", fontsize=10, color=MUTED)

    draw_ast(ax, tree, x0=6.95, y0=2.05, sx=0.62, sy=0.78, r=0.25, fontsize=11)
    ax.text(8.2, 2.5, "tree (AST)", ha="center", fontsize=10, color=MUTED)

    box(ax, 10.3, 1.2, number_text(value), fill=DONE, w=1.1, h=0.8, fontsize=14,
        round_=True)
    ax.text(10.85, 2.25, "value", ha="center", fontsize=10, color=MUTED)

    arrow(ax, (2.2, 1.6), (3.1, 1.6), colour=AMBER, lw=1.8)
    arrow(ax, (5.9, 1.6), (6.75, 1.6), colour=AMBER, lw=1.8)
    arrow(ax, (9.55, 1.6), (10.2, 1.6), colour=AMBER, lw=1.8)
    for cx, name, sub in [(2.65, "tokenize", "lexer · text → tokens"),
                          (6.32, "parse", "parser · tokens → tree"),
                          (9.87, "evaluate", "evaluator · tree → value")]:
        ax.text(cx, -0.1, name, ha="center", fontsize=10.5, color=AMBER,
                fontweight="bold", family="monospace")
        ax.text(cx, -0.45, sub, ha="center", fontsize=8.8, color=SLATE)
    ax.text(5.7, -1.1, "calculate(text) = evaluate(Parser(tokenize(text)).parse())",
            ha="center", fontsize=10.5, color=SLATE, family="monospace")
    clean(ax, (-0.2, 11.6), (-1.35, 2.7))
    title(ax, "Every translator: text → tokens → tree → value (or code)")
    return base.save(fig, "pipeline")


def figure_tokenize():
    from dsa.translation import tokenize

    text = "12 * (3.5+4)"
    tokens = tokenize(text)
    fig, ax = plt.subplots(figsize=(10.4, 3.4))
    w = 0.62
    # characters
    for i, ch in enumerate(text):
        fill = "white" if ch == " " else FILL
        box(ax, i * w, 1.2, "␣" if ch == " " else ch, fill=fill, w=w, h=0.6,
            fontsize=12, family="monospace", colour=MUTED if ch == " " else SLATE)
        ax.text(i * w + w / 2, 1.08, str(i), ha="center", va="top", fontsize=7.5,
                color=MUTED)
    ax.text(-0.25, 1.5, "characters", ha="right", va="center", fontsize=10, color=MUTED)
    # group the characters into tokens
    i = 0
    colours = [HILITE, DONE]
    k = 0
    starts = []
    for t in tokens:
        while text[i] == " ":
            i += 1
        start = i
        i += len(t)
        starts.append((start, i, t))
    for n, (a, b, t) in enumerate(starts):
        colour = colours[n % 2]
        x1, x2 = a * w + 0.05, b * w - 0.05
        ax.plot([x1, x1, x2, x2], [0.95, 0.85, 0.85, 0.95], color=SLATE, linewidth=1.0)
        box(ax, (x1 + x2) / 2 - max(0.28, (x2 - x1) / 2), -0.05, t, fill=colour,
            w=max(0.56, x2 - x1), h=0.55, fontsize=11.5, family="monospace")
    ax.text(-0.25, 0.22, "tokens", ha="right", va="center", fontsize=10, color=MUTED)
    ax.text(len(text) * w + 0.3, 1.5, "a space separates,\nbut is never a token",
            va="center", fontsize=9.5, color=MUTED)
    ax.text(len(text) * w + 0.3, 0.22, "12 and 3.5 stay whole:\nkeep reading while\n"
            "the next character\nis a digit or '.'", va="center", fontsize=9.5,
            color=SLATE)
    ax.text(0, -0.55, f"tokenize({text!r}) → {tokens}", fontsize=10,
            family="monospace", color=SLATE)
    clean(ax, (-1.8, 10.6), (-0.8, 2.0))
    title(ax, "The lexer groups characters into tokens — one left-to-right pass, O(n)")
    return base.save(fig, "tokenize")


# -- precedence and associativity ---------------------------------------------


def figure_precedence():
    from dsa.translation import evaluate

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.9))
    for ax, text in zip(axes, ["3 + 4 * 2", "(3 + 4) * 2"]):
        tree = parse(text)
        draw_ast(ax, tree, sx=0.95, sy=1.05, r=0.33)
        ax.text(2.0, -2.75, f"{text}  =  {number_text(evaluate(tree))}", ha="center",
                fontsize=12, family="monospace", color=SLATE)
        clean(ax, (-0.6, 4.6), (-3.1, 0.6))
    axes[0].text(3.3, -0.95, "* is deeper:\nit is evaluated\nfirst", fontsize=9.5,
                 color=AMBER, ha="left")
    axes[1].text(-0.55, -0.95, "the parentheses\nput + deeper", fontsize=9.5,
                 color=AMBER, ha="left")
    fig.suptitle("Precedence is not stored anywhere: it is the shape of the tree",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "precedence")


def figure_associativity():
    from dsa.translation import BinOp, Num, evaluate

    right = BinOp("-", Num(1.0), BinOp("-", Num(2.0), Num(3.0)))
    left = parse("1 - 2 - 3")
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.9))
    for ax, tree, head, colour, mark in [
        (axes[0], left, "left-associative — correct", GREEN, "(1 − 2) − 3 = "),
        (axes[1], right, "right-associative — wrong", RED, "1 − (2 − 3) = "),
    ]:
        draw_ast(ax, tree, sx=0.95, sy=1.05, r=0.33,
                 fills={id(tree): DONE if colour == GREEN else PINK})
        ax.text(2.0, -2.75, mark + number_text(evaluate(tree)), ha="center",
                fontsize=12, color=colour, fontweight="bold")
        ax.set_title(head, fontsize=11.5, color=colour, pad=4)
        clean(ax, (-0.6, 4.6), (-3.1, 0.6))
    fig.suptitle("1 − 2 − 3: two trees, two answers. The grammar must build the left one",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    return base.save(fig, "associativity")


def figure_expr_loop():
    """Snapshots of `node` in Parser.expr for "1 - 2 - 3 + 4"."""
    from dsa.translation import BinOp, Num

    a = Num(1.0)
    b = BinOp("-", a, Num(2.0))
    c = BinOp("-", b, Num(3.0))
    d = BinOp("+", c, Num(4.0))
    snaps = [(a, "first: node = self.term()", "1"),
             (b, "'-' seen: node = BinOp('-',\n      node, term())", "1 - 2"),
             (c, "'-' seen: node = BinOp('-',\n      node, term())", "1 - 2 - 3"),
             (d, "'+' seen: node = BinOp('+',\n      node, term())", "1 - 2 - 3 + 4")]
    fig, ax = plt.subplots(figsize=(12.4, 4.1))
    x0 = 0.0
    for k, (tree, caption, consumed) in enumerate(snaps):
        fills = {id(tree): HILITE} if k else {id(tree): FILL}
        if k:                                   # the old tree, now the LEFT child
            for n in post_order(tree.left):
                fills[id(n)] = DONE
        draw_ast(ax, tree, x0=x0, sx=0.62, sy=0.8, r=0.24, fills=fills, fontsize=10.5)
        width = 0.62 * 2 * k
        centre = x0 + width / 2
        ax.text(centre, 0.55, f"after {consumed!r}", ha="center", fontsize=10,
                color=SLATE)
        ax.text(centre, -3.05, caption.replace(": ", ":\n"), ha="center", va="top",
                fontsize=8.3, color=AMBER, family="monospace", multialignment="center")
        x0 += width + (3.9 if k == 0 else 3.0)
    clean(ax, (-1.4, x0 - 0.8), (-3.75, 0.9))
    title(ax, "Parser.expr's loop: the tree so far becomes the LEFT child — "
              "so the tree leans left")
    return base.save(fig, "expr-loop")


# -- recursive descent --------------------------------------------------------


def figure_calls():
    """The call tree of the parser on "3 + 4 * 2", traced from the real code."""
    from dsa.translation import Parser, tokenize

    # record every call and return of expr/term/factor, with the tokens consumed
    events = []

    class Traced(Parser):
        def expr(self):
            events.append(("call", "expr", self.position))
            r = super().expr()
            events.append(("ret", "expr", self.position))
            return r

        def term(self):
            events.append(("call", "term", self.position))
            r = super().term()
            events.append(("ret", "term", self.position))
            return r

        def factor(self):
            events.append(("call", "factor", self.position))
            r = super().factor()
            events.append(("ret", "factor", self.position))
            return r

    tokens = tokenize("3 + 4 * 2")
    Traced(tokens).parse()

    # rebuild the call tree: children are calls and the operator tokens between
    class Call:
        def __init__(self, name, start):
            self.name, self.start, self.kids = name, start, []

    root = None
    stack = []
    for kind, name, position in events:
        if kind == "call":
            call = Call(name, position)
            if stack:
                parent = stack[-1]
                # operator tokens consumed by the parent loop before this call
                last = parent.kids[-1].end if parent.kids and isinstance(parent.kids[-1], Call) else parent.start
                for p in range(last, position):
                    parent.kids.append(("tok", tokens[p]))
                parent.kids.append(call)
            else:
                root = call
            stack.append(call)
        else:
            call = stack.pop()
            call.end = position
            if call.name == "factor":
                call.kids.append(("tok", tokens[call.start]))

    # layout: leaves (tokens) left to right, parents centred over children
    positions = {}
    counter = [0]

    def place(item, depth):
        if isinstance(item, tuple):
            x = counter[0]
            counter[0] += 1
            positions[id(item)] = (x, -depth)
            return x
        xs = [place(k, depth + 1) for k in item.kids]
        x = sum(xs) / len(xs)
        positions[id(item)] = (x, -depth)
        return x

    place(root, 0)
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    sx, sy = 1.25, 0.95

    def draw(item):
        x, y = positions[id(item)]
        x, y = x * sx, y * sy
        if isinstance(item, tuple):
            token = item[1]
            fill = HILITE if token in "+-*/" else FILL
            box(ax, x - 0.3, y - 0.25, token, fill=fill, w=0.6, h=0.5, fontsize=12,
                family="monospace")
            return
        box(ax, x - 0.5, y - 0.22, item.name, fill="white", w=1.0, h=0.44,
            fontsize=10.5, family="monospace", round_=True)
        for k in item.kids:
            kx, ky = positions[id(k)]
            ax.plot([x, kx * sx], [y - 0.22, ky * sy + 0.25], color=MUTED,
                    linewidth=1.1, zorder=0)
            draw(k)

    draw(root)
    ymin = min(p[1] for p in positions.values()) * sy
    ax.text(counter[0] * sx + 0.1, -0.2, "expr   := term (('+' | '-') term)*\n"
            "term   := factor (('*' | '/') factor)*\n"
            "factor := NUMBER | '(' expr ')' | '-' factor",
            fontsize=9.5, family="monospace", color=SLATE, va="top")
    ax.text(counter[0] * sx + 0.1, -2.2, "each box is one call —\n"
            "a frame on the call stack.\nThe deepest path is the\n"
            "deepest the stack grows.", fontsize=9.5, color=AMBER, va="top")
    clean(ax, (-0.8, counter[0] * sx + 5.4), (ymin - 0.5, 0.5))
    title(ax, "Recursive descent on 3 + 4 * 2: the calls form a tree (the parse tree)")
    return base.save(fig, "calls")


def figure_evaluate():
    """Post-order evaluation of (3 + 4) * (5 - 2): visit order and values."""
    from dsa.translation import BinOp, evaluate

    text = "(3 + 4) * (5 - 2)"
    tree = parse(text)
    order = post_order(tree)
    notes = {}
    for k, n in enumerate(order, start=1):
        v = evaluate(n)
        colour = GREEN if isinstance(n, BinOp) else MUTED
        notes[id(n)] = (f"#{k}  = {number_text(v)}", colour)
    fig, ax = plt.subplots(figsize=(9.6, 4.3))
    draw_ast(ax, tree, sx=1.2, sy=1.15, r=0.33, notes=notes)
    postfix = " ".join(n.op if isinstance(n, BinOp) else number_text(n.value)
                       for n in order)
    ax.text(3.6, -3.3, f"visited in post-order:   {postfix}", ha="center",
            fontsize=12, family="monospace", color=SLATE)
    ax.text(3.6, -3.8, "— exactly the postfix form of Lecture 06", ha="center",
            fontsize=10.5, color=AMBER)
    ax.text(7.6, 0.0, "evaluate(node):\n  a leaf → its value\n  else: left value,\n"
            "        right value,\n        then apply op", fontsize=9.5,
            family="monospace", color=SLATE, va="top")
    clean(ax, (-0.6, 10.2), (-4.1, 0.7))
    title(ax, f"evaluate({text}): children first, then the node — post-order")
    return base.save(fig, "evaluate")


def figure_two_routes():
    fig, ax = plt.subplots(figsize=(11.0, 4.1))
    box(ax, 0.0, 1.55, "tokens", fill=FILL, w=1.6, h=0.7, fontsize=11.5, round_=True)
    # upper route: stack
    box(ax, 2.6, 2.75, "infix_to_postfix\n(shunting-yard, Week 6)", fill="white", w=3.0,
        h=0.85, fontsize=9.5, round_=True)
    box(ax, 6.4, 2.75, "evaluate_postfix\n(one stack)", fill="white", w=2.6, h=0.85,
        fontsize=9.5, round_=True)
    ax.text(6.0, 3.85, "the stack route — no tree is ever built", ha="center",
            fontsize=10, color=PURPLE, fontweight="bold")
    # lower route: tree
    box(ax, 2.6, 0.2, "Parser.parse\n(recursive descent)", fill="white", w=3.0, h=0.85,
        fontsize=9.5, round_=True)
    box(ax, 6.4, 0.2, "evaluate\n(post-order walk)", fill="white", w=2.6, h=0.85,
        fontsize=9.5, round_=True)
    ax.text(6.0, -0.35, "the tree route — Week 15", ha="center", fontsize=10,
            color=GREEN, fontweight="bold")
    box(ax, 9.9, 1.55, "value", fill=DONE, w=1.2, h=0.7, fontsize=11.5, round_=True)
    arrow(ax, (1.6, 2.1), (2.55, 3.1), colour=PURPLE)
    arrow(ax, (5.6, 3.17), (6.35, 3.17), colour=PURPLE)
    ax.text(5.98, 3.3, "postfix", ha="center", fontsize=8.5, color=PURPLE)
    arrow(ax, (9.0, 3.1), (9.95, 2.25), colour=PURPLE)
    arrow(ax, (1.6, 1.7), (2.55, 0.7), colour=GREEN)
    arrow(ax, (5.6, 0.62), (6.35, 0.62), colour=GREEN)
    ax.text(5.98, 0.75, "AST", ha="center", fontsize=8.5, color=GREEN)
    arrow(ax, (9.0, 0.7), (9.95, 1.6), colour=GREEN)
    ax.text(6.0, 1.9, "post-order of the tree  =  the postfix list", ha="center",
            fontsize=10, color=SLATE, style="italic")
    clean(ax, (-0.2, 11.3), (-0.6, 4.1))
    title(ax, "Two routes from tokens to a value — same answer, both O(n)")
    return base.save(fig, "two-routes")


# -- measured -----------------------------------------------------------------


def balanced(n_leaves, rng):
    """A fully parenthesised, balanced expression with n_leaves numbers."""
    ops = "+-*"
    parts = [str(rng.randint(1, 9)) for _ in range(n_leaves)]
    while len(parts) > 1:
        merged = []
        for i in range(0, len(parts) - 1, 2):
            merged.append(f"({parts[i]} {rng.choice(ops)} {parts[i + 1]})")
        if len(parts) % 2:
            merged.append(parts[-1])
        parts = merged
    return parts[0]


def peak_depth(func):
    """Run func() and return the deepest Python call stack it reached."""
    depth = [0]
    best = [0]

    def tracer(frame, event, arg):
        if event == "call":
            depth[0] += 1
            best[0] = max(best[0], depth[0])
        elif event == "return":
            depth[0] -= 1
        return tracer

    sys.setprofile(tracer)
    try:
        func()
    finally:
        sys.setprofile(None)
    return best[0]


def best_time(func, loops, repeat=7):
    """Seconds per call: the best of `repeat` runs of `loops` calls each.

    Several calls per run smooth out timer noise on the small sizes; keeping
    the minimum discards runs slowed down by something else on the machine.
    """
    import gc
    import time

    best = float("inf")
    for _ in range(repeat):
        gc.collect()
        start = time.perf_counter()
        for _ in range(loops):
            func()
        best = min(best, (time.perf_counter() - start) / loops)
    return best


def figure_measured():
    from dsa import translation
    from dsa.stack import infix_to_postfix
    try:
        translation.calculate("1 + 2")
        infix_to_postfix(["1", "+", "2"])
    except NotImplementedError:
        print("  (skipped measured.png: dsa/translation.py is not implemented yet)")
        return None

    rng = random.Random(15)
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.7))

    # left: time, on balanced expressions (shallow trees, no recursion limit)
    ax = axes[0]
    leaves = [2 ** k for k in range(6, 14)]
    texts = {n: balanced(n, rng) for n in leaves}
    token_lists = {n: translation.tokenize(texts[n]) for n in leaves}
    trees = {n: translation.Parser(token_lists[n]).parse() for n in leaves}
    ntok = [len(token_lists[n]) for n in leaves]
    series = [
        ("tokenize", lambda n: translation.tokenize(texts[n]), AMBER),
        ("parse", lambda n: translation.Parser(token_lists[n]).parse(), PURPLE),
        ("evaluate", lambda n: translation.evaluate(trees[n]), GREEN),
        ("stack route: infix_to_postfix + evaluate_postfix",
         lambda n: translation.evaluate_postfix(infix_to_postfix(token_lists[n])), RED),
        ("calculate (all three stages)", lambda n: translation.calculate(texts[n]), SLATE),
    ]
    printed = {}
    for label, run, colour in series:
        seconds = [best_time(lambda n=n, run=run: run(n), loops=max(1, 20_000 // n))
                   for n in leaves]
        ax.plot(ntok, [s * 1e3 for s in seconds], "o-", color=colour, label=label,
                linewidth=2.0, markersize=4.5)
        printed[label] = [round(s * 1e3, 3) for s in seconds]
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("tokens in the expression (log scale)")
    ax.set_ylabel("milliseconds (log scale)")
    ax.set_title("time: every stage is a straight line of slope 1 — O(n)",
                 fontsize=11, color=SLATE)
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    # right: depth of the call stack against the shape of the input
    ax = axes[1]
    depths = {"nested": [], "flat": [], "balanced": []}
    xs = [8, 16, 32, 64, 128, 256]
    for k in xs:
        nested = "(" * k + "1" + ")" * k
        flat = " + ".join(["1"] * k)
        bal = balanced(k, rng)
        depths["nested"].append(peak_depth(lambda: translation.calculate(nested)))
        depths["flat"].append(peak_depth(lambda: translation.calculate(flat)))
        depths["balanced"].append(peak_depth(lambda: translation.calculate(bal)))
    ax.plot(xs, depths["nested"], "o-", color=RED, linewidth=2.0, markersize=4.5,
            label="((( … 1 … ))) — k pairs of parentheses")
    ax.plot(xs, depths["flat"], "o-", color=AMBER, linewidth=2.0, markersize=4.5,
            label="1 + 1 + … + 1 — k numbers")
    ax.plot(xs, depths["balanced"], "o-", color=GREEN, linewidth=2.0, markersize=4.5,
            label="balanced ((1 + 2) * (3 - 4)) … — k numbers")
    limit = sys.getrecursionlimit()
    ax.axhline(limit, color=MUTED, linestyle="--", linewidth=1.2)
    ax.text(8, limit * 1.12, f"Python's default recursion limit: {limit} frames",
            fontsize=8.5, color=MUTED)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_ylim(4, 4000)
    ax.set_xlabel("k (log scale)")
    ax.set_ylabel("deepest Python call stack (frames, log scale)")
    ax.set_title("recursion depth follows the shape, not the length",
                 fontsize=11, color=SLATE)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    for ax in axes:
        ax.grid(True, alpha=0.25, linewidth=0.7)
        for side in ("right", "top"):
            ax.spines[side].set_visible(False)
    fig.suptitle("Measured: linear time, and a depth set by the tree's height",
                 fontsize=12.5, fontweight="bold", color=SLATE)
    fig.tight_layout()
    print("    tokens      ", ntok)
    for label, values in printed.items():
        print(f"    {label[:30]:30s}", values)
    print("    k           ", xs)
    for key, values in depths.items():
        print(f"    depth {key:9s}", values)
    return base.save(fig, "measured")


# -- the course, in one picture -----------------------------------------------


def figure_retrospective():
    weeks = [
        (1, "Why this\ncourse", "ADT vs\nstructure"), (2, "Complexity,\nthe Array", "Parser.tokens\nis an Array"),
        (3, "Recursion", "expr, term,\nfactor, evaluate"), (4, "Dynamic\narray", "under Stack"),
        (5, "Linked\nlists", "nodes and\nreferences"), (6, "Stacks", "evaluate_postfix,\nshunting-yard"),
        (7, "Queues", "level-order\nof an AST"), (8, "Searching", ""),
        (9, "Basic\nsorting", ""), (10, "Advanced\nsorting", ""),
        (11, "Trees", "the AST;\npost-order"), (12, "Heaps", ""),
        (13, "Hash\ntables", "a symbol\ntable (SWE141)"), (14, "Graphs", "call graph;\ndependencies"),
        (15, "Language\ntranslation", "all of them"),
    ]
    used = {2, 3, 4, 5, 6, 11}
    fig, ax = plt.subplots(figsize=(11.0, 6.0))
    w, h, gap, row_gap = 1.9, 1.0, 0.18, 1.85
    for i, (n, name, use) in enumerate(weeks):
        r, c = divmod(i, 5)
        x = c * (w + gap)
        y = -r * row_gap
        if n == 15:
            fill = DONE
        elif n in used:
            fill = HILITE
        else:
            fill = FILL
        box(ax, x, y, f"{n}\n{name}", fill=fill, w=w, h=h, fontsize=9, round_=True)
        if use:
            ax.text(x + w / 2, y - 0.08, use, ha="center", va="top", fontsize=8,
                    color=AMBER if n in used else MUTED)
    ly = -2 * row_gap - 1.25
    ax.add_patch(Rectangle((0.0, ly), 0.3, 0.3, facecolor=HILITE, edgecolor=SLATE))
    ax.text(0.45, ly + 0.15, "used directly by dsa/translation.py", fontsize=9,
            va="center", color=SLATE)
    ax.add_patch(Rectangle((5.0, ly), 0.3, 0.3, facecolor=FILL, edgecolor=SLATE))
    ax.text(5.45, ly + 0.15, "the same ideas, one step further away", fontsize=9,
            va="center", color=SLATE)
    clean(ax, (-0.2, 5 * (w + gap)), (ly - 0.3, 1.2))
    title(ax, "Fifteen weeks, one program: what the calculator stands on")
    return base.save(fig, "retrospective")


FIGURES = [figure_pipeline, figure_tokenize, figure_precedence, figure_associativity,
           figure_expr_loop, figure_calls, figure_evaluate, figure_two_routes,
           figure_measured, figure_retrospective]


def main():
    print(f"Generating {len(FIGURES)} figures into {base.OUT.relative_to(ROOT)}")
    for builder in FIGURES:
        try:
            builder()
        except NotImplementedError:
            print(f"  (skipped {builder.__name__}: dsa/translation.py is not implemented yet)")
    print("Done.")


if __name__ == "__main__":
    main()
