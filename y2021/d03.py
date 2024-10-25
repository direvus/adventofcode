"""Advent of Code 2021

Day 3: Binary Diagnostic

https://adventofcode.com/2021/day/3
"""
import logging  # noqa: F401
from collections import Counter

from util import timing


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        result.append(line)
    return result


def get_gamma(messages):
    result = []
    for i in range(len(messages[0])):
        counter = Counter((x[i] for x in messages))
        result.append(counter.most_common(1)[0][0])
    return ''.join(result)


def get_oxy(messages):
    choices = list(messages)
    i = 0
    while len(choices) > 1:
        counter = Counter((x[i] for x in choices))
        value = '0' if counter['0'] > counter['1'] else '1'
        choices = [x for x in choices if x[i] == value]
        i += 1
    return choices[0]


def get_co2(messages):
    choices = list(messages)
    i = 0
    while len(choices) > 1:
        counter = Counter((x[i] for x in choices))
        value = '1' if counter['1'] < counter['0'] else '0'
        choices = [x for x in choices if x[i] == value]
        i += 1
    return choices[0]


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        γ = get_gamma(parsed)
        trans = str.maketrans('01', '10')
        ε = γ.translate(trans)
        result1 = int(γ, 2) * int(ε, 2)

    with timing("Part 2"):
        oxy = get_oxy(parsed)
        co2 = get_co2(parsed)
        result2 = int(oxy, 2) * int(co2, 2)

    return (result1, result2)
