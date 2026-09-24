---
title: "Course Guide"
subtitle: "Data Structures and Algorithms · هياكل البيانات والخوارزميات"
author: "Dr. Haitham A. El-Ghareeb"
institute: "Faculty of Computers and Information Sciences, Mansoura University"
date: "Fall 2026"
lang: en
---

> Every rule on this page comes from **the لائحة that governs your own
> program**, with the page number printed beside it. All four bylaws are in
> this repository under [`regulations/`](regulations/). Where this guide and
> your bylaw disagree, **the bylaw is right** — tell me and I will fix the guide.

---

## 1. Which course are you registered in?

Three programs, three bylaws, **one course**. Find your row.

| Your program | Code | Bylaw | Spec page |
|---|---|---|---|
| **Artificial Intelligence** | **CS2101** | [AI, 2020](regulations/Program-ArtificialIntelligence-2020.pdf) | p. 44 |
| **Bioinformatics / Medical Informatics** | **IS122** | [Medical Informatics, 2014](regulations/Program-MedicalInformatics-2014.pdf) | p. 35 |
| **Software Engineering** | **IS122** | [Software Engineering, 2013](regulations/Program-SoftwareEngineering-2013.pdf) | p. 38 |

> **On the name "Bioinformatics".** There is no Bioinformatics *program* at the
> faculty — the one usually meant is **Medical Informatics (المعلوماتية الطبية)**,
> and its bylaw is the 2014 file above. Bioinformatics is a *course* inside it
> (MED121, p. 45). If you were told you are in Bioinformatics, the 2014 bylaw is
> yours.

### Side by side

| | **AI (2020)** | **Bio / Med. Inf. (2014)** | **SWE (2013)** |
|---|---|---|---|
| Code | **CS2101** | **IS122** | **IS122** |
| Arabic name | هياكل البيانات و الخوارزميات | هياكل البيانات وتحليل الخوارزميات | هياكل البيانات وتحليل الخوارزميات |
| Credit hours | **3** | **3** | **3** |
| Weekly hours | 2 lecture + 2 lab | 2 lecture + 2 lab | 2 lecture + 2 lab |
| Prerequisite | **CS1002** Object Oriented Programming | **CS012**, **MATH012** | **CS012**, **MATH012** |
| Level / semester | Level 2, Semester 3 | Level 2 *(semester not stated)* | Sophomore, Semester 1 |
| Credits to graduate | **138** | **135** | **135** |

Different codes. Same subject, same hours, same room, same exam paper.

---

## 2. What the لائحة says this course contains

The **2013 and 2014** texts are identical, word for word (p. 38 / p. 35):

> "Introduce the fundamental concepts of data structures and the algorithms that
> proceed from them. Topics include **recursion**, the underlying philosophy of
> **object-oriented programming**, fundamental data structures (including
> **stacks, queues, linked lists, hash tables, trees, and graphs**), the basics
> of **algorithmic analysis**, and an introduction to the **principles of
> language translation**."

The **2020 AI** text (p. 44) is longer and names more structures:

> "This course provides fundamental data structures, algorithms, and **abstract
> data types** using mix of programming and theory. Main topics include data
> structures such as **arrays, lists, linked lists, stacks, queues, hash tables,
> heaps, priority queues, graphs, and trees**. It introduces algorithms such as
> those that are used for **list manipulation, graph searches, sorting,
> searching, and tree traversals**. Also, it introduces **analyzing and managing
> the complexity** associated with data structures and their operations."

**This course covers the union of both**, so that every student in the room
gets everything their own bylaw promises and a little more.
[`02-coverage.md`](02-coverage.md) maps each declared topic to the module that
implements it and the test that grades it.

### Two things worth knowing about where this course sits

**It assumes less than you might fear.** The bylaw says this course *teaches*
recursion and the philosophy of object orientation — it does not assume them.
If you are in Bio, nothing before this course taught you either: CS012 is
structured programming only, and MATH012 *Discrete Structures* has no recursion,
induction or asymptotics in it (2014, p. 30). That is exactly why Week 3 is
recursion and why nothing here assumes you have written a class before.

**For two of the three programs, this is the only algorithms course you will
ever take.** The AI bylaw has a follow-on — **AI3001 Analysis and Design of AI
Algorithms** (2020, p. 48). The 2013 and 2014 bylaws have **none at all**. So
if you are in SWE or Bio, what you do not learn here, you will not be taught
anywhere else in your degree. Plan accordingly.

### What this course unlocks

| Course | AI | Bio | SWE |
|---|---|---|---|
| Database Systems | IS2102 | IS123 | IS123 |
| Computer Networks | — | IT131 | IT131 |
| Computer Vision | — | IT132 | IT132 |
| Pattern Recognition | AI3301 | IT137 | — |
| Computer Graphics | AI2102 | — | — |
| **Software Construction** | — | — | **SWE141** |

**SWE141** (2013, p. 42) is worth singling out: "BNF and basic theory of grammars
and parsing… formal languages". That is where this course's "principles of
language translation" grows up.

---

## 3. How you are assessed

All three bylaws agree on the three rules that matter.

| Rule | Value |
|---|---|
| Final written exam | **60%** of the course mark |
| Coursework (أعمال فصلية) | the other **40%** |
| To pass | **≥ 60% overall** **and** **≥ 30% of the final exam** |
| Attendance | **≥ 75%** of lectures and labs, or **محروم** |

*Sources: SWE 2013 pp. 11–13, p. 18 · Med. Inf. 2014 pp. 11–13, p. 18 ·
AI 2020 pp. 14–16, p. 19.*

