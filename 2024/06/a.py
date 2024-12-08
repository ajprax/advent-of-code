from utils import *


def find_start(map):
    for y, row in map.enumerate():
        for x, c in row.enumerate():
            if c in "<^>v":
                return x, y, c


def solve(input):
    map = split(input, "\n", "")
    h = len(map)
    w = len(map[0])
    x, y, direction = find_start(map)

    visited = {(x, y)}
    while True:
        nx, ny = take_step(x, y, direction, "^<v>")
        if nx < 0 or nx >= w or ny < 0 or ny >= h:
            return len(visited)
        if map[ny][nx] == "#":
            direction = turn_right(direction, "^<v>")
        else:
            x, y = nx, ny
            visited.add((x, y))



with print_duration():
    print("solution:", solve(read("input.txt")))
