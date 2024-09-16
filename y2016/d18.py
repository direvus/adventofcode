INF = float('inf')
TRAPS = {
        (0, 0, 1),
        (1, 0, 0),
        (0, 1, 1),
        (1, 1, 0),
        }


def parse(stream) -> tuple:
    line = stream.readline().strip()
    return tuple(1 if x == '.' else 0 for x in line)


def get_next_row(row: tuple) -> tuple:
    """Return the next row, based on the current row."""
    result = []
    length = len(row)
    for i in range(length):
        if i == 0:
            segment = (1,) + row[:i + 2]
        elif i == length - 1:
            segment = row[i - 1:] + (1,)
        else:
            segment = row[i - 1: i + 2]

        tile = 0 if segment in TRAPS else 1
        result.append(tile)
    return tuple(result)


def count_safe_tiles(init: str, rows: int) -> int:
    """Find the number of safe tiles in a grid.

    The `init` argument is the first row of the grid, and `rows` is the number
    of rows (including the initial one) to check for traps.
    """
    result = sum(init)
    row = init
    for _ in range(rows - 1):
        row = get_next_row(row)
        result += sum(row)
    return result


def run(stream, test=False, draw=False):
    init = parse(stream)
    rows = 10 if test else 40

    result1 = count_safe_tiles(init, rows)
    result2 = count_safe_tiles(init, 400000)

    return (result1, result2)
