from utils import *


def solve(input):
    m = split(input, "\n", "")
    h = len(m)
    w = len(m[0])

    def xmas(x, y):
        slash = "".join((m[y + 1][x - 1], m[y][x], m[y - 1][x + 1]))
        backslash = "".join((m[y - 1][x - 1], m[y][x], m[y + 1][x + 1]))
        return {slash, backslash} <= {"MAS", "SAM"}

    return (
        Range(1, w - 1)
        .product(Range(1, h - 1))
        .map(t(xmas))
        .apply(sum)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
