"""Advent of Code 2022

Day 9: Rope Bridge

https://adventofcode.com/2022/day/9
"""
import logging  # noqa: F401

from util import timing


VECTORS = {
        'R': (1, 0),
        'D': (0, 1),
        'L': (-1, 0),
        'U': (0, -1),
        }


def move(position: tuple, direction: str) -> tuple:
    vx, vy = VECTORS[direction]
    return (position[0] + vx, position[1] + vy)


def update(head: tuple, tail: tuple, direction: str) -> tuple:
    head = move(head, direction)
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    if max(abs(dx), abs(dy)) <= 1:
        # No need to update tail
        return head, tail

    vx = 1 if dx > 0 else -1 if dx < 0 else 0
    vy = 1 if dy > 0 else -1 if dy < 0 else 0
    tail = (tail[0] + vx, tail[1] + vy)
    return head, tail


def get_tail_positions(instructions) -> list:
    head = (0, 0)
    tail = (0, 0)
    result = []
    for direction, count in instructions:
        for i in range(count):
            head, tail = update(head, tail, direction)
            logging.debug(f'{head} {tail}')
            result.append(tail)
    return result


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        words = line.split()
        result.append((words[0], int(words[1])))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        instructions = parse(stream)
        tails = get_tail_positions(instructions)
        result1 = len(set(tails))

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
