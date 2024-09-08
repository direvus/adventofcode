from ast import literal_eval


def get_string_length(literal: str) -> int:
    s = literal_eval(literal)
    return len(s)


def get_repr(source: str) -> str:
    result = ['"']
    for ch in source:
        if ch == '\\':
            result.append('\\\\')
        elif ch == '"':
            result.append('\\"')
        else:
            result.append(ch)
    result.append('"')
    return ''.join(result)


def run(stream, test=False):
    result1 = 0
    result2 = 0
    for line in stream:
        line = line.strip()
        linelength = len(line)
        strlength = get_string_length(line)
        result1 += linelength - strlength
        r = get_repr(line)
        replength = len(r)
        result2 += replength - linelength

    return (result1, result2)
