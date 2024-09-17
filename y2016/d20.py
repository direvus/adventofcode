import logging


def parse(stream) -> set:
    spans = set()
    for line in stream:
        a, b = sorted(int(x) for x in line.strip().split('-'))
        spans.add((a, b))
    return spans


def merge_spans(spans: set) -> set:
    """Merge adjacent or overlapping spans together.

    Return a new minimal set of spans that enclose the same values as the
    original spans.
    """
    if len(spans) == 0:
        return set()
    spans = sorted(spans)
    result = set()
    prevlow, prevhigh = spans[0]
    for low, high in spans[1:]:
        if low > prevhigh + 1:
            # Disjoint, commit the previous one to the results
            result.add((prevlow, prevhigh))
            prevlow = low
            prevhigh = high
            continue
        # Must be adjacent or overlapped, either way extend the span so that it
        # covers both
        prevhigh = max(prevhigh, high)
    result.add((prevlow, prevhigh))
    return result


def get_spans_total(spans: set) -> int:
    """Return the number of value enclosed by the set of spans.

    The spans must already be in simple form (no overlaps).
    """
    return sum(high - low + 1 for low, high in spans)


def diff_spans(a: tuple, b: set) -> set:
    """Subtract set of spans `b` from single span `a`.

    Return a new set of spans that encloses all the values that are in `a`, but
    not in any of the spans in `b`.

    The spans in `b` must already be in simple form (no overlaps).
    """
    result = set()
    return result


def get_lowest_value(blocks: set) -> int:
    """Get the lowest non-negative integer that is not blocked.

    The blocklist `blocks` should be an iterable of ranges, where each range is
    described by a (low, high) inclusive tuple.
    """
    i = 0
    for low, high in sorted(blocks):
        logging.debug(f"Range {low} - {high} is blocked, checking {i}")
        if i < low:
            logging.debug(f"{i} is outside the range, return it")
            return i
        logging.debug(f"{i} is inside the range, return it")
        i = high + 1
    return i


def run(stream, test: bool = False):
    blocks = parse(stream)
    blocks = merge_spans(blocks)

    result1 = get_lowest_value(blocks)
    result2 = 0

    return (result1, result2)
