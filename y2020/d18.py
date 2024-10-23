"""Advent of Code 2020

Day 18: Operation Order

https://adventofcode.com/2020/day/18
"""
import logging  # noqa: F401
from operator import add, mul

from util import timing


OPERATORS = {'+': add, '*': mul}


def tokenise(text: str):
    """Lex out tokens from a string source.

    The function acts as a generator, yielding each token as it is lexed. Each
    of the yielded tokens are tuples, the first element is a symbol name, and
    the optional second element is an attribute value for the symbol.
    """
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
            yield (ch,)
            i += 1
            continue

        if ch.isdigit():
            j = i + 1
            while j < length and text[j].isdigit():
                j += 1
            yield ('int', int(text[i:j]))
            i = j
            continue

        raise ValueError(f"Unrecognised symbol `{ch}` at position {i}")


class Expr:
    def __init__(self):
        self.op = None
        self.left = None
        self.right = None

    def __str__(self):
        return f'{self.left} {self.op.__name__} {self.right}'

    def evaluate(self):
        left = self.left
        if isinstance(left, Expr):
            left = left.evaluate()

        right = self.right
        if isinstance(right, Expr):
            right = right.evaluate()
        return self.op(left, right)


class ArithmeticParser:
    """A parser for simple arithmetic grammar with no operator precedence.

    Supports the + and * operators on non-negative integers only.

    Values bind to operators left-associatively and the operators have equal
    precedence.
    """
    def __init__(self, tokens):
        self.tokens = tuple(tokens)
        self.pointer = 0

    def get_symbol(self) -> str:
        if self.pointer >= len(self.tokens):
            return None
        return self.tokens[self.pointer][0]

    def read_token(self, symbol: str):
        token = self.tokens[self.pointer]
        if token[0] != symbol:
            raise ValueError(
                    f"Expected {symbol} at token {self.pointer}, got "
                    f"{token} instead.")
        self.pointer += 1
        if len(token) > 1:
            return token[1]

    def parse_int(self):
        value = self.read_token('int')
        return value

    def parse_term(self):
        match self.get_symbol():
            case '(':
                self.read_token('(')
                expr = self.parse_expr()
                self.read_token(')')
                return expr
            case 'int':
                return self.parse_int()
            case _:
                raise ValueError(
                        f"Expected an integer or `(` at token {self.pointer}, "
                        f"got {self.get_symbol()} instead.")

    def parse_expr_rhs(self, lhs: Expr | int):
        match self.get_symbol():
            case '+' | '*':
                symbol = self.get_symbol()
                self.read_token(symbol)
                expr = Expr()
                expr.left = lhs
                expr.op = OPERATORS[symbol]
                expr.right = self.parse_term()
                return self.parse_expr_rhs(expr)
            case _:
                return lhs

    def parse_expr(self):
        left = self.parse_term()
        expr = self.parse_expr_rhs(left)
        return expr

    def parse(self):
        return self.parse_expr()


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        if line == '':
            continue
        tokens = tuple(tokenise(line))
        result.append(tokens)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        token_list = parse(stream)
        result1 = 0
        for tokens in token_list:
            parser = ArithmeticParser(tokens)
            expr = parser.parse()
            result1 += expr.evaluate()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
