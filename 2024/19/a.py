from utils import *


def solve(input):
    towels, designs = split(input, "\n\n")
    towels = split(towels, ", ")
    designs = split(designs, "\n")

    _possible = {"": True}

    def possible(design):
        if design not in _possible:
            _possible[design] = (
                towels
                .filter(design.startswith)
                .map(lambda towel: design[len(towel):])
                .any(possible)
            )
        return _possible[design]

    return designs.map(possible).apply(sum)

with print_duration():
    print("solution:", solve(read("input.txt")))
