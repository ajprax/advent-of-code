from utils import *


def find_start(map):
    for y, row in map.enumerate():
        for x, c in row.enumerate():
            if c in "<^>v":
                return x, y, c


def turn(direction):
    match direction:
        case "^":
            return ">"
        case ">":
            return "v"
        case "v":
            return "<"
        case "<":
            return "^"


def step(x, y, direction):
    match direction:
        case "^":
            return x, y - 1
        case ">":
            return x + 1, y
        case "v":
            return x, y + 1
        case "<":
            return x - 1, y


def solve(input):
    map = split(input, "\n", "")
    h = len(map)
    w = len(map[0])
    x, y, direction = find_start(map)

    visited = {(x, y)}
    while True:
        nx, ny = step(x, y, direction)
        if nx < 0 or nx >= w or ny < 0 or ny >= h:
            return len(visited)
        if map[ny][nx] == "#":
            direction = turn(direction)
        else:
            x, y = nx, ny
            visited.add((x, y))



with print_duration():
    print("solution:", solve(read("input.txt")))
