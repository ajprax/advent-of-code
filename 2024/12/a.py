from utils import *


def find_plots(map):
    h, w = hw(map)
    inbounds_ = inbounds(map)

    plots = List()
    assigned = Set()
    for x in range(w):
        for y in range(h):
            if (x, y) in assigned:
                continue
            plot = Set()
            plant = map[y][x]
            search = [(x, y)]
            while search:
                x, y = search.pop()
                if (x, y) in assigned:
                    continue
                nplant = map[y][x]
                if plant == nplant and (x, y):
                    plot.add((x, y))
                    assigned.add((x, y))
                    search.extend(
                        neighbors(x, y)
                        .filter(t(inbounds_))
                    )
            plots.append(plot)
    return plots


def price(plot):
    area = len(plot)
    perimeter = 0
    for x, y in plot:
        for neighbor in neighbors(x, y):
            if neighbor not in plot:
                perimeter += 1
    return area * perimeter


def solve(input):
    map = split(input, "\n", "")
    plots = find_plots(map)
    return plots.map(price).apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))
