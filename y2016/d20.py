import logging

from spans import SpanSet


def parse(stream) -> SpanSet:
    spans = SpanSet()
    for line in stream:
        a, b = sorted(int(x) for x in line.strip().split('-'))
        spans.add_span((a, b))
    return spans


def get_spans_total(spans: set) -> int:
    """Return the number of distinct values enclosed by the set of spans.

    The spans must already be in simple form (no overlaps).
    """
    return sum(high - low + 1 for low, high in spans)


def get_lowest_value(blocks: SpanSet) -> int:
    """Get the lowest non-negative integer that is not blocked."""
    i = 0
    for low, high in sorted(blocks.spans):
        if i < low:
            return i
        i = high + 1
    return i


def run(stream, test: bool = False):
    blocks = parse(stream)
    logging.debug(f"Simplified blocklist is {blocks}")

    result1 = get_lowest_value(blocks)

    totalspan = (0, 12) if test else (0, 4294967295)
    addr = SpanSet({totalspan})
    logging.debug(f"Overall address space: {addr}")
    remain = addr - blocks
    logging.debug(f"Remaining spans: {remain}")
    result2 = remain.total

    return (result1, result2)
