#!/usr/bin/env python
import re


SYMBOLS = {'#', '$', '%', '&', '*', '+', '-', '/', '=', '@'}
SYM_RE = re.compile(r'[#$%&*+/=@-]')
NUM_RE = re.compile(r'\d+')


def run(stream, test=False):
    total1 = 0
    total2 = 0
    numbers = []
    symbols = []
    gears = {}
    i = 0
    for line in stream:
        symbols.append(set())
        numbers.append([])
        for m in SYM_RE.finditer(line):
            symbols[-1].add(m.start())
            if m.group(0) == '*':
                gears[(i, m.start())] = []
        for m in NUM_RE.finditer(line):
            numbers[-1].append((int(m.group(0)), m.start(), m.end()))
        i += 1
    for row, matches in enumerate(numbers):
        # Get the positions of symbols in the current and adjacent rows
        low = max(0, row - 1)
        high = min(len(symbols), row + 2)

        for num, start, end in matches:
            matched = False
            for i in range(low, high):
                for j in range(start - 1, end + 1):
                    if j in symbols[i]:
                        if not matched:
                            total1 += num
                            matched = True
                        if (i, j) in gears:
                            gears[(i, j)].append(num)

    for loc, nums in gears.items():
        if len(nums) == 2:
            total2 += (nums[0] * nums[1])
    return (total1, total2)
