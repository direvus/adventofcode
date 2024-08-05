#!/usr/bin/env python
import sys


def get_diffs(values: list[int]) -> list[int]:
    result = []
    for i in range(len(values) - 1):
        result.append(values[i + 1] - values[i])
    return result


def predict_next(sequence: list[int]) -> int:
    if len(set(sequence)) == 1:
        return sequence[0]
    diffs = get_diffs(sequence)
    nextdiff = predict_next(diffs)
    return sequence[-1] + nextdiff


def predict_prev(sequence: list[int]) -> int:
    if len(set(sequence)) == 1:
        return sequence[0]
    diffs = get_diffs(sequence)
    prev = predict_prev(diffs)
    return sequence[0] - prev


if __name__ == '__main__':
    seqs = []
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            continue
        seq = [int(x) for x in line.split()]
        seqs.append(seq)

    # Part 1
    total = 0
    for seq in seqs:
        total += predict_next(seq)
    print(total)

    # Part 2
    total = 0
    for seq in seqs:
        total += predict_prev(seq)
    print(total)
