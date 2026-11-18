---
title: "Midterm Exam, November 2026 — Model 2"
subtitle: "DSA27 · Data Structures and Algorithms · 20 questions · 10 marks"
author: "Mansoura University · Faculty of Computers and Information · AI, Bioinformatics and SE programs"
date: "November 2026"
lang: en
---

> The midterm paper as it was set in November 2026 (academic year 2026/2027),
> Model 2 of two. Choose **one** answer out of four for each question; each
> question carries half a mark. Mark yourself with the
> [model answer](midterm-2026-11-model2-answers.md) **only after** you have finished. The other
> paper is [Model 1](midterm-2026-11-model1.md).

**1.** Where and why was the C language created?

- **a)** By Donald Knuth, to typeset The Art of Computer Programming
- **b)** By Dennis Ritchie at Bell Labs, to write the Unix operating system
- **c)** By Bjarne Stroustrup at Bell Labs, to add classes to Simula
- **d)** By Guido van Rossum, as a teaching language

**2.** Which pairing of designer, language and design decision is correct?

- **a)** Bjarne Stroustrup, C++, leave no room for a lower-level language
- **b)** Graydon Hoare, C, trust the programmer
- **c)** Guido van Rossum, Go, fewer features and faster builds
- **d)** Bjarne Stroustrup, Python, readability is worth paying for

**3.** Lecture 01 calls Python’s ready-made built-in structures and tools “the honest case against Python, for us”. Why are they a problem in this course?

- **a)** They make the tests run too fast to be measured
- **b)** They are slower than any structure a student can write
- **c)** They are not part of the Python standard library
- **d)** They already are the structures the course studies, so using them would hide the mechanism and the cost that the course is about

**4.** Python’s built-in list is best described as:

- **a)** a stack of values with no indexing
- **b)** a fixed-size array of integers
- **c)** a linked list of values
- **d)** a dynamic array of references to objects

**5.** In the RAM model of Lecture 02, which of these is NOT one basic step?

- **a)** Calling a function (the call itself, not the work it then does)
- **b)** Checking whether a value occurs in a Python list of many items
- **c)** Comparing two small integers
- **d)** Writing a value into one slot of an array

**6.** Under the course storage rule of Lecture 02, which of these is NOT allowed?

- **a)** A queue class that stores its items in a Python list
- **b)** A stack that stores its items in the student’s own dynamic array
- **c)** A linked list that stores its values in node objects
- **d)** A function that returns its result to the caller as a Python list

**7.** Memoisation means:

- **a)** replacing recursion with a loop
- **b)** storing the answer to each subproblem the first time and looking it up afterwards
- **c)** printing each call to debug it
- **d)** raising the recursion limit

**8.** Calling a Python function that contains the keyword yield:

- **a)** runs the body and returns the first yielded value
- **b)** raises an error immediately
- **c)** runs the whole body and returns a list
- **d)** returns a generator object without running the body yet

**9.** Euclid’s greatest-common-divisor function is easy to rewrite as a plain loop, while Towers of Hanoi would need an explicit stack. Why?

- **a)** The first makes one recursive call as its very last action; Hanoi branches and must remember work still to do after each call
- **b)** The first is exponential and Hanoi is not
- **c)** Python optimises the tail call in Hanoi but not in the first
- **d)** Hanoi cannot be written without recursion at all

**10.** When the course dynamic array runs out of room and resizes, it:

- **a)** copies only the new element into a second array
- **b)** links a second array after the first one
- **c)** allocates a new, bigger array, copies every element into it, and switches to it
- **d)** makes the existing array longer, in place

**11.** When CPython’s list runs out of room, it grows its capacity by about:

- **a)** one slot
- **b)** a factor of ten
- **c)** exactly double
- **d)** one eighth, plus a little

**12.** When reading by index, the course dynamic array checks the index against its size, not against its capacity. Why?

- **a)** It is only needed so that negative indices work
- **b)** The slots beyond the size do not exist in memory yet
- **c)** The slots beyond the size hold nothing the user stored, so reading one must raise an error, as it does for a Python list
- **d)** Comparing with the size is faster than comparing with the capacity

**13.** In Python, what happens to a node that nothing refers to any more?

- **a)** The programmer must delete it explicitly
- **b)** The garbage collector reclaims it
- **c)** It stays in memory until the program ends
- **d)** It becomes the new head of the list

**14.** Python’s collections.deque is implemented as:

- **a)** a doubly linked list of fixed-size blocks
- **b)** a dynamic array
- **c)** a singly linked list of single values
- **d)** a single fixed-size array

**15.** In a circular linked list the last node points back to the first. What does the usual traversal, which stops when it reaches a missing next node, do on such a list?

- **a)** It visits every node once and stops
- **b)** It raises an error at the end
- **c)** It loops for ever, because no node’s next reference is ever missing
- **d)** It stops when it returns to the head

**16.** Peek differs from pop in that it:

- **a)** is slower
- **b)** never raises an error
- **c)** returns the bottom item
- **d)** returns the top item without removing it

**17.** A stack built on a singly linked list should keep its top at:

- **a)** the last node
- **b)** the head
- **c)** the middle node
- **d)** a separate array

**18.** A deque is a structure that:

- **a)** adds and removes items at both ends
- **b)** removes items in sorted order
- **c)** serves the most urgent item first
- **d)** can only be used as a stack

**19.** A ring-buffer queue that stores only its head and tail positions (no size) finds that head equals tail. The queue is:

- **a)** full
- **b)** empty
- **c)** either full or empty, and it cannot tell which
- **d)** corrupted

**20.** A faulty growth step for a circular queue copies every slot to the same position in the bigger block and keeps the head where it was. It still passes a test that fills a new queue of capacity four with A, B, C, D and then adds E. Why does the test not catch the fault?

- **a)** The array reorders its slots when it grows
- **b)** The test only checks the length of the queue
- **c)** The ring has not wrapped yet: the head is at the first slot, so slot order and queue order are the same
- **d)** The faulty copy is in fact correct
