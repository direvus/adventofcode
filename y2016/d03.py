def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        sides = line.split()
        result.append([int(x) for x in sides])
    return result


def reparse(triangles) -> list:
    result = []
    i = 0
    work = ([], [], [])
    for i, tri in enumerate(triangles):
        work[0].append(tri[0])
        work[1].append(tri[1])
        work[2].append(tri[2])
        if (i + 1) % 3 == 0:
            result.extend(work)
            work = ([], [], [])
    return result


def is_possible(sides: tuple) -> bool:
    return (
            sides[0] + sides[1] > sides[2] and
            sides[1] + sides[2] > sides[0] and
            sides[0] + sides[2] > sides[1])


def count_possible(triangles: list) -> int:
    result = 0
    for sides in triangles:
        if is_possible(sides):
            result += 1
    return result


def run(stream, test=False, draw=False):
    triangles = parse(stream)

    result1 = count_possible(triangles)

    verticals = reparse(triangles)
    result2 = count_possible(verticals)

    return (result1, result2)
