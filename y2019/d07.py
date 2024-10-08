"""Advent of Code 2019

Day 7: Amplification Circuit

https://adventofcode.com/2019/day/7
"""
import logging  # noqa: F401
from itertools import permutations

from util import NINF, timing
from y2019.intcode import Computer


class Chain:
    def __init__(self, amplifiers=None):
        self.amplifiers = list(amplifiers)

    def reset(self):
        for amp in self.amplifiers:
            amp.reset()

    def run(self, phases: tuple[int]) -> int:
        signal = 0
        for i in range(len(phases)):
            amp = self.amplifiers[i]
            (signal,) = amp.run((phases[i], signal))
        return signal

    def run_loop(self, phases: tuple[int]) -> int:
        for i in range(len(phases)):
            amp = self.amplifiers[i]
            amp.add_input(phases[i])

        signal = 0
        i = 0
        length = len(self.amplifiers)
        try:
            while not self.amplifiers[-1].halt:
                amp = self.amplifiers[i % length]
                amp.add_input(signal)
                signal = next(amp.generate())
                i += 1
        except StopIteration:
            pass
        return signal

    def find_highest_signal(self):
        best = NINF
        for phases in permutations(range(5)):
            self.reset()
            signal = self.run(phases)
            if signal > best:
                best = signal
        return best

    def find_highest_signal_loop(self):
        best = NINF
        for phases in permutations(range(5, 10)):
            self.reset()
            signal = self.run_loop(phases)
            logging.debug(f"{phases} produced {signal}")
            if signal > best:
                best = signal
        return best


def parse(stream) -> Chain:
    comp = Computer()
    comp.parse(stream)

    amps = [comp]
    for _ in range(4):
        amps.append(comp.clone())
    return Chain(amps)


def run(stream, test: bool = False):
    with timing("Part 1"):
        chain = parse(stream)
        result1 = chain.find_highest_signal()

    with timing("Part 2"):
        if test:
            chain = parse(
                    "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
                    "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
        else:
            chain.reset()
        result2 = chain.find_highest_signal_loop()

    return (result1, result2)
