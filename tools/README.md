# Build tooling

Markdown in `docs/` is the source of truth. Everything in `docs/pdf/` and every
image in `docs/lectures/*/figures/` is generated from it. Students never need
any of this — it is for editing the course material.

```powershell
python tools/figures.py                     # regenerate Lecture 01 figures
python tools/figures_l02.py                 # regenerate Lecture 02 figures
python tools/figures_l03.py                 # regenerate Lecture 03 figures
python tools/figures_l04.py                 # regenerate Lecture 04 figures
python tools/figures_l05.py                 # regenerate Lecture 05 figures
python tools/figures_l06.py                 # regenerate Lecture 06 figures
python tools/figures_l07.py                 # regenerate Lecture 07 figures
python tools/figures_l08.py                 # regenerate Lecture 08 figures (timing needs a working dsa/searching.py)
python tools/with_solutions.py tools/figures_l09.py   # ... to l15: the figures of weeks 9-15 time the solutions
python tools/build.py                       # all PDFs (Windows, Linux, macOS)
python tools/build.py lecture01-slides      # one target; --list shows them all
python tools/build.py book lab-manual lab-manual-ta   # the three compiled documents
pwsh   tools/build.ps1 [-Only <target>]     # the same, from PowerShell
python tools/make_notebooks.py              # scaffold any missing week notebook
```

| Script | What it does |
|---|---|
| `build.py` | Markdown → PDF, via pandoc and XeLaTeX. Falls back to Noto fonts where Segoe UI/Consolas are absent |
| `build.ps1` | A PowerShell wrapper around `build.py` |
| `compile_book.py` | Assembles the students' book and the two lab-manual editions from `docs/` (see below) |
| `figures.py` | Ten figures for Lecture 01, drawn with `viz/` and matplotlib |
| `make_notebooks.py` | One notebook per teaching week. **Never overwrites** an existing one |

## Requirements

| | |
|---|---|
| **pandoc** | `winget install --id JohnMacFarlane.Pandoc` |
| **XeLaTeX** | MiKTeX or TeX Live. `xelatex` must be on `PATH`. |

`build.ps1` adds `%LOCALAPPDATA%\Pandoc` to `PATH` itself, because winget
installs pandoc per-user and a shell opened before the install will not see it.

MiKTeX fetches missing packages on demand and pops up a dialog each time. To
stop that:

```powershell
initexmf --set-config-value "[MPM]AutoInstall=1"
```

## One source, two documents

`docs/lectures/01-why-this-course/lecture.md` is built twice — a reading handout
and a presentation deck — from the same file. Fenced divs decide what goes where:

```markdown
## A slide title            <- becomes one frame (--slide-level=2)

- the tight version that goes on the slide

::: {.handout-only}
The longer prose, the sources, the thing you say out loud. Dropped from
the deck, kept in the handout.
:::

::: {.slides-only}
Something that only makes sense projected. Dropped from the handout.
:::
```

Heading levels matter: `#` becomes a section divider slide, `##` becomes a
frame. Keep the visible part of a `##` section short enough to fit a slide and
put the depth in a `handout-only` block.

## Filters

| File | What it does |
|---|---|
| `strip-handout-only.lua` | Drops `.handout-only` divs — used for the **slides** |
| `strip-slides-only.lua` | Drops `.slides-only` divs — used for the **handout** |
| `unwrap-divs.lua` | Replaces a surviving div with its children, so pandoc emits no stray LaTeX environment |
| `arabic.lua` | Wraps each run of Arabic in `\textarabic{}` |

### Why `arabic.lua` exists

XeTeX does not reorder bidirectional text by itself. Two things go wrong
without the filter:

- An Arabic phrase inside English comes out with its **words in reverse order**.
  The filter merges each maximal run of Arabic words and wraps the *whole run*
  once — wrapping word by word is not enough, because the words would still be
  laid out left to right.
- Arabic inside a code span is set in a monospace font with no Arabic glyphs,
  so XeLaTeX reports `Missing character` and silently drops it. The filter sets
  those in the Arabic font instead.

The usual answer, `polyglossia`, is deliberately **not** used: it loads `bidi`,
which patches `tabular` and breaks pandoc's `longtable` output. The XeTeX
primitives `\beginR`/`\endR` do the whole job without touching tables.

## Templates

`templates/handout-header.tex` and `templates/beamer-header.tex` carry the
colours (slate `#233A3E`, amber `#C8860D`), the Arabic font setup, and the
Beamer theme — which reproduces the look of the 2019 deck this material
replaces.

Segoe UI carries Arabic in its **regular and bold faces only**, so both headers
map the italic slots back onto them. Without that, Arabic inside emphasis or a
blockquote disappears.

## Output

