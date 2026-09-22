---
title: "Course Guide"
subtitle: "CS201 — Data Structures and Algorithms · هياكل البيانات والخوارزميات"
author: "Dr. Haitham A. El-Ghareeb"
institute: "Faculty of Computers and Information Sciences, Mansoura University"
date: "Fall 2026"
lang: en
---

> Every rule on this page is taken from the **FCIS Internal Bylaw for the
> Bachelor Stage, Credit Hour System, 2026**, with the page number printed next
> to it. The bylaw is in this repository:
> [`regulations/FCIS-Bylaw-2026.pdf`](regulations/FCIS-Bylaw-2026.pdf).
> Where this guide and the bylaw disagree, **the bylaw is right**.

---

## 1. The course

| Field | Value | Source |
|---|---|---|
| Code | **CS201** | Bylaw p. 138 |
| Name (EN) | Data Structures and Algorithms | p. 138 |
| Name (AR) | **هياكل البيانات والخوارزميات** | p. 36 |
| Credit hours | **3** | p. 138 |
| Weekly contact hours | Lecture **2** · Tutorial **—** · Laboratory **2** | p. 138 |
| Prerequisite | Introduction to Programming and Problem Solving (**CS101**) | p. 138 |
| Level / semester | **المستوى الثاني (Sophomore) — Fall** | p. 36 |
| Required student workload | **155 hours** | p. 138 |
| Equivalent ECTS | **5.14** | p. 138 |
| Taught as a **major** in | IS, CS, IT, SE, MI, AI, NCS — **all seven programs** | p. 138 |
| Taught as a minor in | — | p. 138 |

### Official course content (quoted verbatim, bylaw p. 138)

> "This course introduces fundamental data structures, algorithms, and abstract
> data types using a mix of programming and theory. Main topics include data
> structures such as arrays, lists, linked lists, stacks, queues, hash tables,
> heaps, priority queues, graphs, and trees. It introduces algorithms used for
> list manipulation, graph searches, sorting, searching, and tree traversals.
> Also, it introduces analyzing and managing the complexity associated with data
> structures and their operations."

### Where CS201 sits

```
CS101  Introduction to Programming          (Freshman)
  │      and Problem Solving
  ▼
CS201  Data Structures and Algorithms       (Sophomore Fall)   ← you are here
  │
  ├───> IS202  Introduction to Database Systems    (Sophomore Spring)
  └───> CS303  Analysis and Design of Algorithms   (Junior Fall)
```

`CS303` is where divide-and-conquer, greedy methods, **dynamic programming**,
the master theorem, graph theory and NP-completeness are treated properly
(bylaw p. 144). CS201 is the foundation it stands on.

---

## 2. How you are assessed

Taken directly from the CS201 specification, bylaw p. 138:

| Component | Weight | Type |
|---|---|---|
| Student Activities / Practical Exam (SA/PE) | **20** | Exam |
| Midterm (MT) | **15** | Exam |
| Oral Exam (OE) | **5** | Exam |
| Final written exam (FE) | **60** | Exam |
| | **100** | |

### The two rules that fail students

**1 — The double threshold** (Article 17, p. 23)

You must score **at least 60% of the total** *and* **at least 30% of the final
exam mark**. Both. Missing either one is a fail.

> A student with 35/40 on coursework who scores 25% on the final has **failed**,
> even though the arithmetic total looks survivable. Coursework cannot rescue a
> final exam below 30%.

**2 — Attendance** (Article 15, p. 21)

You must attend **at least 75%** of lectures and labs to be allowed into the
final exam. Below that you are recorded as **محروم** (barred) and counted as a
fail for the course.

> Over a 14-week course that is roughly three sessions you can miss. Not five.

### Grade scale (bylaw p. 22)

| Grade | Points | Percentage | | Grade | Points | Percentage |
|---|---|---|---|---|---|---|
| A+ | 4.0 | ≥ 97% | | C+ | 2.3 | 73 – < 76% |
| A | 4.0 | 93 – < 97% | | C | 2.0 | 70 – < 73% |
| A− | 3.7 | 89 – < 93% | | C− | 1.7 | 67 – < 70% |
| B+ | 3.3 | 84 – < 89% | | D+ | 1.3 | 64 – < 67% |
| B | 3.0 | 80 – < 84% | | D | 1.0 | 60 – < 64% |
| B− | 2.7 | 76 – < 80% | | **F** | 0.0 | **< 60%** |

Non-GPA grades (p. 22): `P` ناجح · `F` راسب · `W` منسحب · `Abs` absent from the
final without an accepted excuse · `I` incomplete.

The minimum passing grade in any course is **D** (p. 21). Graduation requires a
cumulative GPA of at least **2.00 / 4.00** across **142 credit hours** (pp. 15–16).

---

## 3. Proposed — confirm before relying on this

> **The 20 marks for Student Activities / Practical Exam are allocated by the
> instructor, not by the bylaw.** The split below is a *proposal* and is not
> final until announced in the lecture and on the WhatsApp channel.

| Activity | Proposed marks |
|---|---|
| Lab exercises — `pytest -m challenge` passing, checked at milestones | 10 |
| Practical exam — implement a structure under time, in the lab | 8 |
| Homework 1 (environment + written comparison) | 2 |
| | **20** |

Everything else on this page is bylaw text and is not negotiable.

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
| **Visualisation** | `viz/` draws, animates and measures. Already written — use it. |

The rule that shapes everything, from `dsa/__init__.py`:

> **No module may use the built-in it is reimplementing.**

`dsa/dynamic_array.py` may not be backed by a `list`. `dsa/hashmap.py` may not be
backed by a `dict`. Routing around this may make tests pass; it will not make you
a programmer.

### Asking for help

1. Read the failing test. It states the contract.
2. Set a breakpoint and step through it — **F5**, *pytest: current test file*.
3. Then ask, on the [WhatsApp channel](https://whatsapp.com/channel/0029Vb8XynEFy72KWbH6vS2V),
   with the failing test name and the error text.

"It does not work" is not a question. "`test_pop_from_empty_raises` expects
`IndexError` and I am getting `None`" is.

---

## 6. Links

| | |
|---|---|
| Repository | <https://github.com/helghareeb/DSA27> |
| WhatsApp channel | <https://whatsapp.com/channel/0029Vb8XynEFy72KWbH6vS2V> |
| YouTube | <https://www.youtube.com/@0xHGH> |
| Study plan | [`01-study-plan.md`](01-study-plan.md) |
| Lecture 01 | [`../lectures/01-why-this-course/lecture.md`](../lectures/01-why-this-course/lecture.md) |
| Your program's regulations | [`regulations/`](regulations/) |
