from utils import *


def solve(input):
    x = y = 0
    visited = {(x, y)}
    for d in split(input, ""):
        x, y = take_step(x, y, d, "^<v>")
        visited.add((x, y))
    return len(visited)


with print_duration():
    print("solution:", solve(read("input.txt")))
