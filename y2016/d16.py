import logging


def parse(stream) -> list:
    return stream.readline().strip()


def generate_checksum(data: str) -> str:
    check = data
    while len(check) % 2 == 0:
        check = ''.join(
                str(int(check[i] == check[i + 1]))
                for i in range(0, len(check) - 1, 2))
    logging.debug(f"Finished making checksum with length {len(check)}")
    return check


def generate_data(data: str, length: int) -> tuple:
    while len(data) < length:
        a = data
        b = ''.join('0' if x == '1' else '1' for x in reversed(data))
        data = a + '0' + b
    check = generate_checksum(data[:length])
    return data, check


def run(stream, test=False, draw=False):
    init = parse(stream)
    length = 20 if test else 272
    logging.debug(f"Initial state = {init}")
    logging.debug(f"Target length = {length}")

    _, result1 = generate_data(init, length)
    _, result2 = generate_data(init, 35651584)

    return (result1, result2)
