"""Advent of Code 2022

Day 23: Unstable Diffusion

https://adventofcode.com/2022/day/23
"""
import logging  # noqa: F401
from collections import deque, Counter
from functools import cache

from util import timing


VECTORS = (
        (0, -1),   # N
        (1, -1),   # NE
        (1, 0),    # E
        (1, 1),    # SE
        (0, 1),    # S
        (-1, 1),   # SW
        (-1, 0),   # W
        (-1, -1),  # NW
        )
OPTIONS = (
        (0, 1, 7),
        (4, 3, 5),
        (6, 7, 5),
        (2, 1, 3),
        )


@cache
def move(position: tuple, direction: int):
    x, y = position
    vx, vy = VECTORS[direction]
    return x + vx, y + vy


@cache
def get_adjacent(position: tuple):
    return tuple(move(position, i) for i in range(8))


def parse(stream) -> set:
    y = 0
    result = []
    for line in stream:
        line = line.strip()
        for x, ch in enumerate(line):
            if ch == '#':
                result.append((x, y))
        y += 1
    return result


def plan_moves(elves, options):
    moves = []
    occupied = set(elves)
    for elf in elves:
        adj = get_adjacent(elf)
        present = tuple(x in occupied for x in adj)
        if not any(present):
            moves.append(elf)
            continue

        move = elf
        for indexes in options:
            if not any(present[x] for x in indexes):
                move = adj[indexes[0]]
                break
        moves.append(move)
    return moves


def do_moves(elves, moves):
    counts = Counter(moves)
    result = []
    for i in range(len(elves)):
        elf = elves[i]
        move = moves[i]
        if counts[move] == 1:
            result.append(move)
        else:
            result.append(elf)
    return result


def do_rounds(elves, rounds: int = 10):
    options = deque(OPTIONS)
    for i in range(rounds):
        moves = plan_moves(elves, options)
        new = do_moves(elves, moves)
        elves = new
        options.append(options.popleft())
    return elves


def count_rounds(elves):
    """Continue until a round completes with no elves moving.

    Return the total number of rounds that have completed.
    """
    options = deque(OPTIONS)
    rounds = 0
    while True:
        moves = plan_moves(elves, options)
        new = do_moves(elves, moves)
        rounds += 1
        if new == elves:
            return rounds
        elves = new
        options.append(options.popleft())


def count_empty_spaces(positions: list) -> int:
    xs = {p[0] for p in positions}
    ys = {p[1] for p in positions}

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    width = maxx - minx + 1
    height = maxy - miny + 1

    total = width * height
    return total - len(positions)


def to_string(elves) -> str:
    lines = []
    xs = {p[0] for p in elves}
    ys = {p[1] for p in elves}

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for y in range(miny, maxy + 1):
        line = []
        for x in range(minx, maxx + 1):
            line.append('#' if (x, y) in elves else '.')
        lines.append(''.join(line))
    return '\n'.join(lines)


def run(stream, test: bool = False):
    with timing("Part 1"):
        elves = parse(stream)
        positions = do_rounds(elves)
        result1 = count_empty_spaces(positions)

    with timing("Part 2"):
        result2 = count_rounds(elves)

    return (result1, result2)
