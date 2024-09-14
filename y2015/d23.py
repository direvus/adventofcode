class Computer:
    def __init__(self):
        self.registers = {
                'a': 0,
                'b': 0,
                }

    def do_instruction(self, instruction, operands) -> int:
        """Execute one instruction on the Computer.

        Return the offset to the next instruction, relative to the current one.
        """
        match instruction:
            case 'hlf':
                self.registers[operands[0]] //= 2
            case 'tpl':
                self.registers[operands[0]] *= 3
            case 'inc':
                self.registers[operands[0]] += 1
            case 'jmp':
                return int(operands[0])
            case 'jie':
                reg, off = operands
                if self.registers[reg] % 2 == 0:
                    return int(off)
            case 'jio':
                reg, off = operands
                if self.registers[reg] == 1:
                    return int(off)
        return 1

    def run_program(self, program: tuple):
        """Run this program until the Computer halts.

        Each instruction will supply an offset to the next instruction to
        execute. The Computer halts when that offset points outside of the
        program space.
        """
        i = 0  # Instruction pointer
        c = 0  # Instruction counter
        while i >= 0 and i < len(program):
            inst, ops = program[i]
            i += self.do_instruction(inst, ops)
            c += 1


def parse_program(stream) -> tuple:
    program = []
    for line in stream:
        line = line.strip()
        inst, ops = line.split(' ', maxsplit=1)
        operands = ops.split(', ')
        program.append((inst, operands))
    return tuple(program)


def run(stream, test=False, draw=False):
    comp = Computer()
    prog = parse_program(stream)
    comp.run_program(prog)

    read = 'a' if test else 'b'
    result1 = comp.registers[read]

    comp = Computer()
    comp.registers['a'] = 1
    comp.run_program(prog)
    result2 = comp.registers[read]

    return (result1, result2)
