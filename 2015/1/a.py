from utils import *


def solve(input):
    return input.count("(") - input.count(")")


with print_duration():
    print("solution:", solve(read("input.txt")))
