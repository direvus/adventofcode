"""assembly.py - Utility module for assembly-style interpreters.

Callers should extend the Computer abstract base class, populating the
`instructions` attribute with a mapping of opcodes to callables and the
`registers` attribute with a mutable mapping of register names to initial
values.

The instruction callables will generally be methods on the concrete Computer
class, so that they can modify the registers of the Computer object internally.
"""


class Computer:
    counter = 0
    pointer = 0
    registers = {}
    instructions = {}
    program = []
    halt = False

    def __init__(self, registers=None, instructions=None):
        if registers:
            self.registers = registers
        if instructions:
            self.instructions = instructions

    def load_program(self, program):
        """Load a program into this Computer.

        The `program` argument should be structured as an iterable of
        (opcode, operands) tuples.
        """
        self.program = tuple(program)

    def do_noop(self, *args):
        return None

    def do_instruction(self):
        """Execute the instruction at the current instruction pointer.

        Afterwards, the instruction pointer will be advanced by the return
        value of the instruction call, or else by 1 if the call does not return
        a value.

        In any case, return the result of the instruction.
        """
        opcode, operands = self.program[self.pointer]
        fn = self.instructions[opcode]
        result = fn(*operands)

        if result is None:
            self.pointer += 1
        else:
            self.pointer += result
        self.counter += 1

        return result

    def run(self):
        """Execute instructions until the computer halts.

        The computer can halt either by some instruction setting its `halt`
        property to a truthy value, or by the instruction pointer pointing
        outside of the bounds of the program.
        """
        self.pointer = 0
        self.counter = 0
        size = len(self.program)
        while self.pointer >= 0 and self.pointer < size and not self.halt:
            self.do_instruction()
