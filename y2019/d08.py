"""Advent of Code 2019

Day 8: Space Image Format

https://adventofcode.com/2019/day/8
"""
import logging  # noqa: F401
from collections import Counter

from util import INF, timing


def parse(stream) -> str:
    return stream.readline().strip()


class Image:
    def __init__(self, width: int, height: int, line: str):
        self.layers = []
        self.width = width
        self.height = height
        if line:
            self.read(line)

    def read(self, line: str):
        i = 0
        while i < len(line):
            layer = []
            for y in range(self.height):
                row = line[i:i + self.width]
                layer.append(row)
                i += self.width
            self.layers.append(layer)

    def count_digits_on_layer(self, layer: int) -> Counter:
        rows = self.layers[layer]
        counter = Counter()
        for row in rows:
            counter.update(row)
        return counter

    def find_fewest_digits(self, digit: str) -> Counter | None:
        """Find the layer with the fewest instances of `digit`.

        Return that layer's Counter of digit values.
        """
        fewest = INF
        result = None
        for i in range(len(self.layers)):
            counter = self.count_digits_on_layer(i)
            if counter[digit] < fewest:
                fewest = counter[digit]
                result = counter
        return result

    def get_pixel(self, x: int, y: int) -> str:
        """Return the decoded pixel value at a position.

        This is the first non-transparent pixel value, reading from the first
        (top) layer down.
        """
        for i in range(len(self.layers)):
            value = self.layers[i][y][x]
            if value != '2':
                return value
        return '2'

    def decode(self) -> str:
        lines = []
        glyphs = {
                '0': ' ',
                '1': '*',
                '2': ' ',
                }
        for y in range(self.height):
            line = []
            for x in range(self.width):
                px = self.get_pixel(x, y)
                line.append(glyphs[px])
            lines.append(''.join(line))
        return '\n'.join(lines)


def run(stream, test: bool = False):
    with timing("Part 1"):
        line = parse(stream)
        w, h = (3, 2) if test else (25, 6)
        im = Image(w, h, line)
        ctr = im.find_fewest_digits('0')
        result1 = ctr['1'] * ctr['2']

    with timing("Part 2"):
        if test:
            im = Image(2, 2, '0222112222120000')
        result2 = im.decode()

    return (result1, result2)
