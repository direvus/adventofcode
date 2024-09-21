"""Advent of Code 2017

Day 16: Permutation Promenade

https://adventofcode.com/2017/day/16
"""
import logging  # noqa: F401
import string

from util import timing


def spin(values: list, count: int) -> list:
    return values[-count:] + values[:-count]


def exchange(values: list, a: int, b: int) -> list:
    values[a], values[b] = values[b], values[a]
    return values


def partner(values: list, a: str, b: str) -> list:
    i = values.index(a)
    j = values.index(b)
    return exchange(values, i, j)


def parse(stream) -> tuple:
    result = []
    for line in stream:
        line = line.strip()
        for command in line.split(','):
            fn = None
            args = []
            match command[0]:
                case 's':
                    fn = spin
                    args = (int(command[1:]),)
                case 'x':
                    fn = exchange
                    args = tuple(int(x) for x in command[1:].split('/'))
                case 'p':
                    fn = partner
                    args = command[1:].split('/')
            result.append((fn, args))
    return tuple(result)


def run_program(values: list, program: tuple, count: int = 1) -> list:
    for _ in range(count):
        for fn, args in program:
            values = fn(values, *args)
    return values


def find_cycle(initial: tuple, program: tuple) -> int:
    values = run_program(list(initial), program)
    i = 1
    while values != initial:
        values = run_program(values, program)
        i += 1
    return i


def run(stream, test: bool = False):
    with timing("Part 1"):
        count = 5 if test else 16
        initial = tuple(string.ascii_lowercase[:count])
        program = parse(stream)
        result1 = ''.join(run_program(list(initial), program))

    with timing("Part 2"):
        cycle = find_cycle(list(initial), program)
        logging.debug(f"Found cycle after {cycle} runs")
        count = 10 ** 9  # 1 billion
        values = run_program(list(initial), program, count % cycle)
        result2 = ''.join(values)

    return (result1, result2)
