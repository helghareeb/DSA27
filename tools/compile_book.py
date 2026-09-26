#!/usr/bin/env python3
"""Assemble the three compiled documents from the course Markdown.

    python tools/compile_book.py book            -> build/book.md
    python tools/compile_book.py lab-manual      -> build/lab-manual.md
    python tools/compile_book.py lab-manual-ta   -> build/lab-manual-ta.md

`tools/build.py book` (etc.) runs this and then pandoc. Nothing here is written
by hand twice: every chapter is a file in docs/, with its YAML stripped, its
headings pushed down a level or two, its image paths made relative to the
repository root, and its links to other Markdown files reduced to their text
(a link to a .md file means nothing on paper).

book           The students' book. Course guide and study plan; then, for each
               of the fifteen weeks, the lecture handout followed by that week's
               question bank; then the answers to every week's questions, and the
               practice papers.
lab-manual     Students' edition. Labs 1–15, with every `# Answers to the
               checkpoints` section and every `::: {.ta-only}` block removed
               (the second by tools/strip-ta-only.lua at build time).
lab-manual-ta  TAs' edition. The TA guide, labs 1–15 complete with the checkpoint
               answers and TA-only notes, and the reference solutions to every
               lab exercise as an appendix.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BUILD = ROOT / "build"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import LABS, LECTURES  # noqa: E402

AUTHOR = "Dr. Haitham A. El-Ghareeb"
INSTITUTE = "Faculty of Computers and Information Sciences, Mansoura University"
TERM = "Fall 2026"

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})(\s)")
IMAGE = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)")
LINK = re.compile(r"(?<![!\\])\[((?:[^\[\]]|\[[^\[\]]*\])+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


# ------------------------------------------------------------- helpers ----
def split_yaml(text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r'^(\w[\w-]*):\s*"?(.*?)"?\s*$', line)
                if m:
                    meta[m.group(1)] = m.group(2)
            text = text[end + 4:]
    return meta, text.lstrip("\n")


def _rewrite_link(m: re.Match, src: Path) -> str:
    text, target = m.group(1), m.group(2)
    if re.match(r"^(https?:|mailto:)", target):
        return m.group(0)
    return text


def transform(text: str, src: Path, shift: int) -> str:
    """Shift headings, fix image paths, flatten local links — outside code only."""
    out = []
    in_code = False
    fence = ""
    for line in text.splitlines():
        f = FENCE.match(line)
        if f:
            if not in_code:
                in_code, fence = True, f.group(1)
            elif f.group(1) == fence:
                in_code = False
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        h = HEADING.match(line)
        if h and shift:
            level = min(len(h.group(1)) + shift, 6)
            line = "#" * level + line[len(h.group(1)):]
        line = IMAGE.sub(lambda m: m.group(1) + _image_path(m.group(2), src), line)
        line = LINK.sub(lambda m: _rewrite_link(m, src), line)
        out.append(line)
    return "\n".join(out) + "\n"


def _image_path(p: str, src: Path) -> str:
    if re.match(r"^(https?:|/)", p):
        return p
    return (src.parent / p).resolve().relative_to(ROOT).as_posix()


# In the book, questions and answers are no longer separate files.
BOOK_EDITS = [
    (re.compile(r"\*\*Answers are in a separate file:\*\*\s*\[`week(\d+)-answers\.md`\]\([^)]*\)\."),
     lambda m: f"**The answers are at the back of the book,** in *Answers — Week {int(m.group(1))}*."),
    (re.compile(r"\*\*Questions:\*\*\s*\[`week(\d+)-questions\.md`\]\([^)]*\)\."),
     lambda m: f"**The questions** are at the end of the *Week {int(m.group(1))}* chapter."),
    (re.compile(r"`week(\d+)-answers\.md`"), lambda m: f"*Answers — Week {int(m.group(1))}*"),
    (re.compile(r"`week(\d+)-questions\.md`"), lambda m: f"the *Week {int(m.group(1))}* questions"),
]


def include(path: Path, shift: int, drop_from: str | None = None,
            edits: list | None = None) -> str:
    meta, body = split_yaml(path.read_text(encoding="utf-8"))
    for pat, rep in edits or []:
        body = pat.sub(rep, body)
    if drop_from:
        m = re.search(rf"^{re.escape(drop_from)}\s*$", body, re.M)
        if m:
            body = body[:m.start()]
    return transform(body, path, shift)


def title_of(path: Path) -> str:
    meta, _ = split_yaml(path.read_text(encoding="utf-8"))
    return meta.get("title", path.stem)


def latex(s: str) -> str:
    return f"\n```{{=latex}}\n{s}\n```\n\n"


def titlepage(title: str, subtitle: str, edition: str) -> str:
    return latex(rf"""\begin{{titlepage}}
