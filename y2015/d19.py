def parse(stream) -> tuple[set, str]:
    reps = set()
    for line in stream:
        line = line.strip()
        if not line:
            break
        reps.add(tuple(line.split(' => ')))
    line = stream.readline().strip()
    return reps, line


def count_outputs(reps: set, molecule: str) -> int:
    outputs = set()
    for src, dst in reps:
        index = 0
        while src in molecule[index:]:
            index = molecule.index(src, index)
            output = molecule[:index] + dst + molecule[index + len(src):]
            outputs.add(output)
            index += 1
    return len(outputs)


def run(stream, test=False, draw=False):
    reps, molecule = parse(stream)
    result1 = count_outputs(reps, molecule)
    result2 = 0
    return (result1, result2)
