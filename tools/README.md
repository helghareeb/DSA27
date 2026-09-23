# Build tooling

Markdown in `docs/` is the source of truth. Everything in `docs/pdf/` and every
image in `docs/lectures/*/figures/` is generated from it. Students never need
any of this — it is for editing the course material.

```powershell
python tools/figures.py                     # regenerate Lecture 01 figures
python tools/figures_l02.py                 # regenerate Lecture 02 figures
pwsh   tools/build.ps1                      # all PDFs
pwsh   tools/build.ps1 -Only lecture01-slides   # one target
python tools/make_notebooks.py              # scaffold any missing week notebook
```

| Script | What it does |
|---|---|
| `build.ps1` | Markdown → PDF, via pandoc and XeLaTeX |
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
| `course-guide` | `docs/course/00-course-guide.md` | `docs/pdf/DSA27-Course-Guide.pdf` |
| `study-plan` | `docs/course/01-study-plan.md` | `docs/pdf/DSA27-Study-Plan.pdf` |
| `coverage` | `docs/course/02-coverage.md` | `docs/pdf/DSA27-Coverage.pdf` |
| `regulations` | `docs/course/regulations/dsa-in-your-program.md` | `docs/pdf/DSA27-DSA-In-Your-Program.pdf` |
| `lab01` | `docs/labs/lab01-python-basics.md` | `docs/pdf/DSA27-Lab01.pdf` |
| `lab02` | `docs/labs/lab02-control-flow-functions.md` | `docs/pdf/DSA27-Lab02.pdf` |
| `lab03` | `docs/labs/lab03-data-structures-classes.md` | `docs/pdf/DSA27-Lab03.pdf` |
| `lab-ta-guide` | `docs/labs/ta-guide.md` | `docs/pdf/DSA27-Lab-TA-Guide.pdf` |

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
