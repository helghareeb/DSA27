# DSA27 Question Bank

Practice questions **with worked answers**, week by week. Use it to train for the
final exam, to check you have understood a lecture, and to find out which *kind*
of question you are weak at.

## The final exam, and how this bank matches it

| Section | Marks | Format |
|---|---|---|
| **Multiple choice** | **30** | one correct answer out of **four** |
| **Essay / written** | **30** | short answers, explanations, traces, complexity analysis, proofs, code |

Remember the pass rule: **≥ 60% overall and ≥ 30% of the final** (and ≥ 75%
attendance to sit it at all). See the [course guide](../course/00-course-guide.md).

The bank has more question types than the exam has sections, because the written
section can ask any of them:

| Code | Type | What it trains |
|---|---|---|
| **M** | Multiple choice, four options | recall and quick application; every answer explains why the *wrong* options are wrong |
| **E** | Short answer and essay | explaining and justifying — with model answers and **marking points** |
| **T** | Trace the code | predicting exactly what code prints, and drawing the call stack |
| **K** | Complexity analysis | reading Θ off code and justifying it |
| **P** | Proofs | Big-O / Θ proofs and induction |
| **R** | Recurrences | writing and solving the recurrence of a recursive function |
| **S** | Array state | showing an array after each operation, and counting moves |
| **B** | Find and fix the bug | reading code critically — what breaks, for which input, and the fix |
| **C** | Write the code | real code, checked automatically by `pytest` |

Every question is tagged **[what]** (recall), **[how]** (apply) or **[why]**
(explain and justify) — the three levels from Lecture 01. The exam leans on
**[why]**.

## The weeks

| Week | Covers | Questions | Answers | Code |
|---|---|---|---|---|
| **1** | Lecture 01 (why this course) · Lab 01 (Python basics) | [questions](week01-questions.md) | [answers](week01-answers.md) | `practice/week01.py` |
| **2** | Lecture 02 (complexity, the Array) · Lab 02 (control flow, functions, errors) | [questions](week02-questions.md) | [answers](week02-answers.md) | `practice/week02.py` |
| **3** | Lecture 03 (recursion) · Lab 03 (data structures, classes) | [questions](week03-questions.md) | [answers](week03-answers.md) | `practice/week03.py` |
| — | **[Mock exam, weeks 1–3](mock-exam-weeks01-03.md)** — 30 marks MCQ + 30 marks written | | in the weekly answer files | |

Printable PDFs of every file are in [`docs/pdf/`](../pdf/) (`DSA27-QB-...`).
New weeks are added as the lectures are delivered.

## How to use it

1. **After the lecture and the lab, not before.** The bank tests what you know;
   it does not teach it. Read the handout first.
2. **Answer on paper, with the answers file closed.** For multiple choice, write
   down your letter *and one sentence of why*. A guessed right answer teaches
   you nothing.
3. **Then mark yourself** with the answers file. For every question you got
   wrong — or right for the wrong reason — read the explanation of **every**
   option. The wrong options are the misconceptions examiners test.
4. **Written answers:** compare against the **marking points**. Each point is
   roughly one mark. If a point is missing from your answer, you would have lost
   that mark.
5. **Trace questions:** predict first, *then* run the code in the REPL to check.
   A trace you only read is not practice.
6. **Code questions:** write them in `practice/weekNN.py`, then

   ```powershell
   pytest tests/test_practice_week02.py -v      # one week
   pytest -m practice                           # all of them
   ```

   The tests fail until you write the code — like every exercise in this course.
   Compare with the worked solution in the answers file only **after** the tests
   pass, and look for what the solution does more simply than yours.
7. **A week before the exam,** sit the [mock exam](mock-exam-weeks01-03.md) under
   exam conditions, then mark it.

## Honesty about what this is

- The bank trains the **same skills** as the exam, with **different questions**.
  Real exam questions are not drawn from it — memorising these answers will not
  help you; understanding them will.
- Every "what is printed" answer and every numeric claim here was checked by
  running the code, and every code solution passes its tests. If you still find
  a mistake, report it on the course channel — a corrected question is worth
  more than a silent one.
- The `practice/` problems are **not graded**. The graded exercises are in
  `labs/` and `dsa/`.
