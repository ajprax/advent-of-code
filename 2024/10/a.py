from utils import *


def count_trails(map):
    def _count_trails(x, y):
        locations = Set([(x, y)])
        for h in range(1, 10):
            locations = (
                locations
                .flat_map(t(neighbors))
                .filter(t(inbounds(map)))
                .filter(t(lambda x, y: map[y][x] == h))
            )
        return locations.size()
    return _count_trails


def solve(input):
    map = split(input, "\n", "").map(lambda row: row.map(int))
    return indices(map).filter(t(lambda x, y: map[y][x] == 0)).map(t(count_trails(map))).apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))
