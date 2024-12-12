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


def count_sides(direction):
    def _count_sides(coordinates):
        if direction == "horizontal":
            return (
                coordinates
                .sorted(itemgetter(0))
                .map(t(lambda x, y: (x - 1, y) not in coordinates))
                .apply(sum)
            )
        elif direction == "vertical":
            return (
                coordinates
                .sorted(itemgetter(1))
                .map(t(lambda x, y: (x, y - 1) not in coordinates))
                .apply(sum)
            )
    return _count_sides


def price(plot):
    area = len(plot)

    sides = Iterator().chain(
        (
            plot
            .filter(t(lambda x, y: (x, y - 1) not in plot))
            .group_by(itemgetter(1))
            .values()
            .map(count_sides("horizontal"))
        ),
        (
            plot
            .filter(t(lambda x, y: (x - 1, y) not in plot))
            .group_by(itemgetter(0))
            .values()
            .map(count_sides("vertical"))
        ),
        (
            plot
            .filter(t(lambda x, y: (x, y + 1) not in plot))
            .group_by(itemgetter(1))
            .values()
            .map(count_sides("horizontal"))
        ),
        (
            plot
            .filter(t(lambda x, y: (x + 1, y) not in plot))
            .group_by(itemgetter(0))
            .values()
            .map(count_sides("vertical"))
        ),
    ).apply(sum)

    return area * sides


def solve(input):
    map = split(input, "\n", "")
    plots = find_plots(map)
    return plots.map(price).apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))
