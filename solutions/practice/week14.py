"""SOLUTION — try the problems in `practice/week14.py` first; see `solutions/README.md`.

Question bank, Week 14 — graphs and graph searches. Problems W14-C1 to W14-C5.

Questions:  docs/question-bank/week14-questions.md
Tests:      tests/test_practice_week14.py

Use your own structures as the working storage — `Graph` from `dsa/graph.py`,
`ChainingHashMap` from `dsa/hashmap.py` for visited sets and counts,
`CircularQueue` from `dsa/queue.py` and `Stack` from `dsa/stack.py` — not a
Python dict, set or `collections.deque`. Lists are fine as inputs and results.
"""

from dsa.graph import Graph
from dsa.hashmap import ChainingHashMap
from dsa.queue import CircularQueue

STEPS = ((-1, 0), (1, 0), (0, -1), (0, 1))          # up, down, left, right


def maze_distance(maze):
    """W14-C1. The fewest steps from S to T in a maze, or -1 if T is unreachable."""
    rows = len(maze)
    cols = len(maze[0]) if rows else 0
    start = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == "S":
                start = (r, c)
    distance = ChainingHashMap()                    # cell -> steps from S
    distance.put(start, 0)
    queue = CircularQueue()
    queue.enqueue(start)
    while not queue.is_empty():
        r, c = queue.dequeue()
        if maze[r][c] == "T":
            return distance.get((r, c))
        for dr, dc in STEPS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" \
                    and (nr, nc) not in distance:
                distance.put((nr, nc), distance.get((r, c)) + 1)
                queue.enqueue((nr, nc))
    return -1


def is_bipartite(graph):
    """W14-C2. True when the graph can be two-coloured along every edge."""
    colour = ChainingHashMap()                      # vertex -> 0 or 1
    for start in graph.nodes():
        if start in colour:
            continue
        colour.put(start, 0)
        queue = CircularQueue()
        queue.enqueue(start)
        while not queue.is_empty():
            node = queue.dequeue()
            for neighbour in graph.neighbours(node):
                if neighbour not in colour:
                    colour.put(neighbour, 1 - colour.get(node))
                    queue.enqueue(neighbour)
                elif colour.get(neighbour) == colour.get(node):
                    return False                    # an edge inside one colour
    return True


WHITE, GREY, BLACK = 0, 1, 2


def topological_order_dfs(graph):
    """W14-C3. Reversed DFS finishing order, or None when there is a cycle."""
    colour = ChainingHashMap()                      # absent means WHITE
    finished = []

    def visit(node):
        colour.put(node, GREY)
        for neighbour in graph.neighbours(node):
            state = colour.get(neighbour, WHITE)
            if state == GREY:
                return False                        # back into the current path
            if state == WHITE and not visit(neighbour):
                return False
        colour.put(node, BLACK)
        finished.append(node)                       # everything after it is done
        return True

    for node in graph.nodes():
        if colour.get(node, WHITE) == WHITE and not visit(node):
            return None
    finished.reverse()
    return finished


def semester_plan(prerequisites):
    """W14-C4. Kahn's algorithm, one layer (semester) at a time."""
    graph = Graph(directed=True)
    for before, after in prerequisites:
        graph.add_edge(before, after)
    waiting = ChainingHashMap()                     # course -> unmet prerequisites
    for course in graph.nodes():
        waiting.put(course, 0)
    for course in graph.nodes():
        for later in graph.neighbours(course):
            waiting.put(later, waiting.get(later) + 1)
    semester = [course for course in graph.nodes() if waiting.get(course) == 0]
    plan, placed = [], 0
    while semester:
        semester.sort()
        plan.append(semester)
        placed += len(semester)
        following = []
        for course in semester:
            for later in graph.neighbours(course):
                waiting.put(later, waiting.get(later) - 1)
                if waiting.get(later) == 0:
                    following.append(later)
        semester = following
    if placed < len(graph):                         # the rest wait on each other
        return None
    return plan


def count_islands(grid):
    """W14-C5. Connected components of the land cells."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    seen = ChainingHashMap()
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in seen:
                continue
            islands += 1                            # a new island: flood it
            seen.put((r, c), True)
            queue = CircularQueue()
            queue.enqueue((r, c))
            while not queue.is_empty():
                cr, cc = queue.dequeue()
                for dr, dc in STEPS:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" \
                            and (nr, nc) not in seen:
                        seen.put((nr, nc), True)
                        queue.enqueue((nr, nc))
    return islands
