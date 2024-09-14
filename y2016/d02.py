from util import Point


SIZE = 3
VECTORS = {
        'U': (-1, 0),
        'R': (0, 1),
        'D': (1, 0),
        'L': (0, -1),
        }
KEYPAD = {
                              (0, 2): '1',
                 (1, 1): '2', (1, 2): '3', (1, 3): '4',               # noqa: E131, E501
    (2, 0): '5', (2, 1): '6', (2, 2): '7', (2, 3): '8', (2, 4): '9',  # noqa: E131, E501
                 (3, 1): 'A', (3, 2): 'B', (3, 3): 'C',
                              (4, 2): 'D',
        }


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        result.append(line)
    return result


def move(start: Point, direction: str, count: int = 1) -> Point:
    """Move in a straight line to a new position.

    Valid values for `direction` are U, R, D and L.

    The movement is clamped to a square grid of size `SIZE`.
    """
    v = VECTORS[direction]
    y = min(SIZE - 1, max(0, start.y + v[0] * count))
    x = min(SIZE - 1, max(0, start.x + v[1] * count))
    return Point(y, x)


def move_keypad(start: Point, direction: str) -> Point:
    """Move one grid square to a new position.

    Valid values for `direction` are U, R, D and L.

    The movement is clamped to the KEYPAD diagonal grid.
    """
    v = VECTORS[direction]
    y = start.y + v[0]
    x = start.x + v[1]
    pos = Point(y, x)
    if pos in KEYPAD:
        return pos
    return start


def get_digit(position: Point) -> int:
    return position.y * 3 + position.x + 1


def get_keypad_digit(position: Point) -> str:
    return KEYPAD.get(position, None)


def get_code(instructions, start) -> str:
    digits = []
    pos = start
    for line in instructions:
        for direction in line:
            pos = move(pos, direction)
        digits.append(str(get_digit(pos)))
    return ''.join(digits)


def get_keypad_code(instructions, start) -> str:
    digits = []
    pos = start
    for line in instructions:
        for direction in line:
            pos = move_keypad(pos, direction)
        digits.append(get_keypad_digit(pos))
    return ''.join(digits)


def run(stream, test=False, draw=False):
    instructions = parse(stream)
    start = Point(1, 1)
    code = get_code(instructions, start)

    result1 = code
    result2 = get_keypad_code(instructions, Point(2, 0))

    return (result1, result2)
