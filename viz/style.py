"""Shared colours and sizing, so every diagram in the course looks the same."""

# Normal element
NODE_FILL = "#e8eef7"
NODE_EDGE = "#3a5a8c"

# The element currently under consideration
HILITE_FILL = "#ffe3b0"
HILITE_EDGE = "#c8860d"

# An element already in its final position / already visited
DONE_FILL = "#d8efd8"
DONE_EDGE = "#3f7a3f"

# Muted text (None pointers, axis labels)
MUTED = "#8a8a8a"

FONT = "DejaVu Sans"


def colours(index, highlight=(), done=()):
    """Pick (fill, edge) for one element given the highlight/done index sets."""
    if index in done:
        return DONE_FILL, DONE_EDGE
    if index in highlight:
        return HILITE_FILL, HILITE_EDGE
    return NODE_FILL, NODE_EDGE


def as_index_set(value):
    """Accept None, a single int, or any iterable of ints; return a set."""
    if value is None:
        return set()
    if isinstance(value, int):
        return {value}
    return set(value)
