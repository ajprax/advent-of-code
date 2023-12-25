from utils import *


def next_directions(ds):
    if not ds:
        return "S", "E"
    d = ds[-1]

    if len(ds) < 3:
        return turn_left(d), turn_right(d), d
    elif len(set(ds)) == 1:
        return turn_left(d), turn_right(d)
    return turn_left(d), turn_right(d), d


def solve(input):
    city = split(input, "\n", "").map(lambda line: line.map(int))
    h, w = hw(city)
    paths = PriorityQueue()
    paths.put((0, 0, 0, []))
    # keys are (x, y, ds[-3:]), values are loss
    best = {}
    while True:
        loss, x, y, ds = paths.get()
        if x + 1 == w and y + 1 == h:
            return loss
        k = (x, y, tuple(ds[-3:]))
        if k in best:
            if loss < best[k]:
                best[k] = loss
            else:
                continue
        else:
            best[k] = loss
        for d in next_directions(ds[-3:]):
            nx, ny = take_step(x, y, d)
            if inbounds(city)(nx, ny):
                paths.put((loss + city[ny][nx], nx, ny, ds + [d]))


with print_duration():
    print("solution:", solve(read("input.txt")))
