import math

from utils import *


@dataclass
class Range:
    dst: int
    src: int
    length: int

    @classmethod
    def parse(cls, line):
        return cls(*split(line, None).map(int))

    def __contains__(self, index):
        return self.src <= index < (self.src + self.length)

    def map(self, index):
        return self.dst + index - self.src


@dataclass
class Map:
    ranges: List[Range]

    def map(self, index):
        for range in self.ranges:
            if index in range:
                return range.map(index)
        return index


def solve(input):
    seeds, *maps = split(input, "\n\n")
    seeds = split(seeds[7:], None).map(int)
    maps = (
        List(maps)
        .map(lambda map: List(split(map, "\n")[1:]).map(Range.parse))
        .map(Map)
    )

    best = math.inf
    for seed in seeds:
        value = seed
        for map in maps:
            value = map.map(value)
        best = min(best, value)

    return best


with print_duration():
    print("solution:", solve(read("input.txt")))
