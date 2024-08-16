#!/usr/bin/env python
import sys
from collections import namedtuple

from util import timing, Direction


VECTORS = {
        Direction.NORTH: (-1,  0),
        Direction.SOUTH:  (1,  0),
        Direction.EAST:   (0,  1),
        Direction.WEST:   (0, -1),
        }
COMMANDS = {
        'U': Direction.NORTH,
        'D': Direction.SOUTH,
        'L': Direction.WEST,
        'R': Direction.EAST,
        }


Point = namedtuple('point', ['y', 'x'])


def move(
        point: Point,
        direction: Direction,
        count: int = 1,
        ) -> Point:
    v = tuple(x * count for x in VECTORS[direction])
    return Point(point[0] + v[0], point[1] + v[1])


def get_size(points: list[Point]) -> tuple[int, int, Point]:
    min_y, min_x = points[0]
    max_y, max_x = points[0]
    for i in range(1, len(points)):
        p = points[i]
        if p.y < min_y:
            min_y = p.y
        if p.y > max_y:
            max_y = p.y
        if p.x < min_x:
            min_x = p.x
        if p.x > max_x:
            max_x = p.x
    origin = Point(points[0].y - min_y, points[0].x - min_x)
    return (max_y - min_y + 1, max_x - min_x + 1, origin)


def get_internal_area(points: list[Point]) -> set:
    verts = []
    min_y = points[0].y
    max_y = points[0].y
    for i in range(len(points) - 1):
        a = points[i]
        b = points[i + 1]
        if a.x == b.x:
            verts.append((a.x, min(a.y, b.y), max(a.y, b.y)))
        if b.y < min_y:
            min_y = b.y
        if b.y > max_y:
            max_y = b.y
    verts.sort()
    result = 0
    inner = set()
    x = None
    for y in range(min_y, max_y + 1):
        inside = False
        edge = False
        for vx, vy1, vy2 in verts:
            if y >= vy1 and y <= vy2:
                corner = y in {vy1, vy2}
                if corner and edge == inside:
                    edge = not edge
                    inside = False
                    continue
                if inside:
                    result += (vx - x) - 1
                    for i in range(x + 1, vx):
                        inner.add(Point(y, i))
                else:
                    x = vx
                if edge or not corner:
                    inside = not inside
                if corner:
                    edge = not edge
    return inner


if __name__ == '__main__':
    digs = []
    for line in sys.stdin:
        command, distance, colour = line.strip().split()
        direction = COMMANDS[command]
        digs.append((direction, int(distance), colour))

    point = Point(0, 0)
    points = [point]
    perimeter = 0
    for direction, distance, colour in digs:
        points.append(move(points[-1], direction, distance))
        perimeter += distance

    height, width, origin = get_size(points)
    rows = [[' '] * width for y in range(height)]

    point = origin
    rows[point.y][point.x] = '#'
    for direction, distance, colour in digs:
        for i in range(distance):
            point = move(point, direction, 1)
            rows[point.y][point.x] = '#'

    inner = get_internal_area(points)
    for p in inner:
        rows[p.y + origin.y][p.x + origin.x] = '+'

    for r in rows:
        print(''.join(r))

    # Part 1
    with timing("Part 1"):
        area = len(inner) + perimeter
    print(f"Result for Part 1 = {area}\n")
