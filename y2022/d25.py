"""Advent of Code 2022

Day 25: Full of Hot Air

https://adventofcode.com/2022/day/25
"""
import logging  # noqa: F401

from util import timing


VALUES = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
DIGITS = {v: k for k, v in VALUES.items()}


def encode_snafu(value: int) -> str:
    """Encode a decimal integer as a SNAFU string."""
    if value == 0:
        return '0'
    div = value
    digits = []
    while div:
        div, rem = divmod(div, 5)
        if rem > 2:
            rem = -5 + rem
            div += 1
        digits.append(DIGITS[rem])
    return ''.join(reversed(digits))


def decode_snafu(value: str) -> int:
    """Decode a SNAFU-encoded string to a decimal integer."""
    unit = 1
    result = 0
    for ch in reversed(value):
        result += unit * VALUES[ch]
        unit *= 5
    return result


def parse(stream) -> tuple:
    result = [line.strip() for line in stream]
    return tuple(result)


def run(stream, test: bool = False):
    with timing("Part 1"):
        values = parse(stream)
        decimals = tuple(decode_snafu(x) for x in values)
        total = sum(decimals)
        result1 = encode_snafu(total)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
