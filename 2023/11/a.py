from utils import *


def expand(input):
    return (
        split(input, "\n", "")
        .flat_map(lambda line: ([line] if "#" in line else [line, line]))
        .transpose()
        .flat_map(lambda line: ([line] if "#" in line else [line, line]))
        .transpose()
    )


def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


def solve(input):
    return (
        expand(input)
        .map(lambda row: row.enumerate())
        .enumerate()
        .flat_map(t(lambda y, row: row.map(t(lambda x, s: (x, y, s)))))
        .filter(t(lambda x, y, s: s == "#"))
        .map(itemgetter(0, 1))
        .combinations(2)
        .map(t(manhattan_distance))
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
