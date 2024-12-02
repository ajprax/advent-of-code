from utils import *


def solve(input):
    count = 0
    for i, c in enumerate(input, 1):
        match c:
            case "(":
                count += 1
            case ")":
                count -= 1
        if count < 0:
            return i


with print_duration():
    print("solution:", solve(read("input.txt")))
