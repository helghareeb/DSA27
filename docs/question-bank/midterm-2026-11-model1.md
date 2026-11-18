---
title: "Midterm Exam, November 2026 — Model 1"
subtitle: "DSA27 · Data Structures and Algorithms · 20 questions · 10 marks"
author: "Mansoura University · Faculty of Computers and Information · AI, Bioinformatics and SE programs"
date: "November 2026"
lang: en
---

> The midterm paper as it was set in November 2026 (academic year 2026/2027),
> Model 1 of two. Choose **one** answer out of four for each question; each
> question carries half a mark. Mark yourself with the
> [model answer](midterm-2026-11-model1-answers.md) **only after** you have finished. The other
> paper is [Model 2](midterm-2026-11-model2.md).

**1.** An Abstract Data Type (ADT) specifies:

- **a)** the class hierarchy of the implementation
- **b)** the operations, what they mean and what they cost, and nothing about storage
- **c)** which programming language the structure must be written in
- **d)** how the data is laid out in memory

**2.** “Every general-purpose programming language is Turing-complete.” What does that tell you?

- **a)** All languages run equally fast
- **b)** All languages differ only in syntax
- **c)** Any problem solvable in one of them is solvable in any other
- **d)** A program written in one language runs unchanged in any other

**3.** In C, reading past the end of an array silently returns whatever happens to be in memory; in Python, the same read raises an error. Which explanation matches Lecture 01?

- **a)** C was designed as a portable assembler that trusts the programmer, so it does not pay for a bounds check; Python chose to fail loudly instead
- **b)** Python checks the index because it is a compiled language
- **c)** C compilers have a long-standing bug that was never fixed
- **d)** C arrays are stored as linked lists, so the index cannot be checked

**4.** When inserting into a partly filled array, the elements after the insertion point must be shifted one place to the right. In which order are they moved?

- **a)** From the insertion index towards the end
- **b)** Any order, because the result is the same
- **c)** By swapping each element with its neighbour, starting from the front
- **d)** From the last used slot back towards the insertion index

**5.** After removing an element from a partly filled array and shifting the rest left, the course clears the slot that was the last used one. Why?

- **a)** Without it, the shifted values would end up in the wrong order
- **b)** So that the length of the array goes down by one
- **c)** That slot is no longer in use; clearing it removes a stale copy of the last value, which would otherwise keep that object alive
- **d)** The course array raises an error if a slot is not empty

**6.** Every correct recursive function needs:

- **a)** a global variable to count the calls
- **b)** a base case, and a recursive case that moves closer to the base case
- **c)** a loop and a return statement
- **d)** at least two recursive calls

**7.** By default, CPython stops a recursion when the call depth reaches about:

- **a)** one hundred calls
- **b)** one hundred thousand calls
- **c)** there is no limit
- **d)** one thousand calls

**8.** What does Python do about tail-call optimisation?

- **a)** It performs it only after the recursion limit is raised
- **b)** It turns every recursion into a loop at compile time
- **c)** It performs it automatically for every tail call
- **d)** It does not perform it: every recursive call costs a stack frame

**9.** “Thrashing” in a dynamic array means:

- **a)** the garbage collector runs
- **b)** alternating operations near one boundary make the array resize on almost every operation
- **c)** the array is full
- **d)** an append causes a resize

**10.** To shrink without thrashing, a dynamic array that doubles when full should halve its capacity when the number of stored elements falls to:

- **a)** half of the capacity
- **b)** zero
- **c)** one less than the capacity
- **d)** one quarter of the capacity

**11.** How does amortised cost differ from average-case cost?

- **a)** Amortised cost is always larger than average-case cost
- **b)** Amortised cost averages over a sequence of operations and needs no assumption about the inputs
- **c)** They are the same thing
- **d)** Amortised cost averages over random inputs

**12.** A node of a singly linked list holds:

- **a)** a value and a reference to the next node
- **b)** a value and references to every later node
- **c)** only a value; the list stores the order separately
- **d)** a value and its index in the list

**13.** To remove a node from a singly linked list, you need a reference to:

- **a)** the last node
- **b)** the node after it
- **c)** the node before it
- **d)** the head only

**14.** When a new node is added at the front of a singly linked list, why must the new node be linked to the current head before the head reference is moved to the new node?

- **a)** It is only a style convention
- **b)** Otherwise the stored size of the list would be wrong
- **c)** Done the other way round, the new node would point to itself and the rest of the list would be lost
- **d)** Python evaluates assignments from right to left

**15.** “LIFO” means:

- **a)** the last item pushed is the first one popped
- **b)** the first item pushed is the first one popped
- **c)** items are popped in sorted order
- **d)** any item can be popped

**16.** In an undo/redo system built from two stacks, what happens to the redo stack when the user performs a new action?

- **a)** It is cleared
- **b)** Nothing happens to it
- **c)** The new action is pushed on it
- **d)** Its top item is undone

**17.** To turn a general recursive algorithm into a loop, you need:

- **a)** nothing, because every recursion is already a loop
- **b)** an explicit stack
- **c)** a sorted array
- **d)** a queue

**18.** “FIFO” means:

- **a)** the first item added is the first one removed
- **b)** items are removed in sorted order
- **c)** any item can be removed
- **d)** the last item added is the first one removed

**19.** A queue built on a singly linked list that keeps references to both its head and its tail should put the front of the queue at:

- **a)** the tail
- **b)** the middle node
- **c)** either end, because it makes no difference
- **d)** the head

**20.** When a circular (ring-buffer) queue removes its front item, it sets the slot it read back to empty. Why?

- **a)** Because the emptiness test looks for an empty head slot
- **b)** Because otherwise the queue’s length would be wrong
- **c)** So that the block no longer refers to the removed object, which can then be freed
- **d)** Because adding an item searches for an empty slot to write into
