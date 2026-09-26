Two hours a week, fifteen weeks. This manual is what you work from in the lab.

**Weeks 1–3** bring everyone in the room to the same Python: the interpreter,
numbers, strings and lists; control flow, functions and errors; data structures,
classes and generators. **From Week 4** each lab walks you through building that
week's structure in the course repository, one method at a time, with drawings,
predictions and the exact tests to run.

**Before Lab 01.** Install Python 3.10 or newer and Graphviz, then:

```text
git clone https://github.com/helghareeb/DSA27.git
cd DSA27
py -3.13 -m venv .venv          # macOS / Linux: python3 -m venv .venv
.\.venv\Scripts\activate        # macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -m "not challenge"       # every one of these must pass
```

**How every lab works.**

- **Read the lecture section** a part names before you start it.
- **Draw before you code.** Each part has a "Draw it" step. A structure you
  cannot draw, you cannot write.
- **Predict at every Checkpoint** — write your prediction down, then run the
  code. The prediction is the exercise; running it is only the check.
- **Run the part's tests before moving on.** `tests/` defines what "correct"
  means. When a test fails, read its output aloud before you change anything.
- **Check-off.** At the end of the session your TA asks you to run the week's
  tests and to explain one line of your code that they choose.

**Attendance** is recorded every session and counts toward the 75% rule: below
it you are not allowed into the final exam.

**About this edition.** This is the students' edition: it has no answers to the
checkpoints and no solutions. When a lab mentions a worked solution, it means the
repository's `solutions/` folder — open it only after you have tried, and after
your tests pass, to compare. The struggle is where the learning happens: a
solution read before you have tried teaches you almost nothing.