| Target | Source | PDF |
|---|---|---|
| `lecture01-handout` | `docs/lectures/01-why-this-course/lecture.md` | `docs/pdf/DSA27-L01-handout.pdf` |
| `lecture01-slides` | *(same file)* | `docs/pdf/DSA27-L01-slides.pdf` |
| `lecture02-handout` | `docs/lectures/02-complexity-and-arrays/lecture.md` | `docs/pdf/DSA27-L02-handout.pdf` |
| `lecture02-slides` | *(same file)* | `docs/pdf/DSA27-L02-slides.pdf` |
| `lecture03-handout` | `docs/lectures/03-recursion/lecture.md` | `docs/pdf/DSA27-L03-handout.pdf` |
| `lecture03-slides` | *(same file)* | `docs/pdf/DSA27-L03-slides.pdf` |
| `lecture04-handout` | `docs/lectures/04-dynamic-arrays/lecture.md` | `docs/pdf/DSA27-L04-handout.pdf` |
| `lecture04-slides` | *(same file)* | `docs/pdf/DSA27-L04-slides.pdf` |
| `lecture05-handout` | `docs/lectures/05-linked-lists/lecture.md` | `docs/pdf/DSA27-L05-handout.pdf` |
| `lecture05-slides` | *(same file)* | `docs/pdf/DSA27-L05-slides.pdf` |
| `lecture06-handout` | `docs/lectures/06-stacks/lecture.md` | `docs/pdf/DSA27-L06-handout.pdf` |
| `lecture06-slides` | *(same file)* | `docs/pdf/DSA27-L06-slides.pdf` |
| `lecture07-handout` | `docs/lectures/07-queues/lecture.md` | `docs/pdf/DSA27-L07-handout.pdf` |
| `lecture07-slides` | *(same file)* | `docs/pdf/DSA27-L07-slides.pdf` |
| `lecture08-handout` | `docs/lectures/08-searching/lecture.md` | `docs/pdf/DSA27-L08-handout.pdf` |
| `lecture08-slides` | *(same file)* | `docs/pdf/DSA27-L08-slides.pdf` |
| `course-guide` | `docs/course/00-course-guide.md` | `docs/pdf/DSA27-Course-Guide.pdf` |
| `study-plan` | `docs/course/01-study-plan.md` | `docs/pdf/DSA27-Study-Plan.pdf` |
| `coverage` | `docs/course/02-coverage.md` | `docs/pdf/DSA27-Coverage.pdf` |
| `regulations` | `docs/course/regulations/dsa-in-your-program.md` | `docs/pdf/DSA27-DSA-In-Your-Program.pdf` |
| `lab01` | `docs/labs/lab01-python-basics.md` | `docs/pdf/DSA27-Lab01.pdf` |
| `lab02` | `docs/labs/lab02-control-flow-functions.md` | `docs/pdf/DSA27-Lab02.pdf` |
| `lab03` | `docs/labs/lab03-data-structures-classes.md` | `docs/pdf/DSA27-Lab03.pdf` |
| `lab04` | `docs/labs/lab04-dynamic-arrays.md` | `docs/pdf/DSA27-Lab04.pdf` |
| `lab05` | `docs/labs/lab05-linked-lists.md` | `docs/pdf/DSA27-Lab05.pdf` |
| `lab06` | `docs/labs/lab06-stacks.md` | `docs/pdf/DSA27-Lab06.pdf` |
| `lab07` | `docs/labs/lab07-queues.md` | `docs/pdf/DSA27-Lab07.pdf` |
| `lab08` | `docs/labs/lab08-searching.md` | `docs/pdf/DSA27-Lab08.pdf` |
| `lab-ta-guide` | `docs/labs/ta-guide.md` | `docs/pdf/DSA27-Lab-TA-Guide.pdf` |
| `question-bank` | `docs/question-bank/*.md` (not the README) | `docs/pdf/DSA27-QB-*.pdf` — seven files |

## Figures

`figures.py` writes **PNG at 300 DPI**. SVG renders on GitHub but not in
XeLaTeX; PDF renders in XeLaTeX but not on GitHub. PNG is the only format both
read, so the Markdown needs one path and one file.

Nothing is borrowed — no stock photographs, no book covers, no licence to worry
about. Every figure is drawn from the course's own tooling and the palette in
`viz/style.py`, so re-running the script reproduces all ten. The
linear-vs-binary-search figure is **real measured output** from
`viz.complexity.measure()`, not a sketch of what the curves ought to look like.

Image paths in the Markdown are relative to the source file, so `build.ps1`
passes `--resource-path` per target; pandoc would otherwise resolve them against
the working directory and silently drop every image.

`docs/pdf/` is **committed**. The point of the PDFs is that a student can click a
GitHub link and get one, so they have to be in the repository.

The four bylaw PDFs in `docs/course/regulations/` are **not** generated. They
are official documents, stored byte-for-byte as downloaded; only their filenames
were made descriptive. Never rebuild or re-compress them.

## The compiled documents

| Target | PDF | Contents |
|---|---|---|
| `book` | `DSA27-Book.pdf` | Course guide, study plan; for each of the 15 weeks the lecture handout and its question bank; then every week's answers and the mock exams |
| `lab-manual` | `DSA27-Lab-Manual.pdf` | Labs 1–15, **students' edition**: each lab's `# Answers to the checkpoints` section (which must be the lab's last top-level section) and every `::: {.ta-only}` block are removed |
| `lab-manual-ta` | `DSA27-Lab-Manual-TA.pdf` | **TAs' edition**: the TA guide, labs 1–15 complete, `ta-only` blocks boxed "For the TA", and every reference solution as an appendix. Not committed: it is built locally and handed to TAs |

`compile_book.py` writes `build/<target>.md` first: YAML stripped, headings pushed
down a level, image paths made relative to the repository root, links to other
Markdown files reduced to their text.

The main font may lack some symbols (Noto Sans has no `→`, `−`, `≤`, box drawing…).
Both header templates map those characters to the monospace font with
`newunicodechar`, so they print the same in prose and in code.
