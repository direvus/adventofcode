def move(pos, ch):
    y, x = pos
    match ch:
        case '<':
            return y, x - 1
        case '>':
            return y, x + 1
        case '^':
            return y - 1, x
        case 'v':
            return y + 1, x


def run(stream, test=False):
    line = stream.readline().strip()
    pos = (0, 0)
    locs = {(0, 0)}
    for ch in line:
        pos = move(pos, ch)
        locs.add(pos)
    result1 = len(locs)

    pos1 = (0, 0)
    pos2 = (0, 0)
    locs = {(0, 0)}
    for i in range(0, len(line), 2):
        pos1 = move(pos1, line[i])
        pos2 = move(pos2, line[i + 1])
        locs.add(pos1)
        locs.add(pos2)
    result2 = len(locs)
    return (result1, result2)