\thispagestyle{{empty}}
\begingroup\color{{dsaslate}}
\vspace*{{3.2cm}}
{{\fontsize{{14}}{{16}}\selectfont\color{{dsaamber}}DSA27 \textperiodcentered{{}} CS2101 \textperiodcentered{{}} IS122\par}}
\vspace{{0.6cm}}
{{\raggedright\hyphenpenalty=10000\fontsize{{32}}{{38}}\selectfont\bfseries {title}\par}}
\vspace{{0.5cm}}
{{\Large {subtitle}\par}}
\vspace{{0.4cm}}
{{\color{{dsaamber}}\rule{{\linewidth}}{{1.2pt}}}}\par
\vspace{{0.4cm}}
{{\large\bfseries {edition}\par}}
\vfill
{{\large {AUTHOR}\par}}
\vspace{{0.2cm}}
{{\normalsize\color{{dsamuted}} {INSTITUTE}\par}}
\vspace{{0.2cm}}
{{\normalsize\color{{dsamuted}} {TERM}\par}}
\endgroup
\end{{titlepage}}
\tableofcontents
\clearpage""")


def chapter(title: str) -> str:
    return f"\n# {title}\n\n"


def part(title: str) -> str:
    return latex(rf"\part{{{title}}}")


def yaml(title: str) -> str:
    # title-meta sets the PDF metadata without pandoc's own \maketitle.
    return f'---\ntitle-meta: "{title}"\nauthor-meta: "{AUTHOR}"\nlang: en\n---\n\n'


# ---------------------------------------------------------------- book ----
def book() -> str:
    parts = [yaml("DSA27 — Data Structures and Algorithms"),
             titlepage("Data Structures and Algorithms",
                       "Lectures, question bank and worked answers",
                       "The students' book")]
    parts.append(chapter("How to use this book"))
    parts.append((ROOT / "tools/templates/book-preface.md").read_text(encoding="utf-8"))

    parts.append(part("The course"))
    parts.append(chapter("Course guide"))
    parts.append(include(DOCS / "course/00-course-guide.md", 1))
    parts.append(chapter("Study plan"))
    parts.append(include(DOCS / "course/01-study-plan.md", 1))

    parts.append(part("Fifteen weeks"))
    for n, slug in LECTURES.items():
        lec = DOCS / "lectures" / slug / "lecture.md"
        q = DOCS / "question-bank" / f"week{n:02d}-questions.md"
        if not lec.exists():
            continue
        parts.append(chapter(f"Week {n} — {title_of(lec)}"))
        parts.append(include(lec, 1))
        if q.exists():
            parts.append(f"\n## Questions for Week {n}\n\n")
            parts.append(include(q, 2, edits=BOOK_EDITS))

    parts.append(part("Answers"))
    parts.append(latex(r"\appendix"))
    for n in LECTURES:
        a = DOCS / "question-bank" / f"week{n:02d}-answers.md"
        if a.exists():
            parts.append(chapter(f"Answers — Week {n}"))
            parts.append(include(a, 1, edits=BOOK_EDITS))
    for stem in ("mock-exam-weeks01-03", "mock-exam-weeks01-07", "mock-exam-weeks01-15"):
        p = DOCS / "question-bank" / f"{stem}.md"
        if p.exists():
            parts.append(chapter(title_of(p) + " — practice paper"))
            parts.append(include(p, 1, edits=BOOK_EDITS))
    return "".join(parts)


# ---------------------------------------------------------- lab manuals ----
ANSWERS = "# Answers to the checkpoints"

# Sentences in the student-visible part of a lab that point at the answers.
STUDENT_EDITS = [
    (re.compile(r"\s*\(answers at the end\)", re.I), ""),
    (re.compile(r"\s*\(answers are at the end[^)]*\)", re.I), ""),
    (re.compile(r"\s*Answers? (are|is) at the end( of (this|the) (lab|manual|document))?\.", re.I), ""),
    (re.compile(r"before you look at the answers at the end"), "before you check it with your TA"),
    (re.compile(r"\(Answer in Part \d+ of the\s+checkpoint answers"), "(Your TA has the answer"),
]


def lab_chapter(n: int, slug: str, ta: bool) -> str:
    path = DOCS / "labs" / f"{slug}.md"
    body = include(path, 1, drop_from=None if ta else ANSWERS)
    if not ta:
        for pat, rep in STUDENT_EDITS:
            body = pat.sub(rep, body)
    return chapter(f"Lab {n:02d} — {title_of(path)}") + body


def lab_intro(ta: bool) -> str:
    return (ROOT / "tools/templates" /
            ("lab-preface-ta.md" if ta else "lab-preface.md")).read_text(encoding="utf-8")


def lab_manual(ta: bool) -> str:
    if ta:
        head = [yaml("DSA27 Lab Manual — TAs' edition"),
                titlepage("Lab Manual", "Data Structures and Algorithms \\textperiodcentered{} Weeks 1 to 15",
                          "Teaching assistants' edition \\textperiodcentered{} with solutions and notes")]
    else:
        head = [yaml("DSA27 Lab Manual"),
                titlepage("Lab Manual", "Data Structures and Algorithms \\textperiodcentered{} Weeks 1 to 15",
                          "Students' edition")]
    parts = head + [chapter("Before the first lab"), lab_intro(ta)]
    if ta:
        parts.append(part("Notes for teaching assistants"))
        parts.append(chapter("Running the labs"))
        parts.append(include(DOCS / "labs/ta-guide.md", 1))
    parts.append(part("The labs"))
    for n, slug in LABS.items():
        if (DOCS / "labs" / f"{slug}.md").exists():
            parts.append(lab_chapter(n, slug, ta))
    if ta:
        parts.append(part("Reference solutions"))
        parts.append(latex(r"\appendix"))
        parts.append(solutions_appendix())
    return "".join(parts)


SOLUTION_FILES = [
    ("Lab 01", "solutions/labs/lab01.py"), ("Lab 02", "solutions/labs/lab02.py"),
    ("Lab 03", "solutions/labs/lab03.py"),
    ("Week 2 — array operations", "solutions/dsa/array_ops.py"),
    ("Week 3 — recursion", "solutions/dsa/recursion.py"),
    ("Lab 04 — dynamic array", "solutions/dsa/dynamic_array.py"),
    ("Lab 05 — linked list", "solutions/dsa/linked_list.py"),
    ("Lab 06 — stack", "solutions/dsa/stack.py"),
    ("Lab 07 — queues", "solutions/dsa/queue.py"),
    ("Lab 08 — searching", "solutions/dsa/searching.py"),
    ("Labs 09 and 10 — sorting", "solutions/dsa/sorting.py"),
    ("Lab 11 — binary search tree", "solutions/dsa/tree.py"),
    ("Lab 12 — heaps and priority queues", "solutions/dsa/heap.py"),
    ("Lab 13 — hash tables", "solutions/dsa/hashmap.py"),
    ("Lab 14 — graphs", "solutions/dsa/graph.py"),
    ("Labs 06 and 15 — translation", "solutions/dsa/translation.py"),
    ("Enrichment — dynamic programming", "solutions/dsa/dynamic_programming.py"),
]


def solutions_appendix() -> str:
    out = [chapter("Reference solutions"),
           "Every exercise the labs set, solved, exactly as in the repository's "
           "`solutions/` folder. Each file passes the course tests: "
           "`pytest --solutions` runs them. Show a student one function, after "
           "they have tried, never the file.\n\n"]
    for label, rel in SOLUTION_FILES:
        p = ROOT / rel
        if not p.exists():
            continue
        code = p.read_text(encoding="utf-8").rstrip()
        out.append(f"\n## {label} — `{rel}`\n\n```python\n{code}\n```\n")
    return "".join(out)


# ---------------------------------------------------------------- main ----
def main(argv: list[str]) -> None:
    builders = {"book": book,
                "lab-manual": lambda: lab_manual(False),
                "lab-manual-ta": lambda: lab_manual(True)}
    names = argv or list(builders)
    BUILD.mkdir(exist_ok=True)
    for name in names:
        text = builders[name]()
        (BUILD / f"{name}.md").write_text(text, encoding="utf-8")
        print(f"  compiled build/{name}.md  ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main(sys.argv[1:])
