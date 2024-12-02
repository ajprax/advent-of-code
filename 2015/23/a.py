from utils import *


@dataclass
class Half:
    register: str

    def execute(self, pointer, registers):
        registers[self.register] //= 2
        return pointer + 1, registers


@dataclass
class Triple:
    register: str

    def execute(self, pointer, registers):
        registers[self.register] *= 3
        return pointer + 1, registers


@dataclass
class Increment:
    register: str

    def execute(self, pointer, registers):
        registers[self.register] += 1
        return pointer + 1, registers


@dataclass
class Jump:
    offset: int

    def execute(self, pointer, registers):
        return pointer + self.offset, registers


@dataclass
class JumpIfEven:
    register: str
    offset: int

    def execute(self, pointer, registers):
        if not registers[self.register] % 2:
            return pointer + self.offset, registers
        return pointer + 1, registers


@dataclass
class JumpIfOne:
    register: str
    offset: int

    def execute(self, pointer, registers):
        if registers[self.register] == 1:
            return pointer + self.offset, registers
        return pointer + 1, registers


def parse_instruction(line):
    match line[:3]:
        case "hlf":
            return Half(line[4:])
        case "tpl":
            return Triple(line[4:])
        case "inc":
            return Increment(line[4:])
        case "jmp":
            return Jump(int(line[4:]))
        case "jie":
            return JumpIfEven(line[4], int(line[6:]))
        case "jio":
            return JumpIfOne(line[4], int(line[6:]))


def init_registers(instructions):
    return instructions.map(lambda instruction: getattr(instruction, "register", None)).filter().set().map_to_values(lambda _: 0)


def solve(input):
    instructions = split(input, "\n").map(parse_instruction)
    registers = init_registers(instructions)
    pointer = 0
    while 0 <= pointer < len(instructions):
        pointer, registers = instructions[pointer].execute(pointer, registers)
    return registers["b"]


with print_duration():
    print("solution:", solve(read("input.txt")))
