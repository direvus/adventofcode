def look_and_say(seq: str, count: int) -> str:
    for _ in range(count):
        ints = [int(x) for x in seq]
        run = 0
        prev = None
        runs = []
        for n in ints:
            if n != prev:
                if run > 0:
                    runs.extend((run, prev))
                prev = n
                run = 1
            else:
                run += 1
        if run > 0:
            runs.extend((run, prev))
        seq = ''.join([str(x) for x in runs])
    return seq


def parse(stream) -> list[int]:
    line = stream.readline().strip()
    return line


def run(stream, test=False):
    seq = parse(stream)

    result1 = len(look_and_say(seq, 40))
    result2 = len(look_and_say(seq, 50))

    return (result1, result2)
