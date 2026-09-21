"""Step through an algorithm one operation at a time.

The intended pattern is that your implementation in `dsa/` is a **generator**
that yields a snapshot after each meaningful step:

    def bubble_sort(values):
        values = list(values)
        for i in range(len(values)):
            for j in range(len(values) - i - 1):
                yield values, (j, j + 1)          # about to compare
                if values[j] > values[j + 1]:
                    values[j], values[j + 1] = values[j + 1], values[j]
        yield values, ()

Then either scrub through it by hand:

    step_slider(bubble_sort([5, 2, 9, 1]))

or play it as an animation:

    animate_bars(bubble_sort([5, 2, 9, 1]))

Turning the algorithm into a generator costs one `yield` and makes every
intermediate state inspectable — which is the whole point in a lecture.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib import animation

from viz.style import as_index_set, colours

__all__ = ["normalise_frames", "animate_bars", "step_slider"]


def normalise_frames(frames):
    """Accept `[values, ...]` or `[(values, highlight), ...]`; return the pair form.

    Each frame's values are copied, so a generator that mutates one list in
    place still produces distinct frames.
    """
    out = []
    for frame in frames:
        # Pair form only when it is a 2-tuple whose first item is itself a
        # sequence of values. That keeps a frame like (5, 2) — a two-element
        # list of values passed as a tuple — from being misread as a pair.
        if isinstance(frame, tuple) and len(frame) == 2 and isinstance(frame[0], (list, tuple)):
            values, highlight = frame
        else:
            values, highlight = frame, ()
        out.append((list(values), as_index_set(highlight)))
    return out


def animate_bars(frames, interval=320, title=None, figsize=(7.0, 3.4)):
    """Animate a sequence of list states as a bar chart.

    Returns a `matplotlib.animation.FuncAnimation`. In a notebook, display it
    with:

        from IPython.display import HTML
        HTML(animate_bars(...).to_jshtml())

    `to_jshtml()` renders in the browser and needs no ffmpeg. Use
    `.save("sort.mp4")` for a video file — that one does need ffmpeg.
    """
    frames = normalise_frames(frames)
    if not frames:
        raise ValueError("no frames to animate — did the generator yield anything?")

    fig, ax = plt.subplots(figsize=figsize)
    n = len(frames[0][0])
    ceiling = max((max(values) for values, _ in frames if values), default=1)

    bars = ax.bar(range(n), frames[0][0], edgecolor="black", linewidth=1.0)
    ax.set_ylim(0, ceiling * 1.15)
    ax.set_xticks(range(n))
    if title:
        ax.set_title(title, fontsize=12)

    def render(index):
        values, highlight = frames[index]
        for i, (bar, value) in enumerate(zip(bars, values)):
            bar.set_height(value)
            fill, edge = colours(i, highlight)
            bar.set_facecolor(fill)
            bar.set_edgecolor(edge)
        ax.set_xlabel(f"step {index + 1} of {len(frames)}", fontsize=10)
        return bars

    anim = animation.FuncAnimation(
        fig, render, frames=len(frames), interval=interval, blit=False, repeat=False
    )
    plt.close(fig)  # stop the static first frame rendering alongside the animation
    return anim


def step_slider(frames, draw=None, title=None):
    """Scrub through frames with an ipywidgets slider — one step per notch.

    Better than an animation when teaching: you control the pace, you can go
    backwards, and you can stop on the interesting step and talk about it.

    `draw` defaults to a bar chart; pass `viz.draw.draw_array` or
    `viz.draw.draw_linked_list` to scrub through those instead.
    """
    import ipywidgets as widgets
    from IPython.display import display

    frames = normalise_frames(frames)
    if not frames:
        raise ValueError("no frames to show — did the generator yield anything?")

    ceiling = max((max(values) for values, _ in frames if values), default=1)

    def show(step):
        values, highlight = frames[step]
        if draw is None:
            fig, ax = plt.subplots(figsize=(7.0, 3.4))
            for i, value in enumerate(values):
                fill, edge = colours(i, highlight)
                ax.bar(i, value, facecolor=fill, edgecolor=edge, linewidth=1.4)
            ax.set_ylim(0, ceiling * 1.15)
            ax.set_xticks(range(len(values)))
            ax.set_title(title or f"step {step + 1} of {len(frames)}", fontsize=12)
            plt.show()
        else:
            draw(values, highlight=highlight, title=title or f"step {step + 1} of {len(frames)}")
            plt.show()

    slider = widgets.IntSlider(
        value=0, min=0, max=len(frames) - 1, step=1,
        description="step", continuous_update=False,
    )
    display(widgets.interactive(show, step=slider))
