from utils import *


def antinodes(a, b):
    ax, ay = a
    bx, by = b
    dx = bx - ax
    dy = by - ay
    return (ax - dx, ay - dy), (bx + dx, by + dy)


def solve(input):
    map = split(input, "\n", "")
    h, w = hw(map)

    antennae = (
        Range(w)
        .product(Range(h))
        .map(t(lambda x, y: ((x, y), map[y][x])))
        .dict()
        .invert_collect()
    )
    antennae.pop(".")

    return (
        antennae
        .values()
        .flat_map(lambda items: items.combinations(2))
        .flat_map(t(antinodes))
        .set()
        .filter(t(inbounds(map)))
        .size()
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
