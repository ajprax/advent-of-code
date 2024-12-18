from heapq import heappop

from utils import *


def blocked(grid):
    _inbounds = t(inbounds(grid))
    # (x, y) -> minimum number of steps to get to that position
    minimums = defaultdict(lambda: inf)
    # (number of steps, (x, y))
    search = [(0, (0, 0))]
    while search:
        steps, (x, y) = heappop(search)
        if (x, y) == (70, 70):
            return False

        if steps < minimums[(x, y)]:
            minimums[(x, y)] = steps
            search.extend(
                neighbors(x, y)
                .filter(_inbounds)
                .filter(t(lambda x, y: grid[y][x] == "."))
                .map(lambda next: (steps + 1, next))
            )
    return True


def mid(a, b):
    return (a + b) // 2


def simulate(falling, n):
    grid = [["." for _ in range(71)] for _ in range(71)]
    for x, y in falling.take(n):
        grid[y][x] = "#"
    return grid


def solve(input):
    falling = split(input, "\n", ",").map(lambda byte: byte.map(int))

    minimum = 1024 # part A wasn't blocked
    maximum = len(falling) - 1
    while True:
        middle = mid(minimum, maximum)
        if middle == minimum: # mid() rounds down, so this indicates minimum + 1 == maximum
            return falling[middle]
        grid = simulate(falling, middle)
        if blocked(grid):
            maximum = middle
        else:
            minimum = middle


with print_duration():
    print("solution:", solve(read("input.txt")))
