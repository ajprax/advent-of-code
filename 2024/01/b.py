from utils import *


def solve(input):
    left, right = (
        split(input, "\n", "   ")
        .unzip()
        .map(lambda a: a.map(int))
    )
    counts = right.count()
    return left.map(lambda l: l * counts.get(l, 0)).apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))
