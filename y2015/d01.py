def run(stream, test=False):
    line = stream.readline().strip()
    result1 = 0
    result2 = None
    for i, ch in enumerate(line):
        if ch == '(':
            result1 += 1
        elif ch == ')':
            result1 -= 1
        if result2 is None and result1 < 0:
            result2 = i + 1

    return (result1, result2)
