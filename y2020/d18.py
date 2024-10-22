"""Advent of Code 2020

Day 18: Operation Order

https://adventofcode.com/2020/day/18
"""
import logging  # noqa: F401
from collections import deque
from operator import add, mul

from util import timing


def tokenise(text: str) -> deque:
    result = deque()
    i = 0
    length = len(text)
    while i < length:
        # Skip over whitespace
        if text[i].isspace():
            i += 1
            continue
        ch = text[i]
        if ch in '()+*':
            # These symbols are always standalone tokens
            result.append(ch)
            i += 1
            continue

        if ch.isdigit():
            j = i
            while j < length and text[j].isdigit():
                j += 1
            result.append(int(text[i:j]))
            i = j
            continue

        raise ValueError(f"Unrecognised symbol `{ch}` at position {i}")
    return result


class Expr:
    def __init__(self):
        self.op = None
        self.left = None
        self.right = None

    def evaluate(self):
        left = self.left
        if isinstance(left, Expr):
            left = left.evaluate()

        right = self.right
        if isinstance(right, Expr):
            right = right.evaluate()
        return self.op(left, right)


def parse_expr(tokens: deque) -> Expr:
    """Parse one expression from a list of tokens.

    The result is an Expr object. Tokens that are consumed by parsing are
    removed from the list.
    """
    expr = Expr()
    expr.left = parse_value(tokens)
    expr.op = parse_operator(tokens)
    expr.right = parse_value(tokens)
    return expr


def parse_value(tokens: deque) -> Expr | int:
    """Parse an expression value from a list of tokens.

    The result is either a nested expression, or a simple integer value. Tokens
    that are consumed by parsing are removed from the list.
    """
    tok = tokens.popleft()
    if isinstance(tok, int):
        return tok

    if tok == '(':
        expr = parse_expr(tokens)
        while tokens:
            if tokens[0] == ')':
                tokens.popleft()
                return expr
            new = Expr()
            new.left = expr
            new.op = parse_operator(tokens)
            new.right = parse_value(tokens)
            expr = new
        raise ValueError("Unterminated `(` in tokens.")
    raise ValueError(
            f"Unexpected `{tok}` in expression value, "
            "expected a literal value or a nested expression.")


def parse_operator(tokens: deque):
    tok = tokens.popleft()
    if tok == '+':
        return add

    if tok == '*':
        return mul

    raise ValueError(
            f"Unexpected `{tok}` in expression operator, expected "
            "`+` or `*`.")


def parse_all(tokens: deque) -> Expr:
    result = parse_expr(tokens)
    while tokens:
        expr = Expr()
        expr.left = result
        expr.op = parse_operator(tokens)
        expr.right = parse_value(tokens)
        result = expr
    return result


def parse(stream) -> list[Expr]:
    result = []
    for line in stream:
        line = line.strip()
        if line == '':
            continue
        tokens = tokenise(line)
        result.append(parse_all(tokens))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        exprs = parse(stream)
        result1 = sum(x.evaluate() for x in exprs)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
