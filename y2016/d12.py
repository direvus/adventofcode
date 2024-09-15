import logging


class Computer:
    def __init__(self):
        self.counter = 0
        self.pointer = 0
        self.registers = {k: 0 for k in {'a', 'b', 'c', 'd'}}

    def get_value(self, value: str) -> int:
        """Get the value for a split-type operand.

        The value can either be an integer literal, or a reference to a
        register. If it's an integer literal, return that value as an integer.
        If it's a register reference, return the value held in that register.
        """
        if value in self.registers:
            return self.registers[value]
        return int(value)

    def do_instruction(self, instruction, operands) -> int:
        """Execute one instruction on the Computer.

        Return the offset to the next instruction, relative to the current one.
        """
        # It's a feature of this particular instruction set that each
        # instruction has a unique first letter, so that's all we need to
        # compare.
        match instruction[0]:
            case 'c':
                src, dest = operands
                value = self.get_value(src)
                self.registers[dest] = value
            case 'i':
                self.registers[operands[0]] += 1
            case 'd':
                self.registers[operands[0]] -= 1
            case 'j':
                testval = self.get_value(operands[0])
                if testval != 0:
                    return int(operands[1])
        return 1

    def run_program(self, program: tuple):
        """Run this program until the Computer halts.

        Each instruction will supply an offset to the next instruction to
        execute. The Computer halts when that offset points outside of the
        program space.
        """
        self.pointer = 0
        self.counter = 0
        while self.pointer >= 0 and self.pointer < len(program):
            inst, ops = program[self.pointer]
            self.pointer += self.do_instruction(inst, ops)
            self.counter += 1


def parse_program(stream) -> tuple:
    program = []
    for line in stream:
        line = line.strip()
        words = line.split(' ')
        inst = words[0]
        operands = words[1:]
        program.append((inst, operands))
    return tuple(program)


def run(stream, test=False, draw=False):
    comp = Computer()
    prog = parse_program(stream)
    comp.run_program(prog)

    result1 = comp.registers['a']

    comp2 = Computer()
    comp2.registers['c'] = 1
    comp2.run_program(prog)
    result2 = comp2.registers['a']

    logging.info(f"Computer 2 executed {comp2.counter} instructions")

    return (result1, result2)
