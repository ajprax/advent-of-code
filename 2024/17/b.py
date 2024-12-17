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
        return self.output

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


# Manually disassembling the program reveals some facts that allow us to efficiently search for a solution
# 1. the program is a loop that runs until A == 0
# 2. on each loop, we drop the 3 rightmost bits of A
# 3. B and C are not carried between loops
# This means that digits in the program from right to left depend only on the same number of 3-bit subsections of the
# starting A value (padded until len(bin(A)[2:]) == 3), so we can find all possible 3-bit sequences that generate the
# desired rightmost digit, then starting from each of those, test all possible 6 bit sequences to find those that
# produce the rightmost 2 digits of the program, and so on until the full program is generated. Then accept the minimum
# solution
def find(program):
    solutions = []
    search = list(range(8))
    while search:
        a = search.pop()
        output = Computer([a, 0, 0], program).run()
        if output == program:
            solutions.append(a)
        elif output == program[-len(output):]:
            for i in range(8):
                search.append((a << 3) + i)
    return min(solutions)


def solve(input):
    registers, program = split(input, "\n\n")
    program = split(program, ": ")[1]
    program = split(program, ",").map(int)

    return find(program)


with print_duration():
    print("solution:", solve(read("input.txt")))
