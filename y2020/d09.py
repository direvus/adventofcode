"""Advent of Code 2020

Day 9: Encoding Error

https://adventofcode.com/2020/day/9
"""
import logging  # noqa: F401
from itertools import combinations

from util import timing


def parse(stream) -> tuple[int]:
    result = []
    for line in stream:
        line = line.strip()
        result.append(int(line))
    return tuple(result)


def has_sum(number: int, components: tuple[int]) -> bool:
    """Return the whether the number can be summed from two components."""
    for com in combinations(components, 2):
        if sum(com) == number:
            return True
    return False


def find_invalid_number(numbers: tuple[int], size: int):
    for index in range(size, len(numbers)):
        number = numbers[index]
        if not has_sum(number, numbers[index - size:index]):
            return number


def find_components(numbers: tuple[int], value: int) -> list[int]:
    for i in range(len(numbers)):
        total = numbers[i]
        for j in range(i + 1, len(numbers)):
            total += numbers[j]
            if total == value:
                return list(numbers[i:j + 1])
            elif total > value:
                # This starting position is a bust
                break


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        size = 5 if test else 25
        result1 = find_invalid_number(parsed, size)

    with timing("Part 2"):
        components = find_components(parsed, result1)
        components.sort()
        result2 = components[0] + components[-1]

    return (result1, result2)
