"""Advent of Code 2024

Day 22: Monkey Market

https://adventofcode.com/2024/day/22
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    return tuple(map(int, (line.strip() for line in stream)))


def mix(value, secret) -> int:
    return value ^ secret


def prune(value) -> int:
    return value % 16777216


def get_secret(secret: int) -> int:
    value = prune(mix(secret, secret * 64))
    value = prune(mix(value, value // 32))
    return prune(mix(value, value * 2048))


def generate(secret: int, rounds: int) -> int:
    for _ in range(rounds):
        secret = get_secret(secret)
    return secret


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum(generate(x, 2000) for x in parsed)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
