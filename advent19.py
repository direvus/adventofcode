#!/usr/bin/env python
import math
import sys
from collections import namedtuple

from util import timing


MIN_RATING = 1
MAX_RATING = 4000
RATINGS = 'xmas'
ALL_RATINGS = {
        k: frozenset(range(MIN_RATING, MAX_RATING + 1))
        for k in RATINGS}

Condition = namedtuple('condition', ['key', 'operator', 'value'])
Rule = namedtuple('rule', ['cond', 'effect'])
Branch = namedtuple('branch', ['cond', 'left', 'right'])


def parse_workflows(stream) -> tuple[dict, list]:
    workflows = {}
    for line in stream:
        line = line.strip()[:-1]
        if not line:
            break
        name, rules = line.split('{')
        parts = rules.split(',')
        rules = []
        for part in parts:
            if ':' in part:
                cond, effect = part.split(':')
                key = cond[0]
                operator = cond[1]
                value = int(cond[2:])
                cond = Condition(key, operator, value)
            else:
                cond = None
                effect = part
            rules.append(Rule(cond, effect))
        workflows[name] = rules

    parts = []
    for line in stream:
        line = line.strip()[1:-1]
        part = {}
        for spec in line.split(','):
            k, v = spec.split('=')
            part[k] = int(v)
        parts.append(part)
    return (workflows, parts)


def run_workflow(rules: list[Rule], part: dict) -> str:
    for cond, effect in rules:
        if cond is None:
            return effect
        k, op, target = cond
        v = part[k]
        if op == '<' and v < target:
            return effect
        if op == '>' and v > target:
            return effect
    raise RuntimeError("Reached end of ruleset without matching a rule")


def process_part(workflows: dict, part: dict) -> bool:
    workflow = 'in'
    while workflow not in {'A', 'R'}:
        rules = workflows[workflow]
        workflow = run_workflow(rules, part)
    return workflow == 'A'


def intersect_ranges(a: dict, b: dict) -> dict:
    result = {}
    for k in RATINGS:
        result[k] = a.get(k, set()) & b.get(k, set())
    return result


def union_ranges(a: dict, b: dict) -> dict:
    result = {}
    for k in RATINGS:
        result[k] = a.get(k, set()) | b.get(k, set())
    return result


def get_effect_ranges(effect: str | Branch) -> dict:
    if effect == 'A':
        return ALL_RATINGS
    if effect == 'R':
        return {}
    return get_ranges(effect)


def describe_ranges(ranges: dict) -> str:
    labels = []
    for k, v in ranges.items():
        if len(v) == MAX_RATING:
            labels.append(f"{k}: ALL")
            continue
        if len(v) == 0:
            labels.append(f"{k}: NONE")
            continue
        spans = []
        low = None
        high = None
        for i in range(MIN_RATING, MAX_RATING + 1):
            if i in v:
                if low is None:
                    low = i
                high = i
            elif low is not None:
                span = f"{low}-{high}" if low < high else str(low)
                spans.append(span)
                low = None
        if low is not None:
            spans.append(f"{low}-{high}")
        labels.append(f"{k}: {','.join(spans)}")
    return ', '.join(labels)


def get_ranges(tree: Branch) -> dict:
    key, operator, value = tree.cond
    left = ALL_RATINGS.copy()
    right = ALL_RATINGS.copy()
    if operator == '<':
        left[key] = set(range(MIN_RATING, value))
        right[key] = set(range(value, MAX_RATING + 1))
    else:
        left[key] = set(range(value + 1, MAX_RATING + 1))
        right[key] = set(range(MIN_RATING, value + 1))
    left = intersect_ranges(left, get_effect_ranges(tree.left))
    right = intersect_ranges(right, get_effect_ranges(tree.right))
    print(f"Evaluated {tree.cond}:")
    print(f"  L = {describe_ranges(left)}")
    print(f"  R = {describe_ranges(right)}")
    return union_ranges(left, right)


def get_total_combinations(tree: Branch) -> int:
    ranges = get_ranges(tree)
    print(describe_ranges(ranges))
    combos = []
    for r in ranges.values():
        length = len(r)
        if length > 0:
            combos.append(length)
    return math.prod(combos)


def make_tree(workflows: dict, name: str, index: int) -> Branch:
    rule = workflows[name][index]
    if rule.effect in {'A', 'R'}:
        effect = rule.effect
    else:
        effect = make_tree(workflows, rule.effect, 0)
    if rule.cond is None:
        return effect
    right = make_tree(workflows, name, index + 1)
    return Branch(rule.cond, effect, right)


if __name__ == '__main__':
    workflows, parts = parse_workflows(sys.stdin)

    # Part 1
    with timing("Part 1"):
        result = 0
        for part in parts:
            if process_part(workflows, part):
                result += sum(part.values())
    print(f"Result for Part 1 = {result} \n")

    # Part 2
    with timing("Part 2"):
        tree = make_tree(workflows, 'in', 0)
        result = get_total_combinations(tree)
    print(f"Result for Part 2 = {result} \n")
