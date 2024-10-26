"""Advent of Code 2021

Day 8: Seven Segment Search

https://adventofcode.com/2021/day/8
"""
import logging  # noqa: F401
from collections import defaultdict, Counter

from util import timing


DIGITS = (
        set('abcefg'),
        set('cf'),
        set('acdeg'),
        set('acdfg'),
        set('bcdf'),
        set('abdfg'),
        set('abdefg'),
        set('acf'),
        set('abcdefg'),
        set('abcdfg'))
SIZES = {
        2: {1},
        3: {7},
        4: {4},
        5: {2, 3, 5},
        6: {0, 6, 9},
        7: {8}}


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        signals, output = line.split(' | ')
        signals = signals.split()
        output = output.split()
        result.append((signals, output))
    return result


def analyse(signals: list[str]):
    options = defaultdict(set)
    known = {}
    for signal in signals:
        size = len(signal)
        digits = SIZES[size]
        if len(digits) == 1:
            digit = next(iter(digits))
            known[digit] = signal
        else:
            options[size].add(signal)

    # At this point, we should know which signals represent 1, 4, 7 and 8. We
    # can isolate wires in the following steps:
    #
    # 'a' is in 7 but not 1.
    a = set(known[7]) - set(known[1])
    assert len(a) == 1
    result = {next(iter(a)): 'a'}

    # 'b' and 'e' are the only wires that appear once each out of 2, 3 and 5,
    # and of those 'b' is the only one also in 4.
    counts = Counter()
    for signal in options[5]:
        counts.update(signal)
    singles = {k for k, v in counts.items() if v == 1}
    assert len(singles) == 2
    assert len(singles & set(known[4])) == 1
    b = singles & set(known[4])
    result[next(iter(b))] = 'b'
    e = singles - b
    result[next(iter(e))] = 'e'

    # 2 is the only signal out of 2, 3 and 5 that has an 'e' wire.
    wire = next(iter(e))
    for signal in options[5]:
        if wire in signal:
            known[2] = signal
            break

    # 9 is the only signal out of 0, 6 and 9 that doesn't have an 'e' wire.
    for signal in options[6]:
        if wire not in signal:
            known[9] = signal
            break

    options[5].discard(known[2])
    options[6].discard(known[9])

    # 'f' is the only wire in 9 after subtracting the wires in 2 and 'b'.
    f = (set(known[9]) - set(known[2])) - b
    result[next(iter(f))] = 'f'

    # 'c' is the only wire in 1 apart from 'f'.
    c = set(known[1]) - f

    # Out of 3 and 5, 3 has a 'c' and 5 doesn't.
    wire = next(iter(c))
    for signal in options[5]:
        if wire in signal:
            known[3] = signal
        else:
            known[5] = signal

    # Out of 0 and 6, 0 has a 'c' and 6 doesn't.
    for signal in options[6]:
        if wire in signal:
            known[0] = signal
        else:
            known[6] = signal

    assert len(known) == 10
    assert len(set(known.values())) == 10

    return {frozenset(v): k for k, v in known.items()}


def run(stream, test: bool = False):
    with timing("Both parts"):
        messages = parse(stream)
        counter = Counter()
        result2 = 0
        for signals, output in messages:
            solution = analyse(signals)
            digits = tuple(solution[frozenset(x)] for x in output)
            counter.update(digits)
            result2 += sum(digits[-(i + 1)] * 10 ** i for i in range(4))
        result1 = counter[1] + counter[4] + counter[7] + counter[8]

    return (result1, result2)
