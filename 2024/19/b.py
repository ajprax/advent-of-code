from utils import *



def solve(input):
    towels, designs = split(input, "\n\n")
    towels = split(towels, ", ")
    designs = split(designs, "\n")

    # design -> int
    _ways = {"": 1}

    def ways(design):
        if design not in _ways:
            _ways[design] = (
                towels
                .filter(design.startswith)
                .map(lambda towel: design[len(towel):])
                .map(ways)
                .apply(sum)
            )
        return _ways[design]

    return designs.map(ways).apply(sum)

with print_duration():
    print("solution:", solve(read("input.txt")))
