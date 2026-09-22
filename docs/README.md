# DSA27 — Course Documentation

**CS201 · Data Structures and Algorithms · هياكل البيانات والخوارزميات**
Faculty of Computers and Information Sciences, Mansoura University — Fall 2026

---

## Start here

| | |
|---|---|
| **[Course Guide](course/00-course-guide.md)** | What the course is, how you are assessed, what fails you. Read this first. |
| **[Study Plan — 14 weeks](course/01-study-plan.md)** | Every week, its topic, and the file that grades it. |
| **[Lecture 01 — Why This Course, and Why Python](lectures/01-why-this-course/lecture.md)** | The opening lecture, in full. |
| **[DSA in your program](course/regulations/dsa-in-your-program.md)** | What the official bylaws say — extracted, with page numbers. |
| **[Links](links.md)** | WhatsApp channel, YouTube, repository. |

## Printable PDFs

| Document | PDF |
|---|---|
| Lecture 01 — handout (read this) | [`DSA27-L01-handout.pdf`](pdf/DSA27-L01-handout.pdf) |
| Lecture 01 — slides (presented) | [`DSA27-L01-slides.pdf`](pdf/DSA27-L01-slides.pdf) |
| Course guide | [`DSA27-Course-Guide.pdf`](pdf/DSA27-Course-Guide.pdf) |
| Study plan | [`DSA27-Study-Plan.pdf`](pdf/DSA27-Study-Plan.pdf) |
| DSA in your program | [`DSA27-DSA-In-Your-Program.pdf`](pdf/DSA27-DSA-In-Your-Program.pdf) |
| **Official bylaws** | [`course/regulations/`](course/regulations/) |

---

## The course in six lines

| | |
|---|---|
| Code | **CS201** — 3 credit hours (Lecture 2 · Lab 2) |
| Prerequisite | CS101 Introduction to Programming and Problem Solving |
| Level | **Sophomore — Fall**, and a major requirement in **all seven programs** |
| Assessment | Activities/Practical **20** · Midterm **15** · Oral **5** · Final **60** |
| To pass | ≥ 60% overall **and** ≥ 30% of the final **and** ≥ 75% attendance |
| Next course | CS303 Analysis and Design of Algorithms (Junior Fall) |

*Source: FCIS Internal Bylaw, Credit Hour System, 2026 — pp. 21, 22, 23, 36, 138.*

---

## Do this before the next lecture

```powershell
git clone https://github.com/helghareeb/DSA27.git
cd DSA27
py -3.13 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pytest -m "not challenge"
```

All of those must pass. They check your machine, not your code.

---

## Layout

```
docs/
├── README.md                       this page
├── links.md                        channel, YouTube, repository
├── assets/                         QR code and images
├── pdf/                            built PDFs (committed)
├── course/
│   ├── 00-course-guide.md          syllabus and rules
│   ├── 01-study-plan.md            14 weeks
│   └── regulations/                official bylaws (PDF) + extract
└── lectures/
    └── 01-why-this-course/
        └── lecture.md              source of both L01 PDFs
```

Markdown is the source of truth. The PDFs in `docs/pdf/` are built from it —
see [`tools/README.md`](../tools/README.md).
