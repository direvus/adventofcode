#!/usr/bin/env python
import sys
from collections import defaultdict, namedtuple

from util import timing, minmax


Point = namedtuple('point', ['x', 'y'])
Point3 = namedtuple('point', ['x', 'y', 'z'])
Block = namedtuple('block', ['a', 'b'])
Line = namedtuple('line', ['a', 'b'])


class Grid:
    def __init__(self):
        self.blocks = []
        self.supports = defaultdict(set)
        self.supported_by = defaultdict(set)
        self.sections = defaultdict(dict)

    def drop(self):
        # Sort the blocks in lowest-first order
        blocks = sorted(self.blocks, key=lambda x: min(x.a.z, x.b.z))

        dropped = []
        self.blocks = dropped

        for block in blocks:
            print(f"Dropping {block}")
            origz = min(block.a.z, block.b.z)
            newz, supports = self.find_z(block)
            print(f"Lands at {newz} supported by {supports}")
            if newz < origz:
                diff = origz - newz
                a = Point3(block.a.x, block.a.y, block.a.z - diff)
                b = Point3(block.b.x, block.b.y, block.b.z - diff)
                block = Block(a, b)
                for s in supports:
                    self.supports[s].add(block)
                    self.supported_by[block].add(s)
            dropped.append(block)
            maxz = max(block.a.z, block.b.z)
            section = get_section(block, maxz)
            self.sections[maxz][section] = block

    def find_z(self, block) -> tuple[int, set]:
        z = min(block.a.z, block.b.z)
        s = get_section(block, z)
        supports = set()
        while z > 1:
            for section in self.sections[z - 1]:
                if intersects(s, section):
                    supports.add(self.sections[z - 1][section])
            if supports:
                return (z, supports)
            z -= 1
        return (z, supports)


def parse_grid(stream) -> Grid:
    grid = Grid()
    for line in stream:
        line = line.strip()
        left, right = line.split('~')
        a = Point3(*[int(x) for x in left.split(',')])
        b = Point3(*[int(x) for x in right.split(',')])
        block = Block(a, b)
        grid.blocks.append(block)
    return grid


def get_section(block: Block, z: int) -> Line | None:
    """Return the cross-section of a block through the Z plane.

    Because all blocks are single straight lines, the cross section must be
    either a single square or a line.
    """
    if block.a.z != block.b.z:
        minz, maxz = minmax(block.a.z, block.b.z)
        if minz <= z and maxz >= z:
            a = Point(block.a.x, block.a.y)
            return Line(a, a)
    elif block.a.z == z:
        a = Point(block.a.x, block.a.y)
        b = Point(block.b.x, block.b.y)
        return Line(a, b)
    return None


def intersects(a: Line, b: Line) -> bool:
    if (a.a.x == a.b.x) and (b.a.x == b.b.x):
        if a.a.x != b.a.x:
            return False
        mina, maxa = minmax(a.a.y, a.b.y)
        minb, maxb = minmax(b.a.y, b.b.y)
        return maxa >= minb and maxb >= mina
    elif (a.a.y == a.b.y) and (b.a.y == b.b.y):
        if a.a.y != b.a.y:
            return False
        mina, maxa = minmax(a.a.x, a.b.x)
        minb, maxb = minmax(b.a.x, b.b.x)
        return maxa >= minb and maxb >= mina
    elif a.a.x == a.b.x:
        mina, maxa = minmax(a.a.y, a.b.y)
        minb, maxb = minmax(b.a.x, b.b.x)
        x = a.a.x
        y = b.a.y
        return y >= mina and y <= maxa and x >= minb and x <= maxb
    else:
        mina, maxa = minmax(a.a.x, a.b.x)
        minb, maxb = minmax(b.a.y, b.b.y)
        x = b.a.x
        y = a.a.y
        return x >= mina and x <= maxa and y >= minb and y <= maxb


def get_removable_blocks(grid: Grid) -> set[Block]:
    """Return all the blocks that can be safely disintegrated.

    Specifically, return a set of all blocks in the grid that are not the sole
    support for any other blocks.
    """
    solos = set()
    for block, supported_by in grid.supported_by.items():
        if len(supported_by) == 1:
            solos |= supported_by
    return set(grid.blocks) - solos


if __name__ == '__main__':
    grid = parse_grid(sys.stdin)

    # Part 1
    with timing("Part 1\n"):
        grid.drop()
        print(grid.blocks)
        print(grid.supports)
        print(grid.supported_by)
        blocks = get_removable_blocks(grid)
    print(f"Result for Part 1 = {len(blocks)} \n")
