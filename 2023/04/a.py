from utils import *


def count_matches(winning, playing):
    return len(set(winning) & set(playing))


def calculate_score(winning, playing):
    matches = count_matches(winning, playing)
    return 2**(matches - 1) if matches else 0


def solve(input):
    return (
        split(input, "\n")
        .map(lambda line: line[10:])
        .map(lambda line: split(line, " | ", None))
        .map(t(calculate_score))
        .reduce(add, 0)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))


