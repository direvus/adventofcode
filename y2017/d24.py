"""Advent of Code 2017

Day 24: Electromagnetic Moat

https://adventofcode.com/2017/day/24
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> tuple:
    pieces = []
    for line in stream:
        line = line.strip()
        ports = tuple(int(x) for x in line.split('/'))
        pieces.append(ports)
    return pieces


def find_strongest_bridge(pieces: tuple) -> int:
    q = [()]
    best = float('-inf')
    while q:
        bridge = q.pop(0)
        lastport = 0
        strength = 0
        for index in bridge:
            part = pieces[index]
            lastport = part[1] if part[0] == lastport else part[0]
            strength += sum(part)
        if strength > best:
            best = strength

        for i, part in enumerate(pieces):
            if i in bridge or lastport not in part:
                continue
            q.append(bridge + (i,))
    return best


def find_longest_bridge(pieces: tuple) -> int:
    q = [()]
    best = (0, 0)
    while q:
        bridge = q.pop(0)
        lastport = 0
        strength = 0
        for index in bridge:
            part = pieces[index]
            lastport = part[1] if part[0] == lastport else part[0]
            strength += sum(part)
        length = len(bridge)
        value = (length, strength)
        if value > best:
            best = value

        for i, part in enumerate(pieces):
            if i in bridge or lastport not in part:
                continue
            q.append(bridge + (i,))
    return best[1]


def run(stream, test: bool = False):
    with timing("Part 1"):
        pieces = parse(stream)
        result1 = find_strongest_bridge(pieces)

    with timing("Part 2"):
        result2 = find_longest_bridge(pieces)

    return (result1, result2)
