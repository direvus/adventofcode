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
    """Return the number of distinct values enclosed by the set of spans.

    The spans must already be in simple form (no overlaps).
    """
    return sum(high - low + 1 for low, high in spans)


def diff_span(a: tuple, b: tuple) -> set:
    """Subtract span `b` from span `a`.

    Return a new set of spans that encloses all the values that are in `a`, but
    not in `b`.
    """
    if b[1] < a[0] or a[1] < b[0]:
        # Disjoint spans, return a set holding only the unmodified `a`.
        return {a}
    if a[0] >= b[0] and a[1] <= b[1]:
        # `a` is entirely covered by `b`, return the empty set.
        return set()
    if b[0] > a[0] and b[1] < a[1]:
        # `b` is entirely contained within `a`, divide `a` into two sets.
        return {
                (a[0], b[0] - 1),
                (b[1] + 1, a[1]),
                }
    if b[0] <= a[0]:
        return {(b[1] + 1, a[1])}
    else:
        return {(a[0], b[0] - 1)}


def diff_spans(span: tuple, others: set) -> set:
    """Subtract set of spans `others` from single span `span`.

    Return a new set of spans that encloses all the values that are in `span`,
    but not in any of the spans in `others`.

    The spans in `others` must already be in simple form (no overlaps).
    """
    result = {span}
    for other in others:
        new = set()
        for span in result:
            new |= diff_span(span, other)
        result = new
    return merge_spans(result)


def get_lowest_value(blocks: set) -> int:
    """Get the lowest non-negative integer that is not blocked.

    The blocklist `blocks` should be an iterable of ranges, where each range is
    described by a (low, high) inclusive tuple.
    """
    i = 0
    for low, high in sorted(blocks):
        if i < low:
            return i
        i = high + 1
    return i


def describe_spans(spans: set) -> str:
    """Return a string description of a set of spans.

    For example:

    >>> describe_spans({(5, 7), (9, 9), (11, 12)})
    5-7, 9, 11-12
    """
    result = []
    for low, high in sorted(spans):
        if low == high:
            result.append(str(low))
        else:
            result.append(f"{low}-{high}")
    return ', '.join(result)


def run(stream, test: bool = False):
    blocks = parse(stream)
    blocks = merge_spans(blocks)
    logging.debug(f"Simplified blocklist is {describe_spans(blocks)}")

    result1 = get_lowest_value(blocks)

    totalspan = (0, 12) if test else (0, 4294967295)
    logging.debug(f"Overall address space: {totalspan}")
    remain = diff_spans(totalspan, blocks)
    logging.debug(f"Remaining spans: {describe_spans(remain)}")
    result2 = get_spans_total(remain)

    return (result1, result2)
