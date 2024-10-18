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


class Nat:
    packet = None
    last = None


class Network:
    def __init__(self, size: int, stream, nat: bool = False):
        self.size = size
        self.result = None
        self.nat = None
        self.threads = []
        if nat:
            self.nat = Nat()
        self.messages = defaultdict(queue.Queue)

        # Get the first Nic to parse the stream, all other Nics will load a
        # copy of its program.
        zero = Nic(stream)
        zero.name = '0'
        zero.input_queue = self.messages[0]
        zero.set_output_hook(self.send)
        self.nics = [zero]

        for i in range(1, size):
            comp = Nic()
            comp.name = str(i)
            comp.program = self.nics[0].program
            comp.load_program()
            comp.input_queue = self.messages[i]
            comp.set_output_hook(self.send)
            self.nics.append(comp)

    def reset(self):
        self.result = None
        for nic in self.nics:
            nic.reset()

        # Drain all message queues
        for k in self.messages:
            q = self.messages[k]
            while not q.empty():
                try:
                    q.get(block=False)
                except queue.Empty:
                    pass

        if self.nat:
            self.nat.packet = None
            self.nat.last = None

    def recv(self, addr: int) -> int:
        if self.messages[addr].empty():
            return -1
        value = self.messages[addr].get()
        return value

    def send(self, outputs: list) -> None:
        if len(outputs) > 2:
            addr = outputs.pop(0)
            x = outputs.pop(0)
            y = outputs.pop(0)
            logging.debug(f"  -> {addr} {x} {y}")
            if addr == 255:
                # In non-NAT mode, the first packet sent to address 255 gives
                # the final result of the run. In NAT mode, the packet goes
                # into the NAT memory, and will get sent when the network is
                # idle.
                if self.nat:
                    self.nat.packet = (x, y)
                else:
                    self.result = y
            if addr < 50:
                self.messages[addr].put(x)
                self.messages[addr].put(y)

    def do_idle_check(self):
        if self.nat.packet is None:
            # No point continuing, we have nothing to send anyway.
            return

        # Is the network currently idle?
        if not all(q.empty() for q in self.messages.values()):
            return

        x, y = self.nat.packet
        logging.debug(f"Network is idle, -> 0 {x} {y}")
        if y == self.nat.last:
            # Sent the same Y value twice in a row, that's the final run
            # result.
            self.result = y
        self.messages[0].put(x)
        self.messages[0].put(y)
        self.nat.last = y

    def run(self):
        for i in range(self.size):
            self.messages[i].put(i)

        self.threads = [Thread(target=nic.run) for nic in self.nics]
        for thread in self.threads:
            thread.start()

        while self.result is None:
            self.threads[0].join(0.2)
            if self.nat:
                self.do_idle_check()

        # Signal all the NICs to stop processing
        for nic in self.nics:
            nic.halt = True

        # Wait for all threads to conclude
        for thread in self.threads:
            thread.join()


def run(stream, test: bool = False):
    if test:
        # No way to test this one.
        return (0, 0)

    with timing("Part 1"):
        net = Network(50, stream)
        net.run()
        result1 = net.result

    with timing("Part 2"):
        net.reset()
        # Switch on NAT mode for the second run
        net.nat = Nat()
        net.run()
        result2 = net.result

    return (result1, result2)
