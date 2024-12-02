from utils import *


def solve(input):
    m = np.zeros((1000, 1000), bool)
    for line in split(input, "\n", " "):
        match line:
            case ["turn", "on", mins, "through", maxes]:
                minx, miny = split(mins, ",").map(int)
                maxx, maxy = split(maxes, ",").map(int).map(lambda i: i + 1)
                m[miny:maxy, minx:maxx] = 1
            case ["turn", "off", mins, "through", maxes]:
                minx, miny = split(mins, ",").map(int)
                maxx, maxy = split(maxes, ",").map(int).map(lambda i: i + 1)
                m[miny:maxy, minx:maxx] = 0
            case ["toggle", mins, "through", maxes]:
                minx, miny = split(mins, ",").map(int)
                maxx, maxy = split(maxes, ",").map(int).map(lambda i: i + 1)
                m[miny:maxy, minx:maxx] = ~m[miny:maxy, minx:maxx]
    return np.count_nonzero(m)


with print_duration():
    print("solution:", solve(read("input.txt")))
