#!/usr/bin/env python
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


def run(stream, test=False):
    seqs = []
    for line in stream:
        line = line.strip()
        if line == '':
            continue
        seq = [int(x) for x in line.split()]
        seqs.append(seq)

    # Part 1
    p1 = 0
    for seq in seqs:
        p1 += predict_next(seq)

    # Part 2
    p2 = 0
    for seq in seqs:
        p2 += predict_prev(seq)
    return (p1, p2)
