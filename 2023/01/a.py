from utils import *


def solve(input):
    return (
        split(input, "\n", "")
        .map(lambda line: line.filter(lambda char: char in "0123456789"))
        .map(lambda digits: int(digits[0] + digits[-1]))
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
