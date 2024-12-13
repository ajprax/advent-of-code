from math import isfinite

from utils import *


machine_re = re.compile("Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")


@dataclass
class Machine:
    a: np.ndarray
    b: np.ndarray
    prize: np.ndarray


def parse(machine):
    m = machine_re.match(machine)
    a = np.array([int(m.group(1)), int(m.group(2))])
    b = np.array([int(m.group(3)), int(m.group(4))])
    p = np.array([int(m.group(5)), int(m.group(6))])
    return Machine(a, b, p)


def minimize(machine):
    best = inf

    As = max(round((machine.prize[0] / machine.a[0]) + 0.5), round((machine.prize[1] / machine.a[1]) + 0.5))
    Bs = 0
    while As >= 0:
        target = As * machine.a + Bs * machine.b
        cost = As * 3 + Bs
        if np.all(target == machine.prize) and cost < best:
            best = cost
            As -= 1
        elif np.all(target > machine.prize):
            As -= 1
        else:
            Bs += 1
    if isfinite(best):
        return best


def solve(input):
    machines = split(input, "\n\n").map(parse)
    return machines.map(minimize).filter().apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))
