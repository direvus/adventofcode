from ctypes import c_ushort


class Circuit:
    def __init__(self):
        self.signals = {}
        self.sources = {}

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            lhs, dest = line.split(' -> ')
            src = lhs.split()
            self.sources[dest] = src

    def run_wire(self, wire: str) -> int:
        if wire.isdigit():
            return int(wire)
        if wire in self.signals:
            return self.signals[wire]
        source = self.sources[wire]
        # NOT is the only unary gate
        if len(source) == 1:
            signal = self.run_wire(source[0])
        elif source[0] == 'NOT':
            value = self.run_wire(source[1])
            signal = c_ushort(~value).value
        elif source[1] == 'AND':
            a = self.run_wire(source[0])
            b = self.run_wire(source[2])
            signal = a & b
        elif source[1] == 'OR':
            a = self.run_wire(source[0])
            b = self.run_wire(source[2])
            signal = a | b
        elif source[1] == 'LSHIFT':
            a = self.run_wire(source[0])
            b = int(source[2])
            signal = a << b
        elif source[1] == 'RSHIFT':
            a = self.run_wire(source[0])
            b = int(source[2])
            signal = a >> b
        self.signals[wire] = signal
        return signal

    def run(self):
        for wire in self.sources:
            self.run_wire(wire)


def run(stream, test=False):
    wire = 'i' if test else 'a'
    result2 = 0
    circuit = Circuit()
    circuit.parse(stream)
    result1 = circuit.run_wire(wire)

    if not test:
        # There's no Part 2 for the test input
        circuit.signals = {'b': result1}
        result2 = circuit.run_wire(wire)

    return (result1, result2)
