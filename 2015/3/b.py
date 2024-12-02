from utils import *


def solve(input):
    sx = sy = rx = ry = 0
    visited = {(sx, sy)}
    for sd, rd in split(input, "").batch(2):
        sx, sy = take_step(sx, sy, sd, "^<v>")
        visited.add((sx, sy))
        rx, ry = take_step(rx, ry, rd, "^<v>")
        visited.add((rx, ry))
    return len(visited)


with print_duration():
    print("solution:", solve(read("input.txt")))
