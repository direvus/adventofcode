from collections import defaultdict


def parse(stream) -> list:
    results = []
    for line in stream:
        line = line.strip()
        results.append(line)
    return results


def get_message(packets: list) -> str:
    counts = [defaultdict(lambda: 0) for _ in range(len(packets[0]))]
    for packet in packets:
        for i, ch in enumerate(packet):
            counts[i][ch] += 1
    result = []
    for count in counts:
        letters = [k for k in count.keys()]
        letters.sort(key=lambda x: -count[x])
        result.append(letters[0])
    return ''.join(result)


def get_message2(packets: list) -> str:
    counts = [defaultdict(lambda: 0) for _ in range(len(packets[0]))]
    for packet in packets:
        for i, ch in enumerate(packet):
            counts[i][ch] += 1
    result = []
    for count in counts:
        letters = [k for k in count.keys()]
        letters.sort(key=lambda x: count[x])
        result.append(letters[0])
    return ''.join(result)


def run(stream, test=False, draw=False):
    packets = parse(stream)

    result1 = get_message(packets)
    result2 = get_message2(packets)

    return (result1, result2)
