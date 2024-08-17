#!/usr/bin/env python
import sys
from collections import namedtuple

from util import timing


Condition = namedtuple('condition', ['key', 'operator', 'value'])
Rule = namedtuple('rule', ['cond', 'effect'])


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


if __name__ == '__main__':
    workflows, parts = parse_workflows(sys.stdin)

    # Part 1
    with timing("Part 1"):
        result = 0
        for part in parts:
            if process_part(workflows, part):
                result += sum(part.values())
    print(f"Result for Part 1 = {result} \n")
