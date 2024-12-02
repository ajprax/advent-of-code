from utils import *


def solve_line(dimensions):
    a, b, c = sorted(dimensions)

    return 2*a + 2*b + a*b*c


def solve(input):
    return (
        split(input, "\n", "x")
        .map(lambda line: line.map(int))
        .map(solve_line)
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
