import logging
from io import StringIO


def parse(stream) -> list:
    return stream.readline().strip()


def generate_checksum(data: str) -> str:
    check = data
    while len(check) % 2 == 0:
        s = StringIO()
        for i in range(0, len(check) - 1, 2):
            s.write('1' if check[i] == check[i + 1] else '0')
        check = s.getvalue()
    logging.debug(f"Finished making checksum with length {len(check)}")
    return check


def generate_data(data: str, length: int) -> tuple:
    while len(data) < length:
        s = StringIO()
        s.write(data)
        s.write('0')
        for ch in reversed(data):
            s.write('0' if ch == '1' else '1')
        data = s.getvalue()
    check = generate_checksum(data[:length])
    return data, check


def run(stream, test=False, draw=False):
    init = parse(stream)
    length = 20 if test else 272
    length2 = 200 if test else 35651584
    logging.debug(f"Initial state = {init}")
    logging.debug(f"Target length = {length}")

    _, result1 = generate_data(init, length)
    _, result2 = generate_data(init, length2)

    return (result1, result2)
