from utils import *


def solve(input):
    m = np.zeros((1000, 1000))
    for line in split(input, "\n", " "):
        match line:
            case ["turn", "on", mins, "through", maxes]:
                minx, miny = split(mins, ",").map(int)
                maxx, maxy = split(maxes, ",").map(int).map(lambda i: i + 1)
                m[miny:maxy, minx:maxx] += 1
            case ["turn", "off", mins, "through", maxes]:
                minx, miny = split(mins, ",").map(int)
                maxx, maxy = split(maxes, ",").map(int).map(lambda i: i + 1)
                m[miny:maxy, minx:maxx] -= 1
                m = np.clip(m, 0, inf)
            case ["toggle", mins, "through", maxes]:
                minx, miny = split(mins, ",").map(int)
                maxx, maxy = split(maxes, ",").map(int).map(lambda i: i + 1)
                m[miny:maxy, minx:maxx] += 2
    return np.sum(m)


with print_duration():
    print("solution:", solve(read("input.txt")))
