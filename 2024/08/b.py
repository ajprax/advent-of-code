from utils import *


def antinodes(map):
    def _antinodes(a, b):
        ax, ay = a
        bx, by = b
        dx = bx - ax
        dy = by - ay
        nx, ny = ax, ay
        while True:
            yield nx, ny
            nx -= dx
            ny -= dy
            if not inbounds(map)(nx, ny):
                break
        nx, ny = bx, by
        while True:
            yield nx, ny
            nx += dx
            ny += dy
            if not inbounds(map)(nx, ny):
                break
    return _antinodes


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
        .flat_map(t(antinodes(map)))
        .set()
        .size()
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
