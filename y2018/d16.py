"""Advent of Code 2018

Day 16: Chronal Classification

https://adventofcode.com/2018/day/16
"""
import logging  # noqa: F401

from util import timing


OPCODES = (
        'addr',
        'addi',
        'mulr',
        'muli',
        'banr',
        'bani',
        'borr',
        'bori',
        'setr',
        'seti',
        'gtir',
        'gtri',
        'gtrr',
        'eqir',
        'eqri',
        'eqrr',
        )


def parse(stream) -> tuple:
    samples = []
    line = stream.readline().strip()
    while line:
        part = line[9:-1]
        inputs = tuple(int(x) for x in part.split(','))

        line = stream.readline().strip()
        code = tuple(int(x) for x in line.split())

        line = stream.readline().strip()
        part = line[9:-1]
        outputs = tuple(int(x) for x in part.split(','))

        samples.append((inputs, code, outputs))
        # Consume one blank line
        line = stream.readline().strip()
        line = stream.readline().strip()

    # Consume any more blank lines
    while not line:
        line = stream.readline()
        if line == '':
            # Reached the end of the stream
            return (tuple(samples), None)
        line = line.strip()

    # Next is the program
    program = []
    while line:
        program.append(tuple(int(x) for x in line.split()))
        line = stream.readline().strip()
    return (tuple(samples), tuple(program))


def do_instruction(registers: tuple, code: tuple) -> tuple:
    """Perform the instruction code on these register contents.

    Return the new register contents.
    """
    result = list(registers)
    match code[0]:
        case 'addr':
            result[code[3]] = registers[code[1]] + registers[code[2]]
        case 'addi':
            result[code[3]] = registers[code[1]] + code[2]
        case 'mulr':
            result[code[3]] = registers[code[1]] * registers[code[2]]
        case 'muli':
            result[code[3]] = registers[code[1]] * code[2]
        case 'banr':
            result[code[3]] = registers[code[1]] & registers[code[2]]
        case 'bani':
            result[code[3]] = registers[code[1]] & code[2]
        case 'borr':
            result[code[3]] = registers[code[1]] | registers[code[2]]
        case 'bori':
            result[code[3]] = registers[code[1]] | code[2]
        case 'setr':
            result[code[3]] = registers[code[1]]
        case 'seti':
            result[code[3]] = code[1]
        case 'gtir':
            result[code[3]] = int(code[1] > registers[code[2]])
        case 'gtri':
            result[code[3]] = int(registers[code[1]] > code[2])
        case 'gtrr':
            result[code[3]] = int(registers[code[1]] > registers[code[2]])
        case 'eqir':
            result[code[3]] = int(code[1] == registers[code[2]])
        case 'eqri':
            result[code[3]] = int(registers[code[1]] == code[2])
        case 'eqrr':
            result[code[3]] = int(registers[code[1]] == registers[code[2]])
    return tuple(result)


def find_matching_instructions(
        inputs: tuple, operands: tuple, output: tuple) -> set:
    """Return all the opcodes that could match these arguments."""
    result = set()
    for opcode in OPCODES:
        if do_instruction(inputs, (opcode,) + operands) == output:
            result.add(opcode)
    return result


def find_matching_threes(samples: tuple) -> int:
    """Return the number of samples that match three or more opcodes."""
    result = 0
    for inputs, code, outputs in samples:
        count = len(find_matching_instructions(inputs, code[1:], outputs))
        if count > 2:
            result += 1
    return result


def identify_opcodes(samples: tuple) -> dict:
    """Use the samples to identify opcode numbers.

    Return a mapping from opcode numbers to opcode strings.
    """
    opnums = {}
    opcodes = {k: set() for k in OPCODES}
    result = {}
    q = []
    for inputs, code, outputs in samples:
        opnum = code[0]
        if opnum in result:
            # Already figured this one out, move on.
            continue
        matches = find_matching_instructions(inputs, code[1:], outputs)
        if opnum in opnums:
            opnums[opnum] &= matches
        else:
            opnums[opnum] = matches

        for opcode in matches:
            if opcode in opcodes:
                opcodes[opcode].add(opnum)

        if len(opnums[opnum]) == 1:
            # We've narrowed it down to one possibility, lock it in.
            opcode = next(iter(opnums[opnum]))
            q.append((opnum, opcode))
            result[opnum] = opcode
            del opnums[opnum]
            del opcodes[opcode]

    while q:
        opnum, opcode = q.pop(0)
        result[opnum] = opcode
        opnums.pop(opnum, None)
        opcodes.pop(opcode, None)

        for k in opnums:
            opnums[k].discard(opcode)
            if len(opnums[k]) == 1:
                v = next(iter(opnums[k]))
                q.append((k, v))

        for k in opcodes:
            opcodes[k].discard(opnum)
            if len(opcodes[k]) == 1:
                v = next(iter(opcodes[k]))
                q.append((v, k))
    if len(result) != len(OPCODES):
        raise ValueError("Failed to identify all opcodes")
    return result


def codify_program(program: tuple, opcodes: dict) -> tuple:
    """Translate a program with numeric opcodes into one with strings."""
    return tuple((opcodes[x[0]],) + x[1:] for x in program)


def run_program(program: tuple) -> tuple:
    registers = [0, 0, 0, 0]
    for code in program:
        registers = do_instruction(registers, code)
    return tuple(registers)


def run(stream, test: bool = False):
    with timing("Part 1"):
        samples, program = parse(stream)
        result1 = find_matching_threes(samples)

    with timing("Part 2"):
        if test:
            # Can't really do Part 2 with the test input, since it's all about
            # identifying the opnum -> opcode mapping from samples, and the
            # test input is only one sample.
            result2 = 0
        else:
            opcodes = identify_opcodes(samples)
            program = codify_program(program, opcodes)
            registers = run_program(program)
            result2 = registers[0]

    return (result1, result2)
