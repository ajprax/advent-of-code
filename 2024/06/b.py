from utils import *


def find_start(map):
    for y, row in map.enumerate():
        for x, c in row.enumerate():
            if c in "<^>v":
                return x, y, c


def add_obstruction(map, x, y):
    map = deepcopy(map)
    map[y][x] = "#"
    return map


def loops(map, start):
    h = len(map)
    w = len(map[0])
    x, y, direction = start
    visited = {(x, y, direction)}
    while True:
        nx, ny = take_step(x, y, direction, "^<v>")
        if nx < 0 or nx >= w or ny < 0 or ny >= h:
            return False
        if map[ny][nx] == "#":
            direction = turn_right(direction, "^<v>")
        else:
            x, y  = nx, ny
            if (x, y, direction) in visited:
                return True
            visited.add((x, y, direction))


def solve(input):
    map = split(input, "\n", "")
    h = len(map)
    w = len(map[0])
    start = find_start(map)

    return (
        Range(w)
        .product(Range(h))
        .filter(t(lambda x, y: map[y][x] == "."))
        .filter(t(lambda x, y: loops(add_obstruction(map, x, y), start)))
        .size()
    )



with print_duration():
    print("solution:", solve(read("input.txt")))
