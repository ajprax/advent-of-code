from utils import *


def step(x, y, d):
    return take_step(x, y, d, "^<v>")


def find_robot(map):
    h, w = hw(map)
    for y in range(h):
        try:
            x = map[y].index("@")
            return x, y
        except ValueError:
            pass


def solve(input):
    map, instructions = split(input, "\n\n")
    map = split(map, "\n", "")
    instructions = split(instructions, "\n", "").flatten()
    rx, ry = find_robot(map)

    for d in instructions:
        push = False
        nx, ny = rx, ry
        while True:
            nx, ny = step(nx, ny, d)
            if map[ny][nx] == ".":
                move = True
                break
            elif map[ny][nx] == "#":
                move = False
                break
            elif map[ny][nx] == "O":
                push = True

        if move:
            if push:
                map[ny][nx] = "O"
            map[ry][rx] = "."
            rx, ry = step(rx, ry, d)
            map[ry][rx] = "@"

    return (
        indices(map)
        .filter(t(lambda x, y: map[y][x] == "O"))
        .map(t(lambda x, y: x + 100 * y))
        .apply(sum)
    )



with print_duration():
    print("solution:", solve(read("input.txt")))
