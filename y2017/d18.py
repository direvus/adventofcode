"""Advent of Code 2017

Day 18: Duet

https://adventofcode.com/2017/day/18
"""
import logging  # noqa: F401
import string
import threading
from collections import defaultdict
from io import StringIO
from queue import Queue, Empty

from util import timing


def parse_program(stream) -> tuple:
    program = []
    for line in stream:
        line = line.strip()
        words = line.split(' ')
        program.append((words[0], words[1:]))
    return program


class Computer:
    def __init__(self, name: str = ''):
        self.name = name
        self.counter = 0
        self.pointer = 0
        self.registers = defaultdict(lambda: 0)
        self.frequency = 0
        self.program = []
        self.output_queue = None
        self.halt = False

    def reset(self):
        self.counter = 0
        self.pointer = 0
        self.frequency = 0
        self.halt = False
        self.registers.clear()

    def stop(self):
        self.halt = True

    def get_value(self, value: str) -> int:
        """Get the value for a split-type operand.

        The value can either be an integer literal, or a reference to a
        register. If it's an integer literal, return that value as an integer.
        If it's a register reference, return the value held in that register.
        """
        if value in string.ascii_lowercase:
            return self.registers[value]
        return int(value)

    def parse(self, stream) -> tuple:
        self.program = parse_program(stream)
        return self.program

    def send(self, value):
        self.frequency = value

    def recv(self) -> int:
        value = self.frequency
        if self.output_queue is not None:
            self.output_queue.put(value)

    def do_rcv(self, operands):
        testval = self.get_value(operands[0])
        if testval != 0:
            self.recv()

    def do_instruction(self, instruction, operands) -> None:
        """Execute one instruction on the Computer.

        Modifies the Computer's instruction pointer directly.
        """
        offset = 1
        match instruction:
            case 'snd':
                value = self.get_value(operands[0])
                self.send(value)
            case 'set':
                reg, value = operands
                self.registers[reg] = self.get_value(value)
            case 'add':
                reg, value = operands
                self.registers[reg] += self.get_value(value)
            case 'mul':
                reg, value = operands
                self.registers[reg] *= self.get_value(value)
            case 'mod':
                reg, value = operands
                self.registers[reg] %= self.get_value(value)
            case 'jgz':
                testval = self.get_value(operands[0])
                if testval > 0:
                    offset = self.get_value(operands[1])
            case 'rcv':
                self.do_rcv(operands)
        self.pointer += offset

    def run_program(self):
        """Run the current program until the Computer halts.

        Each do_instruction() call will modify the instruction pointer.  The
        Computer halts when that pointer points outside of the program space,
        or when the `halt` property is truthy.

        Any non-None return value from do_instruction() will be placed in the
        output queue.
        """
        self.pointer = 0
        self.counter = 0
        length = len(self.program)
        while not self.halt and self.pointer >= 0 and self.pointer < length:
            index = self.pointer
            inst, ops = self.program[self.pointer]
            self.do_instruction(inst, ops)

            self.counter += 1
            continue
            logging.debug(
                    f"{self.name} {self.counter:4d} {index:4d} "
                    f"{inst} \\[{', '.join(ops):6s}] -> "
                    f"{dict(self.registers)}")


class DuetComputer(Computer):
    status: str
    input_queue: Queue
    send_counter: int

    def __init__(self, name: str = ''):
        super().__init__(name)
        self.input_queue = None
        self.send_counter = 0
        self.status = 'READY'

    def do_rcv(self, operands):
        # The duet version is not conditional, it always runs. The operand
        # gives the register to store the received value into.
        value = self.recv()
        if value is not None:
            self.registers[operands[0]] = value

    def send(self, value: int):
        self.status = 'SENDWAIT'
        self.output_queue.put(value)
        self.send_counter += 1
        self.status = 'RUNNING'

    def recv(self) -> int | None:
        self.status = 'RECVWAIT'
        while not self.halt:
            try:
                value = self.input_queue.get(timeout=0.05)
                self.input_queue.task_done()
                self.status = 'RUNNING'
                return value
            except Empty:
                pass


class Duet:
    def __init__(self):
        a = DuetComputer('A')
        b = DuetComputer('B')

        a.registers['p'] = 0
        b.registers['p'] = 1

        self.aq = Queue()
        self.bq = Queue()

        a.input_queue = self.aq
        a.output_queue = self.bq

        b.input_queue = self.bq
        b.output_queue = self.aq

        self.a = a
        self.b = b

    def load_program(self, program):
        self.a.program = tuple(program)
        self.b.program = tuple(program)

    def run(self):
        """Run both computers.

        Keep running until both computers halt on their own, or until all
        remaining live computers are waiting to receive.

        Return the number of times that the B computer sent data.
        """
        t1 = threading.Thread(target=self.a.run_program)
        t2 = threading.Thread(target=self.b.run_program)

        t1.start()
        t2.start()

        timeout = 0.05
        stop = False

        while not stop and (t1.is_alive() or t2.is_alive()):
            t1.join(timeout=timeout)
            t2.join(timeout=timeout)

            dead1 = not t1.is_alive() or (
                    self.a.status == 'RECVWAIT' and self.aq.empty())
            dead2 = not t2.is_alive() or (
                    self.b.status == 'RECVWAIT' and self.bq.empty())

            if dead1 and dead2:
                # All living threads are in RECVWAIT, looks like a deadlock
                logging.debug("Deadlock detected")
                stop = True
        self.a.stop()
        self.b.stop()
        logging.debug(
                f"{self.a.name} {self.a.status} "
                f"{self.a.counter:4d} {self.a.send_counter} "
                f"{dict(self.a.registers)}")
        logging.debug(
                f"{self.b.name} {self.b.status} "
                f"{self.b.counter:4d} {self.b.send_counter} "
                f"{dict(self.b.registers)}")
        return self.b.send_counter


def run(stream, test: bool = False):
    with timing("Part 1"):
        comp = Computer()
        comp.parse(stream)
        q = Queue()
        comp.output_queue = q
        t = threading.Thread(target=comp.run_program)
        t.start()
        result1 = q.get()
        comp.stop()
        q.task_done()

    with timing("Part 2"):
        duet = Duet()
        prog = comp.program
        if test:
            s = StringIO("""snd 1
                    snd 2
                    snd p
                    rcv a
                    rcv b
                    rcv c
                    rcv d
                    """)
            prog = parse_program(s)
        duet.load_program(prog)

        result2 = duet.run()

    return (result1, result2)
