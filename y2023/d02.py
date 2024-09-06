#!/usr/bin/env python
import re


COLOURS = ['red', 'green', 'blue']
LIMITS = [12, 13, 14]


def run(stream, test=False):
    i = 1
    total1 = 0
    total2 = 0
    for line in stream:
        _, cubes = line.strip().split(': ')
        samples = re.split(r'[;,] ', cubes)
        valid = True
        maxima = [0, 0, 0]
        for sample in samples:
            num, colour = sample.split(' ')
            k = COLOURS.index(colour)
            n = int(num)
            if n > maxima[k]:
                maxima[k] = n
            if n > LIMITS[k]:
                valid = False
        if valid:
            total1 += i
        total2 += (maxima[0] * maxima[1] * maxima[2])
        i += 1
    return (total1, total2)
