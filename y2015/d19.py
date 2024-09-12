import re
from collections import defaultdict


INF = float('inf')
ATOM = re.compile(r'[A-Z][a-z]?')


def get_atoms(molecule: str) -> tuple[str]:
    return tuple(ATOM.findall(molecule))


def parse(stream) -> tuple[set, tuple]:
    reps = set()
    for line in stream:
        line = line.strip()
        if not line:
            break
        a, b = line.split(' => ')
        reps.add((a, get_atoms(b)))
    target = get_atoms(stream.readline().strip())
    return reps, target


def replace_atoms(molecule: tuple, atom: str, replacement: str) -> tuple:
    """Return a new molecule tuple by replacing all instances of an atom."""
    result = molecule
    index = 0
    while atom in result[index:]:
        index = result.index(atom, index)
        result = result[:index] + (replacement,) + result[index + 1:]
    return result


def parse_earley(molecule: tuple, reps: set, start: str = 'e'):
    """Parse a context-free grammar using an Earley algorithm.

    This is a modified version of Earley that runs the Scan step for
    non-terminal as well as terminal symbols, since the target string in this
    puzzle consists of a mixture.
    """
    state = defaultdict(set)
    symbols = set()
    gram = defaultdict(set)
    for a, b in reps:
        if a == start:
            state[0].add((a, b, 0, 0))
        gram[a].add(b)
        symbols |= {a} | set(b)
    nonterminals = set(gram.keys())

    length = len(molecule)
    for k in range(length + 1):
        q = list(state[k])
        while q:
            a, b, i, j = q.pop(0)
            if i < len(b):
                if b[i] in nonterminals:
                    # Prediction
                    for product in gram[b[i]]:
                        s = (b[i], product, 0, k)
                        if s not in state[k]:
                            state[k].add(s)
                            q.append(s)
                if k < length and b[i] == molecule[k]:
                    # Scanning
                    s = (a, b, i + 1, j)
                    state[k + 1].add(s)
            else:
                # Completion
                for s in state[j]:
                    if s[2] < len(s[1]) and s[1][s[2]] in nonterminals:
                        c = (s[0], s[1], s[2] + 1, s[3])
                        if c not in state[k]:
                            state[k].add(c)
                            q.append(c)
    finals = {s[0] for s in state[length]}
    return start in finals


def get_neighbours(molecule: tuple, reps: set) -> set[str]:
    outputs = set()
    for src, dst in reps:
        index = 0
        while src in molecule[index:]:
            index = molecule.index(src, index)
            output = molecule[:index] + dst + molecule[index + 1:]
            outputs.add(output)
            index += 1
    return outputs


def count_outputs(reps: set, molecule: tuple) -> int:
    outputs = get_neighbours(molecule, reps)
    return len(outputs)


def get_index(molecule: tuple, search: tuple) -> int | None:
    for i in range(len(molecule) - len(search) + 1):
        if molecule[i:i + len(search)] == search:
            return i
    return None


def replace_longest(molecule: tuple, reps: set, start: str = 'e') -> int:
    """Iteratively replace the longest matching rule to get back to the start.

    Starting with the target molecule, we try to apply each rule in reverse,
    from the longest to the shortest, and keep going until we reach the
    starting string.

    Return the total number of replacements made.
    """
    result = 0
    work = molecule
    reps = list(reps)
    reps.sort(key=lambda x: len(x[1]), reverse=True)
    while work != (start,):
        curr = result
        for a, b in reps:
            i = get_index(work, b)
            if i is not None:
                work = work[:i] + (a,) + work[i + len(b):]
                i = get_index(work, b)
                result += 1
                break
        if curr == result:
            raise ValueError(f"No more replacements for {work}")
    return result


def count_steps(target: tuple, reps: set, start: str = 'e') -> int:
    return replace_longest(target, reps, start)


def run(stream, test=False, draw=False):
    reps, molecule = parse(stream)
    result1 = count_outputs(reps, molecule)
    result2 = count_steps(molecule, reps)
    return (result1, result2)
