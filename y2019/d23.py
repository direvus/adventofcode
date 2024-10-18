"""Advent of Code 2019

Day 23: Category Six

https://adventofcode.com/2019/day/23
"""
import logging  # noqa: F401
import queue
from collections import defaultdict
from threading import Thread

from util import timing
from y2019.intcode import Computer


class Nic(Computer):
    input_queue = None

    def read_input(self) -> int:
        try:
            value = self.input_queue.get(block=True, timeout=0.1)
            return value
        except queue.Empty:
            return -1
        except queue.ShutDown:
            self.halt = True
            return -1


class Network:
    def __init__(self, size: int, stream):
        self.size = size
        self.messages = defaultdict(queue.Queue)

        # Get the first Nic to parse the stream, all other Nics will load a
        # copy of its program.
        zero = Nic(stream)
        zero.name = '0'
        zero.input_queue = self.messages[0]
        zero.set_output_hook(self.send)
        self.nics = [zero]
        self.messages[0].put(0)
        self.result = None
        for i in range(1, size):
            comp = Nic()
            comp.name = str(i)
            comp.program = self.nics[0].program
            comp.load_program()
            comp.input_queue = self.messages[i]
            comp.set_output_hook(self.send)
            self.nics.append(comp)
            self.messages[i].put(i)

    def recv(self, addr: int) -> int:
        if self.messages[addr].empty():
            logging.debug(f"Returning -1 (empty message queue) for {addr}")
            return -1
        value = self.messages[addr].get()
        logging.debug(f"Returning {value} for {addr}")
        return value

    def send(self, outputs: list) -> None:
        if len(outputs) > 2:
            addr = outputs.pop(0)
            x = outputs.pop(0)
            y = outputs.pop(0)
            logging.debug(f"  -> {addr} {x} {y}")
            if addr == 255:
                self.result = y
            if addr < 50:
                self.messages[addr].put(x)
                self.messages[addr].put(y)

    def run(self):
        self.threads = [Thread(target=nic.run) for nic in self.nics]
        for thread in self.threads:
            thread.start()

        while self.result is None:
            self.threads[0].join(1)

        for nic in self.nics:
            nic.halt = True


def run(stream, test: bool = False):
    if test:
        # No way to test this one.
        return (0, 0)

    with timing("Part 1"):
        net = Network(50, stream)
        net.run()
        result1 = net.result

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