### The two rules that fail students

**1 — The double threshold.** You need **both**. A student who collects 35 of
the 40 coursework marks and then scores 25% on the final has **failed**, however
survivable the total looks. Coursework cannot rescue a final exam below 30%.

**2 — Attendance.** 75% of a 15-week course is roughly three sessions you can
miss. Not five. Below that you are recorded as **محروم** and are not allowed into
the final exam at all — it is not a penalty applied to your mark, it is a locked
door.

### How the 40% is split

The bylaws set bounds, not a fixed split:

- **SWE 2013 (p. 13) and Bio 2014 (p. 12):** midterm **≥ 20%**
- **AI 2020 (p. 16):** midterm **≥ 10%**, final **≥ 50%**
- All three: no single component may **exceed 60%**

> **Not yet fixed.** The exact split for this course will be announced in the
> lecture and on the [WhatsApp channel](https://whatsapp.com/channel/0029Vb8XynEFy72KWbH6vS2V),
> and written here once it is. A split of **Final 60 · Midterm 20 · Coursework and
> practical 20** satisfies all three bylaws and is what I intend to propose.
> Until it is announced, treat only the four rules in the table above as binding.

### Grade scale

| Grade | Points | Percentage | | Grade | Points | Percentage |
|---|---|---|---|---|---|---|
| A+ | 4.0 | ≥ 97% | | C+ | 2.3 | 73 – < 76% |
| A | 4.0 | 93 – < 97% | | C | 2.0 | 70 – < 73% |
| A− | 3.7 | 89 – < 93% | | C− | 1.7 | 67 – < 70% |
| B+ | 3.3 | 84 – < 89% | | D+ | 1.3 | 64 – < 67% |
| B | 3.0 | 80 – < 84% | | D | 1.0 | 60 – < 64% |
| B− | 2.7 | 76 – < 80% | | **F** | 0.0 | **< 60%** |

Minimum pass in any course is **D**. Graduation needs a cumulative GPA of at
least **2.00 / 4.00**, across **135** credit hours (SWE, Bio) or **138** (AI).

*One conflict, documented rather than hidden: the 2013 bylaw values A+ at 4.33 on
p. 14 and at 4.00 on p. 57. The other three documents all say 4.00, so 4.00 is
used here. See [`regulations/dsa-in-your-program.md`](regulations/dsa-in-your-program.md).*

---

## 4. What you need before week 2

```powershell
git clone https://github.com/helghareeb/DSA27.git
cd DSA27

py -3.13 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

pytest -m "not challenge"       # every one of these must pass
```

You also need **[Graphviz](https://graphviz.org/download/)** installed as a
program — the `dot` binary, not only the pip package. The environment tests
check for it.

Full setup notes, including the Windows *"python opens the Microsoft Store"*
trap and the VS Code debugging setup, are in the repository
[`README.md`](../../README.md).

---

## 5. How the course runs

| | |
|---|---|
| **Lecture** (2 h/week) | The idea, its cost, and why it exists. |
| **Lab** (2 h/week) | You implement it. The skeletons in `dsa/` raise `NotImplementedError`. |
| **Tests** | `tests/` defines what "correct" means. `pytest -m challenge`. |
| **Solutions** | `solutions/` solves every exercise taught so far — for **after** you have tried. `pytest --solutions` runs the tests on them. |
| **Notebooks** | One per week, in `notebooks/`, wired to the drawing helpers. |
| **Visualisation** | `viz/` draws, animates and measures. Already written — use it. |

The rule that shapes everything, from `dsa/__init__.py`:

> **No module may use the built-in it is reimplementing.**

`dsa/dynamic_array.py` may not be backed by a `list`. `dsa/hashmap.py` may not be
backed by a `dict`. Routing around this may make tests pass; it will not make you
a programmer.

The fifteen weeks are laid out in [`01-study-plan.md`](01-study-plan.md).

### Asking for help

1. Read the failing test. It states the contract.
2. Set a breakpoint and step through it — **F5**, *pytest: current test file*.
3. Then ask, on the [WhatsApp channel](https://whatsapp.com/channel/0029Vb8XynEFy72KWbH6vS2V),
   with the failing test name and the error text.

"It does not work" is not a question. "`test_pop_from_empty_raises` expects
`IndexError` and I am getting `None`" is.

---

## 6. From next year: the 2026 bylaw

The faculty has a new bylaw — [`FCIS-Bylaw-2026.pdf`](regulations/FCIS-Bylaw-2026.pdf),
328 pages, covering all seven programs. It replaces all three of the above with
a single **CS201**: 3 credit hours, prerequisite CS101, Sophomore Fall, assessed
20/15/5/60, a major requirement in every program, and 142 credit hours to
graduate (pp. 36, 138).

**It does not govern you.** It is in the repository so you can see where the
faculty is going, and so this material is ready for the students who arrive
under it.

---

## 7. Links

| | |
|---|---|
| Repository | <https://github.com/helghareeb/DSA27> |
| WhatsApp channel | <https://whatsapp.com/channel/0029Vb8XynEFy72KWbH6vS2V> |
| YouTube | <https://www.youtube.com/@0xHGH> |
| Study plan | [`01-study-plan.md`](01-study-plan.md) |
| Coverage matrix | [`02-coverage.md`](02-coverage.md) |
| Lecture 01 | [`../lectures/01-why-this-course/lecture.md`](../lectures/01-why-this-course/lecture.md) |
| Your program's regulations | [`regulations/`](regulations/) |
