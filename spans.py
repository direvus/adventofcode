def simplify_spans(spans: set) -> set:
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


def subtract_span(a: tuple, b: tuple) -> set:
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


def subtract_spans(span: tuple, others: set) -> set:
    """Subtract set of spans `others` from single span `span`.

    Return a new set of spans that encloses all the values that are in `span`,
    but not in any of the spans in `others`.

    The spans in `others` must already be in simple form (no overlaps).
    """
    result = {span}
    if isinstance(others, SpanSet):
        others = others.spans
    for other in others:
        new = set()
        for span in result:
            new |= subtract_span(span, other)
        result = new
    return simplify_spans(result)


def span_overlaps(a: tuple, b: tuple) -> bool:
    return not (a[1] < b[0] or a[0] > b[1])


def span_contains(span: tuple, other: tuple) -> bool:
    return other[0] >= span[0] and other[1] <= span[1]


class SpanSet:
    def __init__(self, spans: tuple = None):
        self.spans = set()
        if spans:
            for span in spans:
                assert len(span) == 2
                a, b = sorted(span)
                self.spans.add((a, b))
        self.simplify()

    @property
    def total(self):
        """Return the number of distinct values enclosed by the spans."""
        return sum(high - low + 1 for low, high in self.spans)

    def simplify(self):
        self.spans = simplify_spans(self.spans)

    def add_span(self, span: tuple):
        self.spans.add(tuple(sorted(span)))
        self.simplify()

    def subtract(self, other: 'SpanSet') -> 'SpanSet':
        result = set()
        for span in self.spans:
            remain = subtract_spans(span, other)
            result |= remain
        return SpanSet(result)

    def __sub__(self, other):
        return self.subtract(other)

    def contains(self, value: int) -> bool:
        for low, high in self.spans:
            if low <= value and high >= value:
                return True
        return False

    def __str__(self) -> str:
        result = []
        for low, high in sorted(self.spans):
            if low == high:
                result.append(str(low))
            else:
                result.append(f"{low}-{high}")
        return ', '.join(result)
