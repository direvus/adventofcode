import logging  # noqa: F401

from util import timing


REVERSE_SHIFTS = {
        1: 0,
        3: 1,
        5: 2,
        7: 3,
        2: 4,
        4: 5,
        6: 6,
        0: 7,
        }


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


def unscramble(value: str, program: tuple) -> str:
    """Apply the reverse of each step in program, in reverse order."""
    result = value
    for fn, args in reversed(program):
        if fn == rotate_count:
            args = (-args[0],)
        elif fn == move_index:
            args = (args[1], args[0])
        elif fn == rotate_index:
            # This trick only works on passwords of length 8
            if len(result) != 8:
                raise ValueError(
                        "Can only reverse rotate_index on "
                        "strings that are exactly 8 characters long.")
            index = result.index(args[0])
            shift = REVERSE_SHIFTS[index] - index
            fn = rotate_count
            args = (shift,)

        # All the other functions can just be applied again with the same
        # arguments to reverse.

        logging.debug(
                f"Executing {fn.__name__} on {result} with arguments {args}")
        result = fn(result, *args)
    return result


def run(stream, test: bool = False):
    password = 'abcdefgh' if test else 'abcdefgh'
    program = parse(stream)
    logging.debug("Parsed the instructions as:")
    logging.debug(program)

    with timing("Part 1"):
        result1 = scramble(password, program)
    with timing("Part 2"):
        scrambled = 'fbdecgha' if test else 'fbgdceah'
        result2 = unscramble(scrambled, program)

    return (result1, result2)
