This is the **teaching assistants' edition** of the DSA27 lab manual. It is the
students' edition plus four things students do not have in their copy:

1. **Part I — Notes for teaching assistants.** How to run a two-hour session,
   what to demonstrate live each week, the trap to show, where students go
   wrong in each exercise, the know-why questions for check-off, and the
   answers to the take-home practice.
2. **The answers to every checkpoint**, at the end of each lab.
3. **Boxed notes marked "For the TA"** inside the labs, where a hint or an
   answer sits next to the step it belongs to.
4. **The reference solution** to every lab exercise, in the appendix — exactly
   the code in the repository's `solutions/` folder, which passes the course
   tests (`pytest --solutions`).

**Do not hand this edition to students**, and do not project the solutions. Give
the smallest hint that unblocks: point to the docstring and the failing test
first, then to the drawing, and only then to one line of the solution.

The students' own setup instructions, which you should be able to troubleshoot
in the first session, are:

```text
git clone https://github.com/helghareeb/DSA27.git
cd DSA27
py -3.13 -m venv .venv          # macOS / Linux: python3 -m venv .venv
.\.venv\Scripts\activate        # macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -m "not challenge"       # every one of these must pass
```
