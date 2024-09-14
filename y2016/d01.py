VECTORS = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
        ]
TURNS = {'L': -1, 'R': 1}


def parse(stream) -> set:
    line = stream.readline().strip()
    parts = line.split(', ')
    return [(x[0], int(x[1:])) for x in parts]


def move(start, direction, count):
    v = VECTORS[direction]
    return (
            start[0] + v[0] * count,
            start[1] + v[1] * count,
            )


def follow(instructions, start, direction):
    locations = {start}
    pos = start
    repeat = None
    for turn, length in instructions:
        direction = (direction + TURNS[turn]) % 4
        for _ in range(length):
            pos = move(pos, direction, 1)
            if pos in locations and repeat is None:
                repeat = pos
            locations.add(pos)
    return pos, repeat


def get_distance(a, b) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def run(stream, test=False, draw=False):
    instructions = parse(stream)
    start = (0, 0)
    direction = 0
    end, repeat = follow(instructions, start, direction)

    result1 = get_distance(start, end)
    result2 = get_distance(start, repeat)

    return (result1, result2)
