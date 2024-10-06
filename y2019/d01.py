"""Advent of Code 2019

Day 1: The Tyranny of the Rocket Equation

https://adventofcode.com/2019/day/1
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> list[int]:
    result = []
    for line in stream:
        result.append(int(line.strip()))
    return result


def get_fuel(mass: int) -> int:
    return max(0, (mass // 3) - 2)


def get_total_fuel(modules: list[int]) -> int:
    return sum(map(get_fuel, modules))


def get_total_fuel_nested(modules: list[int]) -> int:
    """Get the total nested fuel requirement.

    This is the fuel requirement for all the listed modules, plus the fuel
    requirement for the fuel itself.
    """
    result = 0
    for module in modules:
        fuel = get_fuel(module)
        result += fuel
        while fuel > 0:
            fuel = get_fuel(fuel)
            result += fuel
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = get_total_fuel(parsed)

    with timing("Part 2"):
        result2 = get_total_fuel_nested(parsed)

    return (result1, result2)
