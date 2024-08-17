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
        '0': Direction.EAST,
        '1': Direction.SOUTH,
        '2': Direction.WEST,
        '3': Direction.NORTH,
        }
CORNERS = {
        # Corners that are convex in a clockwise winding
        (Direction.NORTH, Direction.EAST),
        (Direction.EAST, Direction.SOUTH),
        (Direction.SOUTH, Direction.WEST),
        (Direction.WEST, Direction.NORTH),
        }


Point = namedtuple('point', ['y', 'x'])


def move(
        point: Point,
        direction: Direction,
        count: int = 1,
        ) -> Point:
    v = tuple(x * count for x in VECTORS[direction])
    return Point(point[0] + v[0], point[1] + v[1])


def get_size(points: list[Point]) -> tuple[int, int]:
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
    return (max_y - min_y + 1, max_x - min_x + 1)


def get_direction(a: Point, b: Point) -> Direction:
    if a.y == b.y:
        return Direction.EAST if b.x > a.x else Direction.WEST
    else:
        return Direction.SOUTH if b.y > a.y else Direction.NORTH


def simplify(points: list[Point]) -> list[Point]:
    result = []
    prev = points[-2]
    direction = get_direction(prev, points[0])
    for i in range(len(points) - 1):
        a = points[i]
        b = points[i + 1]
        newdir = get_direction(a, b)
        if newdir != direction:
            result.append(a)
            direction = newdir
    result.append(points[0])
    return result


def get_interior_area(points: list[Point]) -> int:
    points = simplify(points)
    if len(points) < 5:
        return 0

    if len(points) == 5:
        # It's a rectangle - calculate area
        width, height = get_size(points)
        return (width - 2) * (height - 2)

    # Irregular polygon - split it up recursively until it's all rectangles.
    verts = []
    clockwise = True
    min_y, max_x = points[0]
    # Collect vertical lines and determine winding direction.
    for i in range(len(points) - 1):
        a = points[i]
        b = points[i + 1]
        if a.x == b.x:
            verts.append((a.x, a.y, b.y, i))
        if a.y < min_y or (a.y == min_y and a.x > max_x):
            min_y, max_x = a
            clockwise = (a.x == b.x)

    # Iterate through the vertices until we hit a concavity. From there, draw
    # a horizontal line and split the polygon along that line, and return the
    # sum of the areas of those polygons, plus the length of the splitting line
    # segment.
    prev = points[-2]
    direction = get_direction(prev, points[0])
    for i in range(len(points) - 1):
        p = points[i]
        nxt = points[i + 1]
        newdir = get_direction(p, nxt)
        directions = (direction, newdir)
        convex = (directions in CORNERS) == clockwise

        if not convex:
            break
        prev = p
        direction = newdir

    # Figure out which direction to split in. If the horizontal part is
    # first, continue in that direction. Otherwise, go opposite the
    # horizontal part.
    if p.y == prev.y:
        reverse = False if p.x > prev.x else True
    else:
        reverse = False if p.y < prev.y else True
        if not clockwise:
            reverse = not reverse

    # Now find the first vertical that intercepts the split line.
    verts.sort(reverse=reverse)
    for vx, vy1, vy2, j in verts:
        if (reverse and vx >= p.x) or (not reverse and vx <= p.x):
            continue
        min_y = min(vy1, vy2)
        max_y = max(vy1, vy2)
        if min_y <= p.y and max_y >= p.y:
            break

    if vy1 == p.y:
        node = j
    elif vy2 == p.y:
        node = j + 1
    else:
        points.insert(j + 1, Point(p.y, vx))
        node = j + 1
        if i > j + 1:
            i += 1

    splitlen = abs(vx - p.x) - 1
    if node > i:
        a = points[i:node + 1] + [p]
        b = points[node:-1] + points[:i + 1] + [points[node]]
    else:
        a = points[i:-1] + points[:node + 1] + [p]
        b = points[node:i + 1] + [points[node]]

    return sum((
            get_interior_area(a),
            get_interior_area(b),
            splitlen))


if __name__ == '__main__':
    digs = []
    for line in sys.stdin:
        command, distance, colour = line.strip().split()
        colour = colour[2:8]
        direction = COMMANDS[command]
        digs.append((direction, int(distance), colour))

    # Part 1
    with timing("Part 1"):
        point = Point(0, 0)
        points = [point]
        perimeter = 0
        for direction, distance, colour in digs:
            point = move(point, direction, distance)
            points.append(point)
            perimeter += distance

        inner = get_interior_area(points)
        area = inner + perimeter
    print(f"Result for Part 1 = {area}\n")

    # Part 2
    with timing("Part 2\n"):
        point = Point(0, 0)
        points = [point]
        perimeter = 0
        for _, _, colour in digs:
            distance = int(colour[:5], 16)
            direction = COMMANDS[colour[5]]
            point = move(point, direction, distance)
            points.append(point)
            perimeter += distance

        inner = get_interior_area(points)
        area = inner + perimeter
    print(f"Result for Part 2 = {area}\n")
