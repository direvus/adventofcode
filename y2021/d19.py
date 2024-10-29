"""Advent of Code 2021

Day 19: Beacon Scanner

https://adventofcode.com/2021/day/19
"""
import logging  # noqa: F401
from itertools import combinations

from util import get_manhattan_distance, timing


# All the possible orientations, with functions to transform coordinates from
# that orientation, back to the reference frame.
ORIENTATIONS = (
        # X is the same
        lambda p: p,
        lambda p: (p[0], -p[2], p[1]),
        lambda p: (p[0], -p[1], -p[2]),
        lambda p: (p[0], p[2], -p[1]),
        # X is reversed
        lambda p: (-p[0], p[1], -p[2]),
        lambda p: (-p[0], p[2], p[1]),
        lambda p: (-p[0], -p[1], p[2]),
        lambda p: (-p[0], -p[2], -p[1]),
        # Y aligned to reference X
        lambda p: (p[1], -p[0], p[2]),
        lambda p: (p[1], -p[2], -p[0]),
        lambda p: (p[1], p[0], -p[2]),
        lambda p: (p[1], p[2], p[0]),
        # Y aligned to reference -X
        lambda p: (-p[1], p[0], p[2]),
        lambda p: (-p[1], -p[2], p[0]),
        lambda p: (-p[1], -p[0], -p[2]),
        lambda p: (-p[1], p[2], -p[0]),
        # Z aligned to reference X
        lambda p: (p[2], p[0], p[1]),
        lambda p: (p[2], -p[1], p[0]),
        lambda p: (p[2], -p[0], -p[1]),
        lambda p: (p[2], p[1], -p[0]),
        # Z aligned to reference -X
        lambda p: (-p[2], -p[0], p[1]),
        lambda p: (-p[2], -p[1], -p[0]),
        lambda p: (-p[2], p[0], -p[1]),
        lambda p: (-p[2], p[1], p[0]),
        )


def add_vector(point: tuple, vector: tuple):
    return (
            point[0] + vector[0],
            point[1] + vector[1],
            point[2] + vector[2],
            )


def sub_vector(point: tuple, vector: tuple):
    return (
            point[0] - vector[0],
            point[1] - vector[1],
            point[2] - vector[2],
            )


class Scanner:
    def __init__(self, name, stream=''):
        self.name = name
        self.position = (0, 0, 0)
        self.pings = []
        self.reoriented = {}

        if stream:
            self.parse(stream)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            if line == '':
                break
            pos = tuple(int(x) for x in line.split(','))
            self.pings.append(pos)

    def transform(self, orientation: int):
        """Transform this scanner into a different orientation.

        Return a new scanner where all the pings have been transformed
        according to `orientation`. Specifically, assume that this scanner is
        oriented a particular way with respect to the reference frame, and
        transform its pings back into reference coordinates.
        """
        if orientation in self.reoriented:
            return self.reoriented[orientation]

        result = Scanner(f'{self.name}:{orientation}')
        fn = ORIENTATIONS[orientation]
        result.pings = list(map(fn, self.pings))
        self.reoriented[orientation] = result
        return result

    def translate(self, vector):
        """Translate this scanner's pings by a vector."""
        result = Scanner(f'{self.name}-{vector}')
        result.position = vector
        result.pings = [add_vector(p, vector) for p in self.pings]
        return result

    def get_alignments(self, other, orientation: int, limit: int = 12):
        """Find the aligned pings between two scanners.

        Treating this scanner's orientation as the frame of reference, and
        assuming the other scanner is oriented according to `orientation` with
        respect to that frame, find the maximum number of pings in common
        between the scanners and return the indexes of those matching pairs of
        pings.

        If `limit` aligned pings are ever found, we immediately return the
        vector from this scanner to the other one. Otherwise, return None.
        """
        # First, get a transformed copy of the other scanner so that we're all
        # using the same coordinate system.
        trans = other.transform(orientation)

        # Now, for each combination of one ping from each scanner, assume those
        # pings refer to the same object. That gives us a possible position for
        # the other scanner, relative to this one. Assuming that position,
        # translate all its pings into the reference frame and then see how
        # many of them coincide.
        matched = set()
        for i in range(len(self.pings)):
            for j in range(len(trans.pings)):
                if (i, j) in matched:
                    continue
                vector = sub_vector(self.pings[i], trans.pings[j])
                shifted = trans.translate(vector)
                common = set(shifted.pings) & set(self.pings)
                count = len(common)
                if count >= limit:
                    return shifted
        return None

    def find_alignment(self, other, limit: int = 12):
        """Find the best possible alignment between two scanners.

        Treating this scanner's orientation as the frame of reference, search
        through the different possible orientations and positions of the other
        scanner, such that the maximum number of pings align between them.

        If `limit` aligned pings are found, we immediately return that
        orientation. If `limit` aligned pings cannot be found in any
        configuration, then return None.
        """
        for orientation in range(24):
            result = self.get_alignments(other, orientation, limit)
            if result is not None:
                return result
        return None


def align_scanners(scanners) -> list[Scanner]:
    fixed = [scanners[0]]
    remain = scanners[1:]
    tested = set()

    while remain:
        for a in fixed:
            for i, b in enumerate(remain):
                pair = frozenset((a.name, b.name))
                if pair in tested:
                    continue
                trans = a.find_alignment(b)
                tested.add(pair)
                if trans is None:
                    continue
                fixed.append(trans)
                del remain[i]
                break
    return fixed


def count_beacons(scanners):
    beacons = set()
    for scanner in scanners:
        beacons |= set(scanner.pings)
    return len(beacons)


def parse(stream) -> str:
    header = stream.readline().strip()
    scanners = []
    while header != '':
        words = header.split()
        name = words[2]
        scanner = Scanner(name, stream)
        scanners.append(scanner)
        header = stream.readline().strip()
    return scanners


def get_max_distance(scanners):
    longest = 0
    for a, b in combinations(scanners, 2):
        dist = get_manhattan_distance(a.position, b.position)
        if dist > longest:
            longest = dist
    return longest


def run(stream, test: bool = False):
    with timing("Part 1"):
        scanners = parse(stream)
        aligned = align_scanners(scanners)
        result1 = count_beacons(aligned)

    with timing("Part 2"):
        result2 = get_max_distance(aligned)

    return (result1, result2)
