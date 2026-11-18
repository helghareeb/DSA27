---
title: "Midterm Exam, November 2026 — Model 2: Model Answer"
subtitle: "DSA27 · Data Structures and Algorithms · 20 questions · 10 marks"
author: "Mansoura University · Faculty of Computers and Information · AI, Bioinformatics and SE programs"
date: "November 2026"
lang: en
---

> Sit [the paper](midterm-2026-11-model2.md) first. Each question carries half a mark.

# Answer key

| # | Answer | # | Answer |
|---|---|---|---|
| 1 | **b** | 11 | **d** |
| 2 | **a** | 12 | **c** |
| 3 | **d** | 13 | **b** |
| 4 | **d** | 14 | **a** |
| 5 | **b** | 15 | **c** |
| 6 | **a** | 16 | **d** |
| 7 | **b** | 17 | **b** |
| 8 | **d** | 18 | **a** |
| 9 | **a** | 19 | **c** |
| 10 | **c** | 20 | **c** |

# The questions with their answers

**1.** Where and why was the C language created?

**b)** By Dennis Ritchie at Bell Labs, to write the Unix operating system

**2.** Which pairing of designer, language and design decision is correct?

**a)** Bjarne Stroustrup, C++, leave no room for a lower-level language

**3.** Lecture 01 calls Python’s ready-made built-in structures and tools “the honest case against Python, for us”. Why are they a problem in this course?

**d)** They already are the structures the course studies, so using them would hide the mechanism and the cost that the course is about

**4.** Python’s built-in list is best described as:

**d)** a dynamic array of references to objects

**5.** In the RAM model of Lecture 02, which of these is NOT one basic step?

**b)** Checking whether a value occurs in a Python list of many items

**6.** Under the course storage rule of Lecture 02, which of these is NOT allowed?

**a)** A queue class that stores its items in a Python list

**7.** Memoisation means:

**b)** storing the answer to each subproblem the first time and looking it up afterwards

**8.** Calling a Python function that contains the keyword yield:

**d)** returns a generator object without running the body yet

**9.** Euclid’s greatest-common-divisor function is easy to rewrite as a plain loop, while Towers of Hanoi would need an explicit stack. Why?

**a)** The first makes one recursive call as its very last action; Hanoi branches and must remember work still to do after each call

**10.** When the course dynamic array runs out of room and resizes, it:

**c)** allocates a new, bigger array, copies every element into it, and switches to it

**11.** When CPython’s list runs out of room, it grows its capacity by about:

**d)** one eighth, plus a little

**12.** When reading by index, the course dynamic array checks the index against its size, not against its capacity. Why?

**c)** The slots beyond the size hold nothing the user stored, so reading one must raise an error, as it does for a Python list

**13.** In Python, what happens to a node that nothing refers to any more?

**b)** The garbage collector reclaims it

**14.** Python’s collections.deque is implemented as:

**a)** a doubly linked list of fixed-size blocks

**15.** In a circular linked list the last node points back to the first. What does the usual traversal, which stops when it reaches a missing next node, do on such a list?

**c)** It loops for ever, because no node’s next reference is ever missing

**16.** Peek differs from pop in that it:

**d)** returns the top item without removing it

**17.** A stack built on a singly linked list should keep its top at:

**b)** the head

**18.** A deque is a structure that:

**a)** adds and removes items at both ends

**19.** A ring-buffer queue that stores only its head and tail positions (no size) finds that head equals tail. The queue is:

**c)** either full or empty, and it cannot tell which

**20.** A faulty growth step for a circular queue copies every slot to the same position in the bigger block and keeps the head where it was. It still passes a test that fills a new queue of capacity four with A, B, C, D and then adds E. Why does the test not catch the fault?

**c)** The ring has not wrapped yet: the head is at the first slot, so slot order and queue order are the same
