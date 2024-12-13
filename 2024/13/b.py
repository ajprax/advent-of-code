from utils import *


machine_re = re.compile("Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")


@dataclass
class Machine:
    a: np.ndarray
    b: np.ndarray
    p: np.ndarray


def parse(machine):
    m = machine_re.match(machine)
    a = np.array([int(m.group(1)), int(m.group(2))])
    b = np.array([int(m.group(3)), int(m.group(4))])
    p = np.array([int(m.group(5)) + 10000000000000, int(m.group(6)) + 10000000000000])
    return Machine(a, b, p)


def minimize(machine):
    m1 = machine.a[1] / machine.a[0]
    b1 = 0

    m2 = machine.b[1] / machine.b[0]
    b2 = machine.p[1] - m2 * machine.p[0]

    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    As = x / machine.a[0]
    Bs = (machine.p[0] - x) / machine.b[0]

    # round and verify
    # rounding is necessary because of floating point imprecision
    # verifying is necessary because rounding may lose real decimals
    if np.all([machine.a * round(As) + machine.b * round(Bs)] == machine.p):
        return round(As * 3 + Bs)


def solve(input):
    machines = split(input, "\n\n").map(parse)
    return machines.map(minimize).filter().apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))


10000000000000