"""Advent of Code 2024

Day 22: Monkey Market

https://adventofcode.com/2024/day/22
"""
import logging  # noqa: F401
from collections import deque, Counter

from util import timing, jit


def parse(stream) -> str:
    return tuple(map(int, (line.strip() for line in stream)))


@jit
def get_secret(secret: int) -> int:
    value = (secret ^ (secret * 64)) % 16777216
    value = (value ^ (value // 32)) % 16777216
    return (value ^ (value * 2048)) % 16777216


def generate(secret: int, rounds: int) -> int:
    seq = deque()
    results = {}
    prev = secret % 10
    for _ in range(rounds):
        secret = get_secret(secret)
        digit = secret % 10
        diff = digit - prev
        seq.append(diff)
        if len(seq) > 4:
            seq.popleft()
        if len(seq) == 4:
            key = tuple(seq)
            if key not in results:
                results[key] = digit
        prev = digit
    return secret, results


def get_best_price(initials):
    sequences = Counter()
    secrets = []
    for initial in initials:
        secret, prices = generate(initial, 2000)
        secrets.append(secret)
        sequences.update(prices)
    return secrets, sequences


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        secrets, sequences = get_best_price(parsed)
        result1 = sum(secrets)

    with timing("Part 2"):
        if test:
            secrets, sequences = get_best_price([1, 2, 3, 2024])
        logging.debug(sequences.most_common(1))
        result2 = sequences.most_common(1)[0][1]

    return (result1, result2)
