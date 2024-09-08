import string


CHARS = string.ascii_lowercase
FORBIDDEN = {'i', 'o', 'l'}
STRAIGHTS = {
        'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'pqr', 'qrs',
        'rst', 'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz'}
PAIRS = {
        'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh',
        'jj', 'kk', 'mm', 'nn', 'pp', 'qq', 'rr', 'ss',
        'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz'}


def is_valid(value: str) -> bool:
    if FORBIDDEN & set(value):
        return False
    triples = {value[i - 3:i] for i in range(3, len(value) + 1)}
    if not triples & STRAIGHTS:
        return False
    doubles = {value[i - 2:i] for i in range(2, len(value) + 1)}
    return len(doubles & PAIRS) >= 2


def gen_next_string(value: str) -> str:
    chars = list(value)
    i = len(chars) - 1
    while i >= 0:
        ch = chars[i]
        if ch == CHARS[-1]:
            chars[i] = CHARS[0]
        else:
            index = CHARS.index(ch)
            chars[i] = CHARS[index + 1]
            break
        i -= 1
    return ''.join(chars)


def gen_next_valid_string(value: str) -> str:
    valid = False
    while not valid:
        value = gen_next_string(value)
        valid = is_valid(value)
    return value


def run(stream, test=False):
    value = stream.readline().strip()

    result1 = gen_next_valid_string(value)
    result2 = gen_next_valid_string(result1)

    return (result1, result2)
