import re
from collections import defaultdict


PATTERN = re.compile(r'^([a-z-]+)-(\d+)\[([a-z]+)\]$')


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        m = PATTERN.match(line)
        name, sector, check = m.groups()
        result.append((name, int(sector), check))
    return result


def generate_checksum(name: str) -> str:
    counts = defaultdict(lambda: 0)
    for ch in name.replace('-', ''):
        counts[ch] += 1
    letters = [k for k in counts.keys()]
    letters.sort(key=lambda x: (-counts[x], x))
    return ''.join(letters[:5])


def is_valid(name: str, checksum: str) -> bool:
    return checksum == generate_checksum(name)


def get_valid_sum(rooms: list) -> int:
    result = 0
    for name, sector, check in rooms:
        if is_valid(name, check):
            result += sector
    return result


def rotate(letter: str, count: int) -> str:
    a = ord('a')
    value = ord(letter) + count - a
    value = a + value % 26
    return chr(value)


def decrypt(name: str, sector: int) -> str:
    result = []
    for ch in name:
        if ch == '-':
            result.append(' ')
        else:
            result.append(rotate(ch, sector))
    return ''.join(result)


def find_north_pole_objects(rooms: list) -> int | None:
    for name, sector, _ in rooms:
        clearname = decrypt(name, sector)
        if clearname == 'northpole object storage':
            return sector


def run(stream, test=False, draw=False):
    rooms = parse(stream)

    result1 = get_valid_sum(rooms)

    if test:
        room = rooms[-1]
        result2 = decrypt(room[0], room[1])
    else:
        result2 = find_north_pole_objects(rooms)

    return (result1, result2)
