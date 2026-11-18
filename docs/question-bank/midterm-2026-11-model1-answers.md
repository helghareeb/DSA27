---
title: "Midterm Exam, November 2026 — Model 1: Model Answer"
subtitle: "DSA27 · Data Structures and Algorithms · 20 questions · 10 marks"
author: "Mansoura University · Faculty of Computers and Information · AI, Bioinformatics and SE programs"
date: "November 2026"
lang: en
---

> Sit [the paper](midterm-2026-11-model1.md) first. Each question carries half a mark.

# Answer key

| # | Answer | # | Answer |
|---|---|---|---|
| 1 | **b** | 11 | **b** |
| 2 | **c** | 12 | **a** |
| 3 | **a** | 13 | **c** |
| 4 | **d** | 14 | **c** |
| 5 | **c** | 15 | **a** |
| 6 | **b** | 16 | **a** |
| 7 | **d** | 17 | **b** |
| 8 | **d** | 18 | **a** |
| 9 | **b** | 19 | **d** |
| 10 | **d** | 20 | **c** |

# The questions with their answers

**1.** An Abstract Data Type (ADT) specifies:

**b)** the operations, what they mean and what they cost, and nothing about storage

**2.** “Every general-purpose programming language is Turing-complete.” What does that tell you?

**c)** Any problem solvable in one of them is solvable in any other

**3.** In C, reading past the end of an array silently returns whatever happens to be in memory; in Python, the same read raises an error. Which explanation matches Lecture 01?

**a)** C was designed as a portable assembler that trusts the programmer, so it does not pay for a bounds check; Python chose to fail loudly instead

**4.** When inserting into a partly filled array, the elements after the insertion point must be shifted one place to the right. In which order are they moved?

**d)** From the last used slot back towards the insertion index

**5.** After removing an element from a partly filled array and shifting the rest left, the course clears the slot that was the last used one. Why?

**c)** That slot is no longer in use; clearing it removes a stale copy of the last value, which would otherwise keep that object alive

**6.** Every correct recursive function needs:

**b)** a base case, and a recursive case that moves closer to the base case

**7.** By default, CPython stops a recursion when the call depth reaches about:

**d)** one thousand calls

**8.** What does Python do about tail-call optimisation?

**d)** It does not perform it: every recursive call costs a stack frame

**9.** “Thrashing” in a dynamic array means:

**b)** alternating operations near one boundary make the array resize on almost every operation

**10.** To shrink without thrashing, a dynamic array that doubles when full should halve its capacity when the number of stored elements falls to:

**d)** one quarter of the capacity

**11.** How does amortised cost differ from average-case cost?

**b)** Amortised cost averages over a sequence of operations and needs no assumption about the inputs

**12.** A node of a singly linked list holds:

**a)** a value and a reference to the next node

**13.** To remove a node from a singly linked list, you need a reference to:

**c)** the node before it

**14.** When a new node is added at the front of a singly linked list, why must the new node be linked to the current head before the head reference is moved to the new node?

**c)** Done the other way round, the new node would point to itself and the rest of the list would be lost

**15.** “LIFO” means:

**a)** the last item pushed is the first one popped

**16.** In an undo/redo system built from two stacks, what happens to the redo stack when the user performs a new action?

**a)** It is cleared

**17.** To turn a general recursive algorithm into a loop, you need:

**b)** an explicit stack

**18.** “FIFO” means:

**a)** the first item added is the first one removed

**19.** A queue built on a singly linked list that keeps references to both its head and its tail should put the front of the queue at:

**d)** the head

**20.** When a circular (ring-buffer) queue removes its front item, it sets the slot it read back to empty. Why?

**c)** So that the block no longer refers to the removed object, which can then be freed
