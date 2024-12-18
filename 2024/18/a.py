from heapq import heappop

from utils import *


def solve(input):
    falling = split(input, "\n", ",").map(lambda byte: byte.map(int)).take(1024)
    grid = [["." for _ in range(71)] for _ in range(71)]
    for x, y in falling:
        grid[y][x] = "#"

    _inbounds = t(inbounds(grid))
    # (x, y) -> minimum number of steps to get to that position
    minimums = defaultdict(lambda: inf)
    # (number of steps, (x, y))
    search = [(0, (0, 0))]
    while search:
        steps, (x, y) = heappop(search)
        if (x, y) == (70, 70):
            return steps

        if steps < minimums[(x, y)]:
            minimums[(x, y)] = steps
            search.extend(
                neighbors(x, y)
                .filter(_inbounds)
                .filter(t(lambda x, y: grid[y][x] == "."))
                .map(lambda next: (steps + 1, next))
            )


with print_duration():
    print("solution:", solve(read("input.txt")))
