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
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    if max(abs(dx), abs(dy)) <= 1:
        # No need to update tail
        return head, tail

    vx = 1 if dx > 0 else -1 if dx < 0 else 0
    vy = 1 if dy > 0 else -1 if dy < 0 else 0
    tail = (tail[0] + vx, tail[1] + vy)
    return head, tail


def get_tail_positions(instructions: list, count: int) -> list:
    knots = [(0, 0)] * count
    result = []
    for direction, distance in instructions:
        logging.debug(f'{direction} {distance}')
        for i in range(distance):
            logging.debug(f'  {direction} #{i}')
            knots[0] = move(knots[0], direction)
            for j in range(1, count):
                head = knots[j - 1]
                tail = knots[j]
                logging.debug(f'    {head} {tail} ->')
                head, tail = update(head, tail, direction)
                logging.debug(f'    {head} {tail}')
                knots[j - 1] = head
                knots[j] = tail
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
        tails = get_tail_positions(instructions, 2)
        result1 = len(set(tails))

    with timing("Part 2"):
        tails = get_tail_positions(instructions, 10)
        result2 = len(set(tails))

    return (result1, result2)
