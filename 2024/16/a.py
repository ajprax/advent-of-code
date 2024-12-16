from utils import *

from heapq import heappush, heappop


def find_start_end(map):
    h, w = hw(map)
    for x in range(w):
        for y in range(h):
            if map[y][x] == "S":
                start = x, y
            elif map[y][x] == "E":
                end = x, y
    return start, end


def solve(input):
    map = split(input, "\n")
    start, end = find_start_end(map)

    # (x, y, direction) -> minimum score to get to that position
    minimums = defaultdict(lambda: inf)
    # (score, position, direction in "NWSE")
    search = [(0, start, "E")]
    while search:
        score, (x, y), d = heappop(search)
        if (x, y) == end:
            return score

        if score < minimums[(x, y, d)]:
            minimums[(x, y, d)] = score

            nx, ny = take_step(x, y, d)
            if map[ny][nx] != "#":
                heappush(search, (score + 1, (nx, ny), d))
            heappush(search, (score + 1000, (x, y), turn_left(d)))
            heappush(search, (score + 1000, (x, y), turn_right(d)))
    assert False, "No path found"


with print_duration():
    print("solution:", solve(read("input.txt")))
