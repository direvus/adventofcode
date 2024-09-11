import re
from collections import defaultdict
from copy import copy


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


def normalise_chomsky(reps: set) -> set:
    terminals = set()
    nonterminals = set()
    for a, b in reps:
        nonterminals.add(a)
        terminals |= set(b)
    terminals -= nonterminals

    # Skipping the START step because we know that the start symbol doesn't
    # appear on the right-hand side in the grammar.
    n = 1
    new = {}
    for t in terminals:
        new[t] = f'N{n}'
        n += 1

    # TERM: Eliminate rules that have non-solitary terminals
    result = copy(reps)
    for a, b in reps:
        terms = set(b) & terminals
        if terms and len(b) > 1:
            result.discard((a, b))
            for t in terms:
                result.add((new[t], (t,)))
                b = replace_atoms(b, t, new[t])
            result.add((a, b))
    # BIN: Now find rules that have more than 2 outputs, and just so I'm not
    # looping over the thing that I'm modifying, copy those into a separate
    # variable first.
    longs = [(a, b) for a, b in result if len(b) > 2]
    n = 1
    for a, b in longs:
        while len(b) > 2:
            # Rule has more than 2 outputs
            t = f'A{n}'
            n += 1
            result.discard((a, b))
            result.add((a, (b[0], t)))
            a = t
            b = b[1:]
            result.add((a, b))

    # DEL: Skipping this step because there are no empty rules
    empty = {a for a, b in result if len(b) == 0}
    assert not empty

    # UNIT: Eliminate unit rules
    nonterminals = {a for a, _ in result}
    units = [(a, b) for a, b in result if len(b) == 1 and b[0] in nonterminals]
    new = set()
    for a, b in units:
        result.discard((a, b))
        for r in result:
            if r[0] == b[0] and r not in units:
                new.add((a, r[1]))
    return result | new


def get_parse_trees(molecule: tuple, reps: set, start: str = 'e'):
    n = len(molecule)
    r = normalise_chomsky(reps)
    routes = defaultdict(lambda: False)  # (length, start, source): bool
    back = defaultdict(list)

    for i in range(n):
        for a, b in r:
            if b == molecule[i:i + 1]:
                routes[(1, i, a)] = True

    print(routes)
    for l in range(2, n + 1):
        for s in range(n - l + 1):
            for p in range(1, l):
                print(f'Considering a {l} long substring from {s}, partitioned at {p}: {molecule[s:s+l]}')
                for a, b in r:
                    if len(b) != 2:
                        continue
                    b, c = b
                    if routes[(p, s, b)] and routes[(l - p, s + p, c)]:
                        print(f"  Can be produced by {a} => {b},{c}")
                        routes[(l, s, a)] = True
                        back[(l, s, a)].append((p, b, c))
    print(routes)
    print(back)


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


def count_steps(target: tuple, reps: set, start: str = 'e') -> int:
    result = get_parse_trees(target, reps, start)


def run(stream, test=False, draw=False):
    reps, molecule = parse(stream)
    result1 = count_outputs(reps, molecule)
    result2 = count_steps(molecule, reps)
    return (result1, result2)
