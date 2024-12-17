from utils import *


@dataclass
class Computer:
    registers: List[int]
    program: List[int]
    output: List[int] = None
    pointer: int = 0

    def __post_init__(self):
        self.output = List()

    def run(self):
        table = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        while self.pointer <= len(self.program) - 1:
            operator, operand = self.program[self.pointer:self.pointer + 2]
            table[operator](operand)

    def combo(self, operand):
        assert operand != 7
        if operand <= 3:
            return operand
        return self.registers[operand - 4]

    def adv(self, operand):
        num = self.registers[0]
        den = 2 ** self.combo(operand)
        self.registers[0] = num // den
        self.pointer += 2

    def bxl(self, operand):
        self.registers[1] = self.registers[1] ^ operand
        self.pointer += 2

    def bst(self, operand):
        self.registers[1] = self.combo(operand) % 8
        self.pointer += 2

    def jnz(self, operand):
        if self.registers[0] == 0:
            self.pointer += 2
        else:
            self.pointer = operand

    def bxc(self, operand):
        self.registers[1] = self.registers[1] ^ self.registers[2]
        self.pointer += 2

    def out(self, operand):
        self.output.append(self.combo(operand) % 8)
        self.pointer += 2

    def bdv(self, operand):
        num = self.registers[0]
        den = 2 ** self.combo(operand)
        self.registers[1] = num // den
        self.pointer += 2

    def cdv(self, operand):
        num = self.registers[0]
        den = 2 ** self.combo(operand)
        self.registers[2] = num // den
        self.pointer += 2


def solve(input):
    registers, program = split(input, "\n\n")
    registers = split(registers, "\n", ": ").map(itemgetter(1)).map(int)
    program = split(program, ": ")[1]
    program = split(program, ",").map(int)

    computer = Computer(registers, program)
    computer.run()
    return ",".join(computer.output.map(str))


with print_duration():
    print("solution:", solve(read("input.txt")))
