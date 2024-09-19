"""Advent of Code 2017

Day 1: Inverse Captcha

https://adventofcode.com/2017/day/1
"""


def parse(stream) -> tuple:
    line = stream.readline().strip()
    return tuple(int(x) for x in line)


def get_match_sum(digits: tuple) -> int:
    """Return the sum of all digits that match the next one."""
    result = 0
    length = len(digits)
    for i, digit in enumerate(digits):
        j = (i + 1) % length
        if digit == digits[j]:
            result += digit
    return result


def get_match_sum_p2(digits: tuple) -> int:
    """Return the sum of all matching digits with Part 2 rules.

    In Part 2, a digit matches if it is the same as the one that is half way
    around the sequence from it.

    This only words when the sequence length is even.
    """
    result = 0
    length = len(digits)
    half = length // 2
    for i, digit in enumerate(digits):
        j = (i + half) % length
        if digit == digits[j]:
            result += digit
    return result


def run(stream, test=False):
    digits = parse(stream)
    result1 = get_match_sum(digits)
    result2 = get_match_sum_p2(digits)

    return (result1, result2)
