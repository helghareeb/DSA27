#!/usr/bin/env python3
"""Build the DSA27 course PDFs from their Markdown sources — on any OS.

    python tools/build.py                 # everything
    python tools/build.py lab08 book      # named targets only
    python tools/build.py --list          # the target names

Markdown in docs/ is the source of truth; everything in docs/pdf/ is generated.
Requires pandoc and xelatex on PATH. `tools/build.ps1` is a thin wrapper.

Fonts. The course look was designed with Segoe UI / Consolas (Windows). Where
they are absent (Linux, macOS) the script falls back to Noto Sans / Noto Sans
Mono, with Noto Sans Arabic carrying the Arabic runs. `fc-list` decides.

Compiled documents (the three the faculty receives):

    book             docs/pdf/DSA27-Book.pdf            lectures 1–15 + question bank with answers
    lab-manual       docs/pdf/DSA27-Lab-Manual.pdf      labs 1–15, students' edition — no solutions
    lab-manual-ta    docs/pdf/DSA27-Lab-Manual-TA.pdf   labs 1–15 + TA notes + worked solutions

They are assembled by tools/compile_book.py from the same Markdown.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
DOCS = ROOT / "docs"
DIST = DOCS / "pdf"
TMPL = TOOLS / "templates"


# ---------------------------------------------------------------- fonts ----
def _installed(family: str) -> bool:
    if shutil.which("fc-list") is None:
        return os.name == "nt"  # trust Windows to have Segoe UI / Consolas
    out = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout
    return any(family in (f.strip() for f in line.split(",")) for line in out.splitlines())


def fonts() -> dict[str, str]:
    if _installed("Segoe UI") and _installed("Consolas"):
        return {"main": "Segoe UI", "mono": "Consolas",
                "arabic": "Segoe UI", "arabicbold": "Segoe UI Bold"}
    main = "Noto Sans" if _installed("Noto Sans") else "DejaVu Sans"
    mono = "Noto Sans Mono" if _installed("Noto Sans Mono") else "DejaVu Sans Mono"
    arabic = "Noto Sans Arabic" if _installed("Noto Sans Arabic") else "Amiri"
    return {"main": main, "mono": mono, "arabic": arabic, "arabicbold": arabic + " Bold"}


FONTS = fonts()


def _pandoc_version() -> tuple[int, ...]:
    if shutil.which("pandoc") is None:
        return (0,)
    first = subprocess.run(["pandoc", "--version"], capture_output=True, text=True).stdout.split()[1]
    return tuple(int(x) for x in first.split(".") if x.isdigit())


# pandoc 3.8 renamed --highlight-style to --syntax-highlighting.
HIGHLIGHT = ("--syntax-highlighting=tango" if _pandoc_version() >= (3, 8)
             else "--highlight-style=tango")

BUILD = ROOT / "build"


def header(name: str) -> str:
    """Return a copy of a header template with the font names filled in.

    --include-in-header files are included verbatim, not templated, so the
    $arabicfont$ placeholders are substituted here.
    """
    text = (TMPL / name).read_text(encoding="utf-8")
    text = text.replace("$arabicboldfont$", FONTS["arabicbold"]).replace("$arabicfont$", FONTS["arabic"])
    BUILD.mkdir(exist_ok=True)
    out = BUILD / name
    out.write_text(text, encoding="utf-8")
    return str(out)


def common() -> list[str]:
    return [
        "--from=markdown+fenced_divs+definition_lists+pipe_tables+tex_math_dollars",
        "--pdf-engine=xelatex",
        "--lua-filter", str(TOOLS / "arabic.lua"),
        "-V", f"mainfont={FONTS['main']}",
        "-V", f"monofont={FONTS['mono']}",
        "-V", "colorlinks=true",
        "-V", "linkcolor=[HTML]{C8860D}",
        "-V", "urlcolor=[HTML]{C8860D}",
        "-V", "toccolor=[HTML]{233A3E}",
    ]


def handout_opts(toc_depth: int | None = 2) -> list[str]:
    opts = common() + [
        "--lua-filter", str(TOOLS / "strip-slides-only.lua"),
        "--lua-filter", str(TOOLS / "strip-ta-only.lua"),
        "--lua-filter", str(TOOLS / "unwrap-divs.lua"),
        "--include-in-header", header("handout-header.tex"),
        HIGHLIGHT,
        "-V", "documentclass=article",
        "-V", "geometry:a4paper,margin=2.4cm",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.15",
    ]
    if toc_depth is not None:
        opts += ["--toc", f"--toc-depth={toc_depth}"]
    return opts


def slide_opts() -> list[str]:
    return common() + [
        "--to=beamer",
        "--slide-level=2",
        "--lua-filter", str(TOOLS / "strip-handout-only.lua"),
        "--lua-filter", str(TOOLS / "unwrap-divs.lua"),
        "--include-in-header", header("beamer-header.tex"),
        HIGHLIGHT,
        "-V", "aspectratio=169",
        "-V", "fontsize=10pt",
    ]


def book_opts(ta: bool = False) -> list[str]:
    """A4 book: chapters, a TOC, the same look as the handouts.

    `ta=True` keeps the ::: {.ta-only} blocks and boxes them; otherwise they go.
    """
    ta_filter = "mark-ta-only.lua" if ta else "strip-ta-only.lua"
    return common() + [
        "--lua-filter", str(TOOLS / "strip-slides-only.lua"),
        "--lua-filter", str(TOOLS / ta_filter),
        "--lua-filter", str(TOOLS / "unwrap-divs.lua"),
        "--include-in-header", header("handout-header.tex"),
        "--include-in-header", str(TMPL / "book-header.tex"),
        HIGHLIGHT,
        "--top-level-division=chapter",
        "--toc-depth=1",
        "-V", "documentclass=report",
        "-V", "geometry:a4paper,margin=2.4cm",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.15",
        "-V", "classoption=openany",
    ]


# -------------------------------------------------------------- targets ----
LECTURES = {
    1: "01-why-this-course", 2: "02-complexity-and-arrays", 3: "03-recursion",
    4: "04-dynamic-arrays", 5: "05-linked-lists", 6: "06-stacks", 7: "07-queues",
    8: "08-searching", 9: "09-sorting-basic", 10: "10-sorting-advanced",
    11: "11-trees", 12: "12-heaps", 13: "13-hash-tables", 14: "14-graphs",
    15: "15-language-translation",
}
LABS = {
    1: "lab01-python-basics", 2: "lab02-control-flow-functions",
    3: "lab03-data-structures-classes", 4: "lab04-dynamic-arrays",
    5: "lab05-linked-lists", 6: "lab06-stacks", 7: "lab07-queues",
    8: "lab08-searching", 9: "lab09-sorting-basic", 10: "lab10-sorting-advanced",
    11: "lab11-trees", 12: "lab12-heaps", 13: "lab13-hash-tables",
    14: "lab14-graphs", 15: "lab15-language-translation",
}
QB = {
    **{f"week{w:02d}-{k}": f"DSA27-QB-Week{w:02d}-{k.title()}.pdf"
       for w in range(1, 16) for k in ("questions", "answers")},
    "mock-exam-weeks01-03": "DSA27-QB-Mock-Exam-Weeks01-03.pdf",
    "mock-exam-weeks01-07": "DSA27-QB-Mock-Exam-Weeks01-07.pdf",
    "mock-exam-weeks01-15": "DSA27-QB-Mock-Exam-Weeks01-15.pdf",
}

Target = tuple[str, Path, Path, list[str]]  # name, source, output, options


def targets() -> list[Target]:
    t: list[Target] = []
    for n, d in LECTURES.items():
        src = DOCS / "lectures" / d / "lecture.md"
        t.append((f"lecture{n:02d}-handout", src, DIST / f"DSA27-L{n:02d}-handout.pdf", handout_opts(2)))
        t.append((f"lecture{n:02d}-slides", src, DIST / f"DSA27-L{n:02d}-slides.pdf", slide_opts()))
    t += [
        ("course-guide", DOCS / "course/00-course-guide.md", DIST / "DSA27-Course-Guide.pdf", handout_opts(2)),
        ("study-plan", DOCS / "course/01-study-plan.md", DIST / "DSA27-Study-Plan.pdf", handout_opts(None)),
        ("coverage", DOCS / "course/02-coverage.md", DIST / "DSA27-Coverage.pdf", handout_opts(2)),
        ("regulations", DOCS / "course/regulations/dsa-in-your-program.md",
         DIST / "DSA27-DSA-In-Your-Program.pdf", handout_opts(2)),
    ]
    for n, f in LABS.items():
        t.append((f"lab{n:02d}", DOCS / "labs" / f"{f}.md", DIST / f"DSA27-Lab{n:02d}.pdf", handout_opts(1)))
    t.append(("lab-ta-guide", DOCS / "labs/ta-guide.md", DIST / "DSA27-Lab-TA-Guide.pdf", handout_opts(1)))
    for stem, pdf in QB.items():
        t.append((f"qb-{stem}", DOCS / "question-bank" / f"{stem}.md", DIST / pdf, handout_opts(1)))
    # The compiled documents. Their Markdown is generated into build/ first.
    for name, pdf in (("book", "DSA27-Book.pdf"),
                      ("lab-manual", "DSA27-Lab-Manual.pdf"),
                      ("lab-manual-ta", "DSA27-Lab-Manual-TA.pdf")):
        t.append((name, ROOT / "build" / f"{name}.md", DIST / pdf, book_opts(ta=name.endswith("-ta"))))
    return t


def build(name: str, source: Path, output: Path, options: list[str]) -> None:
    if name in ("book", "lab-manual", "lab-manual-ta"):
        subprocess.run([sys.executable, str(TOOLS / "compile_book.py"), name], check=True)
    if not source.exists():
        print(f"  {name:24s} skipped — {source.relative_to(ROOT)} does not exist yet")
        return
    print(f"  {name:24s} ", end="", flush=True)
    resource = [str(source.parent), str(ROOT)]
    if name in ("book", "lab-manual", "lab-manual-ta"):
        resource = [str(ROOT)]
    args = ["pandoc", *options, f"--resource-path={os.pathsep.join(resource)}",
            "-o", str(output), str(source)]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED")
        sys.stderr.write(r.stderr[-4000:])
        raise SystemExit(f"pandoc failed for {name} (exit {r.returncode})")
    print(f"-> {output.name}  ({output.stat().st_size // 1024} KB)")


def main(argv: list[str]) -> None:
    if shutil.which("pandoc") is None or shutil.which("xelatex") is None:
        raise SystemExit("pandoc and xelatex must be on PATH. See tools/README.md.")
    all_targets = targets()
    if "--list" in argv:
        print("\n".join(n for n, *_ in all_targets))
        return
    wanted = [a for a in argv if not a.startswith("-")]
    names = {n for n, *_ in all_targets}
    unknown = [w for w in wanted if w not in names]
    if unknown:
        raise SystemExit(f"unknown target(s): {', '.join(unknown)}  (see --list)")
    DIST.mkdir(parents=True, exist_ok=True)
    print(f"Building DSA27 PDFs  [fonts: {FONTS['main']} / {FONTS['mono']} / {FONTS['arabic']}]")
    for name, src, out, opts in all_targets:
        if wanted and name not in wanted:
            continue
        build(name, src, out, opts)


if __name__ == "__main__":
    main(sys.argv[1:])
