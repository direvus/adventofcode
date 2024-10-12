"""Advent of Code 2019

Day 16: Flawed Frequency Transmission

https://adventofcode.com/2019/day/16
"""
import logging  # noqa: F401

import numpy as np

from util import jit, timing


BASE = (0, 1, 0, -1)


@jit
def get_slices(size: int, index: int) -> tuple:
    """Return the positive and negative slices of the pattern."""
    pos = []
    neg = []
    i = index
    length = index + 1
    while i < size:
        pos.append((i, i + length))
        j = i + length * 2
        if j < size:
            neg.append((j, j + length))
        i += length * 4
    return pos, neg


@jit
def get_element(inputs: list, index: int) -> int:
    result = 0
    pos, neg = get_slices(len(inputs), index)
    for i, j in pos:
        result += np.sum(inputs[i:j])
    for i, j in neg:
        result -= np.sum(inputs[i:j])
    return abs(result) % 10


@jit
def do_phase(signal: list, offset: int = 0) -> None:
    """Perform one phase of transforms on the signal.

    Modify the signal in-place and return None.
    """
    for i in range(offset, len(signal)):
        signal[i] = get_element(signal, i)


@jit
def do_phases(inputs, count: int, offset: int = 0, length: int = 8) -> list:
    signal = np.array(inputs, dtype=np.uint8)
    for _ in range(count):
        do_phase(signal, offset)
    return signal[offset:offset + length]


def parse(stream) -> list[int]:
    line = stream.readline().strip()
    return [int(x) for x in line]


def run(stream, test: bool = False):
    with timing("Part 1"):
        signal = parse(stream)
        output = do_phases(signal, 100)
        result1 = ''.join(str(x) for x in output[:8])

    with timing("Part 2"):
        if test:
            signal = list(map(int, '03036732577212944063491565474664'))
        offset = int(''.join(str(x) for x in signal[:7]))
        signal = signal * 10_000
        output = do_phases(signal, 100, offset, 8)
        result2 = ''.join(str(x) for x in output)

    return (result1, result2)
