import assembly


def test_init():
    comp = assembly.Computer()
    assert comp.pointer == 0
    assert comp.counter == 0
    assert comp.registers == {}
    assert comp.instructions == {}


def test_init_registers():
    comp = assembly.Computer({'a': 0, 'b': 0})
    assert comp.pointer == 0
    assert comp.counter == 0
    assert comp.registers == {'a': 0, 'b': 0}
    assert comp.instructions == {}


def test_init_instructions():
    comp = assembly.Computer(None, {'nop': lambda: None})
    assert comp.pointer == 0
    assert comp.counter == 0
    assert comp.registers == {}
    assert 'nop' in comp.instructions
    assert comp.instructions['nop']() is None


def test_run_no_program():
    comp = assembly.Computer()
    comp.run()
    assert comp.pointer == 0
    assert comp.counter == 0


def test_load_program():
    comp = assembly.Computer(None, {'nop': lambda: None})
    program = [('nop', tuple())]
    comp.load_program(program)
    assert comp.program == (('nop', tuple()),)


def test_run():
    comp = assembly.Computer(None, {'nop': lambda: None})
    comp.load_program((('nop', tuple()),),)
    comp.run()
    assert comp.pointer == 1
    assert comp.counter == 1


def test_modify_register():
    class Computer(assembly.Computer):
        registers = {'x': 0}

        def __init__(self):
            self.instructions = {
                    'inc': self.do_increment,
                    }

        def do_increment(self, register):
            self.registers[register] += 1

    comp = Computer()
    comp.load_program((('inc', ('x',)),))
    comp.run()
    assert comp.pointer == 1
    assert comp.counter == 1
    assert comp.registers == {'x': 1}
