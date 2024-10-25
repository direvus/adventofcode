"""Advent of Code 2020

Day 25: Combo Breaker

https://adventofcode.com/2020/day/25
"""
import logging  # noqa: F401

from util import timing


MODULUS = 20201227


def transform(subject, count=1):
    value = 1
    for _ in range(count):
        value = (value * subject) % MODULUS
    return value


def find_loop_size(subject, pub):
    i = 0
    value = 1
    while value != pub:
        value = (value * subject) % MODULUS
        i += 1
    return i


def parse(stream) -> tuple:
    return (
            int(stream.readline().strip()),
            int(stream.readline().strip()))


def run(stream, test: bool = False):
    with timing("Part 1"):
        cardpub, doorpub = parse(stream)
        cardloop = find_loop_size(7, cardpub)
        result1 = transform(doorpub, cardloop)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
