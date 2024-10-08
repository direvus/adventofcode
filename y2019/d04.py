"""Advent of Code 2019

Day 4: Secure Container

https://adventofcode.com/2019/day/4
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> tuple[int, int]:
    line = stream.readline().strip()
    low, high = line.split('-')
    return int(low), int(high)


def has_double(password: str) -> bool:
    for i in range(1, len(password)):
        if password[i - 1] == password[i]:
            return True
    return False


def is_valid(password: str) -> bool:
    double = False
    for i in range(1, len(password)):
        if password[i] < password[i - 1]:
            return False
        if password[i - 1] == password[i]:
            double = True
    return double


def is_valid2(password: str) -> bool:
    double = False
    for i in range(1, len(password)):
        if password[i] < password[i - 1]:
            return False
        if (password[i - 1] == password[i] and
                (i == 1 or password[i - 2] != password[i]) and
                (i == len(password) - 1 or password[i + 1] != password[i])):
            double = True
    return double


def get_valid_passwords(low: int, high: int) -> set[str]:
    return {str(i) for i in range(low, high + 1) if is_valid(str(i))}


def run(stream, test: bool = False):
    with timing("Part 1"):
        low, high = parse(stream)
        passwords = get_valid_passwords(low, high)
        result1 = len(passwords)

    with timing("Part 2"):
        result2 = len(set(filter(is_valid2, passwords)))

    return (result1, result2)
