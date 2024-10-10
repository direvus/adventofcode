from collections import defaultdict


class Computer:
    def __init__(self, program: str = ''):
        self.program = []
        self.memory = defaultdict(lambda: 0)
        self.halt = False
        self.pointer = 0
        self.relative_base = 0
        self.inputs = []
        self.input_hook = None
        self.outputs = []

        self.instructions = {
                99: self.do_halt,
                1: self.do_add,
                2: self.do_mul,
                3: self.do_input,
                4: self.do_output,
                5: self.do_jump_if_true,
                6: self.do_jump_if_false,
                7: self.do_less_than,
                8: self.do_equals,
                9: self.do_adjust_relative_base,
                }
        if program:
            self.parse(program)

    def parse(self, stream):
        if isinstance(stream, str):
            line = stream.strip()
        else:
            line = stream.readline().strip()
        self.program = tuple(int(x) for x in line.split(','))
        self.load_program()

    def load_program(self):
        self.memory.clear()
        self.memory.update({i: x for i, x in enumerate(self.program)})

    def reset(self):
        self.load_program()
        self.pointer = 0
        self.halt = False
        self.inputs = []
        self.outputs = []

    def clone(self):
        new = Computer()
        new.program = self.program
        new.load_program()
        return new

    def add_input(self, value: int):
        self.inputs.append(value)

    def add_inputs(self, values: tuple[int]):
        self.inputs.extend(values)

    def set_input_hook(self, fn):
        self.input_hook = fn

    def read_input(self) -> int:
        """Read a single input value.

        If `input_hook` has been set, we expect it to be a callable that can be
        called without arguments, and we call it to get the next input value.

        Otherwise, we take the first value off the input queue.

        If the computer doesn't have an input hook, and the queue is empty when
        we try to read an input, the program will crash.
        """
        if self.input_hook is None:
            return self.inputs.pop(0)
        return self.input_hook()

    def get_mode(self, modes: int, index: int) -> str:
        modes = str(modes)
        try:
            return modes[-index]
        except IndexError:
            return '0'

    def get_value(self, modes: int, index: int):
        value = self.memory[self.pointer + index]
        mode = self.get_mode(modes, index)
        match mode:
            case '0':
                return self.memory[value]
            case '1':
                return value
            case '2':
                addr = value + self.relative_base
                if addr < 0:
                    raise ValueError(f"Invalid address {addr}")
                return self.memory[addr]
        raise ValueError(f"Unknown parameter mode {mode}")

    def put_value(self, modes: int, index: int, value: int):
        addr = self.memory[self.pointer + index]
        mode = self.get_mode(modes, index)
        match mode:
            case '0':
                self.memory[addr] = value
                return
            case '2':
                addr += self.relative_base
                if addr < 0:
                    raise ValueError(f"Invalid address {addr}")
                self.memory[addr] = value
                return
        raise ValueError(f"Invalid mode for write: {mode}")

    def do_halt(self, modes: int):
        self.halt = True

    def do_add(self, modes: int):
        a = self.get_value(modes, 1)
        b = self.get_value(modes, 2)
        self.put_value(modes, 3, a + b)
        self.pointer += 4

    def do_mul(self, modes: int):
        a = self.get_value(modes, 1)
        b = self.get_value(modes, 2)
        self.put_value(modes, 3, a * b)
        self.pointer += 4

    def do_input(self, modes: int):
        v = self.read_input()
        self.put_value(modes, 1, v)
        self.pointer += 2

    def do_output(self, modes: int):
        v = self.get_value(modes, 1)
        self.outputs.append(v)
        self.pointer += 2

    def do_jump_if_true(self, modes: int):
        a = self.get_value(modes, 1)
        if a != 0:
            b = self.get_value(modes, 2)
            self.pointer = b
        else:
            self.pointer += 3

    def do_jump_if_false(self, modes: int):
        a = self.get_value(modes, 1)
        if a == 0:
            b = self.get_value(modes, 2)
            self.pointer = b
        else:
            self.pointer += 3

    def do_less_than(self, modes: int):
        a = self.get_value(modes, 1)
        b = self.get_value(modes, 2)
        self.put_value(modes, 3, int(a < b))
        self.pointer += 4

    def do_equals(self, modes: int):
        a = self.get_value(modes, 1)
        b = self.get_value(modes, 2)
        self.put_value(modes, 3, int(a == b))
        self.pointer += 4

    def do_adjust_relative_base(self, modes: int):
        a = self.get_value(modes, 1)
        self.relative_base += a
        self.pointer += 2

    def do_instruction(self):
        value = self.memory[self.pointer]
        modes, opcode = divmod(value, 100)
        if opcode not in self.instructions:
            raise ValueError(f"Unknown opcode {opcode} at {self.pointer}")
        self.instructions[opcode](modes)

    def run(self, inputs: tuple[int] = ()) -> tuple[int]:
        self.inputs.extend(list(inputs))
        while not self.halt:
            self.do_instruction()
        return tuple(self.outputs)

    def generate(self):
        while not self.halt:
            while not self.halt and not self.outputs:
                self.do_instruction()
            if self.outputs:
                yield self.outputs.pop(0)
