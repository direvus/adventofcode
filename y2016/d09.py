import re


MARKER = re.compile(r'\((\d+)x(\d+)\)')


def parse(stream) -> str:
    data = stream.read().strip()
    return data


def decompress(data: str) -> str:
    """Decompress data using a run-length encoding scheme.

    The scheme introduces markers in the form `(AxB)` where `A` and `B` are
    both integers, A gives the length of the sequence after the closing
    bracket, and B gives the number of times to repeat it.

    Marker symbols within a repeated sequence are treated as normal literal
    characters.

    Whitespace in the source data is ignored.
    """
    result = []
    i = 0
    total_length = len(data)
    while i < total_length:
        ch = data[i]
        if ch.isspace():
            i += 1
            continue
        m = MARKER.match(data[i:])
        if m:
            length, count = (int(x) for x in m.groups())
            i = i + m.end()
            result.append(data[i:i + length] * count)
            i += length
        else:
            result.append(ch)
            i += 1
    return ''.join(result)


def get_decompressed_length_v2(data: str) -> int:
    """Get the length of the decompressed text according to version 2.

    Don't actually store the decompressed data, just keep track of how many
    bytes would be delivered and return it at the end.

    In the version 2 format, repeat markers can be nested.
    """
    result = 0
    i = 0
    total_length = len(data)
    while i < total_length:
        ch = data[i]
        if ch.isspace():
            i += 1
            continue
        m = MARKER.match(data[i:])
        if m:
            length, count = (int(x) for x in m.groups())
            i = i + m.end()
            result += get_decompressed_length_v2(data[i:i + length]) * count
            i += length
        else:
            result += 1
            i += 1
    return result


def run(stream, test=False, draw=False):
    data = parse(stream)
    decomp = decompress(data)

    result1 = len(decomp)
    result2 = get_decompressed_length_v2(data)
    return (result1, result2)
