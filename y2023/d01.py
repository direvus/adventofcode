#!/usr/bin/env python
import re
import sys


DIGITS = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        }


if __name__ == '__main__':
    total1 = 0
    total2 = 0
    exp = re.compile(r'[^\d]')
    for line in sys.stdin:
        i = 0
        d1 = []
        d2 = []
        while i < len(line):
            if line[i] in DIGITS.values():
                d1.append(line[i])
                d2.append(line[i])
            else:
                for k in DIGITS.keys():
                    if line[i:i+len(k)] == k:
                        d2.append(DIGITS[k])
                        break
            i += 1
        total1 += int(d1[0] + d1[-1])
        total2 += int(d2[0] + d2[-1])

    print(total1)
    print(total2)
