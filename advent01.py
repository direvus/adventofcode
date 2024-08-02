#!/usr/bin/env python
import re
import sys


if __name__ == '__main__':
    total = 0
    exp = re.compile(r'[^\d]')
    for line in sys.stdin:
        digits = exp.sub('', line)
        total += int(digits[0] + digits[-1])
    print(total)
