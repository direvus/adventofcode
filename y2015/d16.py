REQS = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1,
        }


def parse(stream) -> list[dict]:
    result = []
    for line in stream:
        line = line.strip()
        _, counts = line.split(': ', maxsplit=1)
        aunt = {}
        counts = counts.split(', ')
        for count in counts:
            k, v = count.split(': ')
            aunt[k] = int(v)
        result.append(aunt)
    return result


def matches(aunt: dict, reqs: dict, ranges: bool) -> bool:
    for k, v in reqs.items():
        if k not in aunt:
            continue
        if ranges and k in {'cats', 'trees', 'pomeranians', 'goldfish'}:
            if k in {'cats', 'trees'} and aunt[k] <= v:
                return False
            if k in {'pomeranians', 'goldfish'} and aunt[k] >= v:
                return False

        elif aunt[k] != v:
            return False
    return True


def find_aunt(
        aunts: list[dict],
        reqs: dict,
        ranges: bool = False
        ) -> int | None:
    for i, aunt in enumerate(aunts):
        for k, v in reqs.items():
            if matches(aunt, reqs, ranges):
                return i + 1
    return None


def run(stream, test=False):
    aunts = parse(stream)
    result1 = find_aunt(aunts, REQS)
    result2 = find_aunt(aunts, REQS, True)
    return (result1, result2)
