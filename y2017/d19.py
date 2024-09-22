"""Advent of Code 2017

Day 19: A Series of Tubes

https://adventofcode.com/2017/day/19
"""
import logging  # noqa: F401
import string
from collections import defaultdict

from util import timing


VECTORS = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1),
        }


def parse(stream) -> dict:
    result = defaultdict(dict)
    y = 0
    for line in stream:
        for x, ch in enumerate(line):
            if not ch.isspace():
                result[y][x] = ch
        y += 1
    return result


def get_next_node(y: int, x: int, direction: str) -> tuple:
    vy, vx = VECTORS[direction]
    return y + vy, x + vx


def trace_path(nodes: dict) -> tuple:
    """Follow the path described by `nodes`.

    Return all the letter characters that were encountered along the path, in
    the order they were encountered, and also the number of steps taken, as a
    tuple.
    """
    letters = []
    steps = 0
    direction = 'D'
    xs = tuple(k for k, v in nodes[0].items() if v == '|')
    # There should be exactly one cell with a vertical bar in the top row of
    # the grid, otherwise something has gone terribly wrong.
    assert len(xs) == 1
    y = 0
    x = xs[0]
    ch = nodes[y].get(x)
    while ch:
        logging.debug(f"({y}, {x}) {ch} {direction}")
        if ch == '+':
            # Change of direction
            if direction in 'UD':
                choices = 'LR'
                glyph = '-'
            else:
                choices = 'UD'
                glyph = '|'
            options = set()
            for choice in choices:
                ny, nx = get_next_node(y, x, choice)
                nc = nodes[ny].get(nx)
                if nc is not None and (
                        nc == glyph or nc in string.ascii_letters):
                    options.add(choice)
            if len(options) != 1:
                raise ValueError(
                        f"Can't decide which way to go from {y, x} "
                        f"heading {direction}. Found {len(options)} "
                        "valid choices.")
            (direction,) = tuple(options)
            logging.debug(f"Changed direction to {direction}")
        elif ch in string.ascii_letters:
            letters.append(ch)

        # Otherwise, just keep on keepin' on.
        y, x = get_next_node(y, x, direction)
        ch = nodes[y].get(x)
        steps += 1
    return letters, steps


def run(stream, test: bool = False):
    with timing("Part 1"):
        nodes = parse(stream)
        letters, steps = trace_path(nodes)
        result1 = ''.join(letters)

    with timing("Part 2"):
        result2 = steps

    return (result1, result2)
