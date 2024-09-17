import logging  # noqa: F401


def swap_position(value: str, a: int, b: int) -> str:
    work = list(value)
    work[a], work[b] = work[b], work[a]
    return ''.join(work)


def swap_letter(value: str, a: str, b: str) -> str:
    return swap_position(value, value.index(a), value.index(b))


def rotate_count(value: str, count: int) -> str:
    i = count % len(value)
    return value[-i:] + value[:-i]


def rotate_index(value: str, letter: str) -> str:
    index = value.index(letter)
    count = index + 1
    if index >= 4:
        count += 1
    return rotate_count(value, count)


def reverse_span(value: str, start: int, end: int) -> str:
    rev = ''.join(reversed(value[start:end + 1]))
    return value[:start] + rev + value[end + 1:]


def move_index(value: str, source: int, dest: int) -> str:
    work = list(value)
    ch = work.pop(source)
    work.insert(dest, ch)
    return ''.join(work)


def parse(stream) -> set:
    result = []
    for line in stream:
        words = line.strip().split()
        fn = None
        args = []
        match words[0]:
            case 'swap':
                match words[1]:
                    case 'position':
                        fn = swap_position
                        args = (int(words[2]), int(words[5]))
                    case 'letter':
                        fn = swap_letter
                        args = (words[2], words[5])
            case 'rotate':
                if words[1] == 'based':
                    fn = rotate_index
                    args = (words[6],)
                else:
                    fn = rotate_count
                    arg = int(words[2])
                    if words[1] == 'left':
                        arg = -arg
                    args = (arg,)
            case 'reverse':
                fn = reverse_span
                args = (int(words[2]), int(words[4]))
            case 'move':
                fn = move_index
                args = (int(words[2]), int(words[5]))
        result.append((fn, args))
    return tuple(result)


def scramble(value: str, program: tuple) -> str:
    result = value
    for fn, args in program:
        logging.debug(
                f"Executing {fn.__name__} on {result} with arguments {args}")
        result = fn(result, *args)
    return result


def run(stream, test: bool = False):
    password = 'abcde' if test else 'abcdefgh'
    program = parse(stream)
    logging.debug("Parsed the instructions as:")
    logging.debug(program)

    result1 = scramble(password, program)
    result2 = 0

    return (result1, result2)
