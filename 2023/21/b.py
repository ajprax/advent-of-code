import matplotlib.pyplot as plt

from utils import *


def duplicate(map, n):
    h, w = len(map), len(map[0])
    out = List()
    for y in range(h):
        row = map[y]
        out.append(deepcopy(row))
        for _ in range(n-1):
            out[-1].extend(deepcopy(row))
    rows = deepcopy(out)
    for _ in range(n-1):
        out.extend(deepcopy(rows))
    return out


def solve(input):
    nsteps = 26501365
    map = List(input.split("\n")).map(List)
    h, w = len(map), len(map[0])
    map = duplicate(map, 7)

    def passable(x, y):
        return map[y % h][x % w] != "#"

    def next_steps(x, y):
        return neighbors(x, y).filter(t(passable))

    positions = Set([(h//2, w//2)])
    counts = List([0])
    for _ in Range(h+h+h//2):
        positions = positions.flat_map(t(next_steps))
        counts.append(positions.size())

    a, b, c = np.polyfit([0, 1, 2], [counts[h//2], counts[h+h//2], counts[h+h+h//2]], 2)
    x = (nsteps - h//2) / h
    return round(round(a) * x ** 2 + round(b) * x + round(c))


with print_duration():
    print("solution:", solve(read("input.txt")))
