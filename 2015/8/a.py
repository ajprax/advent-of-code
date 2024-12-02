from utils import *


def count_line(line):
    return len(line), len(eval(line))


def solve(input):
    return split(input, "\n").map(count_line).map(t(sub)).reduce(add)


with print_duration():
    print("solution:", solve(read("input.txt")))
