#!/usr/bin/env python
from util import timing


def make_hash(s: str) -> int:
    result = 0
    for ch in s:
        result = ((result + ord(ch)) * 17) % 256
    return result


def get_focus_power(number: int, box: list, lenses: dict) -> int:
    return sum([(number + 1) * (i + 1) * lenses[x] for i, x in enumerate(box)])


def run_step(boxes: list, lenses: dict, instruction: str) -> None:
    if instruction.endswith('-'):
        label = instruction[:-1]
        box = make_hash(label)
        if label in boxes[box]:
            boxes[box].remove(label)
    else:
        label, focus = instruction.split('=')
        box = make_hash(label)
        lenses[label] = int(focus)
        if label not in boxes[box]:
            boxes[box].append(label)


def run(stream, test=False):
    lines = []
    for line in stream:
        lines.append(line.strip())

    seq = (''.join(lines)).split(',')

    # Part 1
    with timing("Part 1"):
        total1 = sum([make_hash(x) for x in seq])
    print(f"Result for Part 1 = {total1}\n")

    # Part 2
    with timing("Part 2"):
        boxes = [[] for _ in range(256)]
        lenses = {}
        for instruction in seq:
            run_step(boxes, lenses, instruction)
        total2 = sum([
                get_focus_power(i, x, lenses)
                for i, x in enumerate(boxes)])
    print(f"Result for Part 2 = {total2}\n")
    return (total1, total2)
