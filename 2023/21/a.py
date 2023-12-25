from utils import *


def find_s(map):
    for y, line in map.enumerate():
        for x, s in line.enumerate():
            if s == "S":
                return x, y


def solve(input, nsteps):
    map = List(input.split("\n")).map(List)

    def passable(x, y):
        return map[y][x] != "#"

    def next_steps(x, y):
        return (
            neighbors(x, y)
            .filter(t(inbounds(map)))
            .filter(t(passable))
        )

    positions = Set([find_s(map)])
    for _ in range(nsteps):
        positions = positions.flat_map(t(next_steps))
    return positions.size()


with print_duration():
    print("sample:", solve(read("sample.txt"), 6), "expected:", 16)

with print_duration():
    print("input:", solve(read("input.txt"), 64))
