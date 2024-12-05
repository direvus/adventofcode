"""Advent of Code 2024

Day 3: Mull It Over

https://adventofcode.com/2024/day/3
"""
import logging  # noqa: F401
import re

from util import timing


PATTERN = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
PATTERN2 = re.compile(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))")


def parse(stream) -> str:
    return stream.read()


def get_total(line) -> int:
    enabled = True
    result = 0
    for m in PATTERN2.findall(line):
        match m[0]:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                if enabled:
                    result += int(m[1]) * int(m[2])
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        line = parse(stream)
        matches = PATTERN.findall(line)
        result1 = sum(int(a) * int(b) for a, b in matches)

    with timing("Part 2"):
        if test:
            line = (
                    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64]"
                    "(mul(11,8)undo()?mul(8,5))"
                    )
        result2 = get_total(line)

    return (result1, result2)
