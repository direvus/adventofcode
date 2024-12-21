"""Advent of Code 2024

Day 21: Keypad Conundrum

https://adventofcode.com/2024/day/21
"""
import logging  # noqa: F401
from collections import deque
from functools import cache

import grid
from util import timing, INF


KEYPAD = {
        (0, 0): '7', (1, 0): '8', (2, 0): '9',
        (0, 1): '4', (1, 1): '5', (2, 1): '6',
        (0, 2): '1', (1, 2): '2', (2, 2): '3',
                     (1, 3): '0', (2, 3): 'A',
        }
KEY_SYMBOLS = {v: k for k, v in KEYPAD.items()}

DIRPAD = {
                     (1, 0): '^', (2, 0): 'A',
        (0, 1): '<', (1, 1): 'v', (2, 1): '>',  # noqa: E131
        }
DIR_SYMBOLS = {v: k for k, v in DIRPAD.items()}


def parse(stream) -> str:
    return tuple(line.strip() for line in stream)


@cache
def find_paths(start: str, end: str):
    if start == end:
        return []

    result = []
    keypad = (start.isdigit() or end.isdigit())
    pad = KEYPAD if keypad else DIRPAD
    symbols = KEY_SYMBOLS if keypad else DIR_SYMBOLS

    position = symbols[start]
    target = symbols[end]
    q = deque()
    q.append((position,))
    distance = grid.get_distance(position, target)

    while q:
        path = q.popleft()
        p = path[-1]
        if p == target:
            result.append(path)
        if len(path) > distance:
            continue
        adjacent = (grid.get_adjacent(p) & pad.keys()) - set(path)
        for n in adjacent:
            q.append(path + (n,))
    return result


@cache
def path_to_dpad(path):
    result = []
    for i in range(1, len(path)):
        ax, ay = path[i - 1]
        bx, by = path[i]
        d = (
                '>' if bx > ax else
                '<' if bx < ax else
                '^' if by < ay else
                'v')
        result.append(d)
    result.append('A')
    return ''.join(result)


@cache
def find_best_length(sequence, level):
    result = 0
    for i in range(len(sequence)):
        start = 'A' if i == 0 else sequence[i - 1]
        end = sequence[i]

        paths = find_paths(start, end)

        if level == 0:
            length = min(len(x) for x in paths) if paths else 1
            result += length
            continue

        if not paths:
            result += 1
            continue

        lengths = set()
        for path in paths:
            dpad = path_to_dpad(path)
            lengths.add(find_best_length(dpad, level - 1))
        result += min(lengths)
    return result


def get_complexity(code: str, depth: int = 2) -> int:
    num = int(code.replace('A', ''))
    return num * find_best_length(code, depth)


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum(get_complexity(x) for x in parsed)

    with timing("Part 2"):
        result2 = sum(get_complexity(x, 25) for x in parsed)

    return (result1, result2)
