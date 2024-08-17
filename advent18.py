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


def get_interior_area(points: list[Point], corners: dict) -> int:
    verts = []
    clockwise = True
    min_y, max_x = points[0]
    convex = set()
    for i in range(len(points) - 1):
        a = points[i]
        b = points[i + 1]
        if a.x == b.x:
            verts.append((a.x, a.y, b.y))
        if a.y < min_y or (a.y == min_y and a.x > max_x):
            min_y, max_x = a
            clockwise = (a.x == b.x)

    # Now we know the winding direction, so filter out the corners that are
    # convex in that winding.
    convex = {p for p, w in corners.items() if w == clockwise}

    verts.sort()
    # For each point along each vertical line, draw a horizontal ray out to the
    # interior side of the vertical until it intersects with another vertical.
    # We ignore points that lie on convex corners because those rays would be
    # on the perimeter, and we also ignore points that we've intersected with
    # on previous rays.
    result = 0
    hits = set()
    for i, (vx, vy1, vy2) in enumerate(verts):
        up = vy2 < vy1
        step = 1 if clockwise == up else -1
        for y in range(min(vy1, vy2), max(vy1, vy2) + 1):
            p = Point(y, vx)
            if p in convex or p in hits:
                continue
            j = i + step
            while j >= 0 and j < len(verts):
                other = verts[j]
                min_y = min(other[1], other[2])
                max_y = max(other[1], other[2])
                if y >= min_y and y <= max_y:
                    result += abs(other[0] - vx) - 1
                    hits.add(Point(y, other[0]))
                    break

                j += step
    return result


if __name__ == '__main__':
    digs = []
    for line in sys.stdin:
        command, distance, colour = line.strip().split()
        direction = COMMANDS[command]
        digs.append((direction, int(distance), colour))

    point = Point(0, 0)
    points = [point]
    perimeter = 0
    prevdir = digs[-1][0]
    corners = {}
    for direction, distance, colour in digs:
        corners[point] = (prevdir, direction) in CORNERS
        point = move(point, direction, distance)
        points.append(point)
        perimeter += distance
        prevdir = direction

    # Part 1
    with timing("Part 1"):
        inner = get_interior_area(points, corners)
        area = inner + perimeter
    print(f"Result for Part 1 = {area}\n")
