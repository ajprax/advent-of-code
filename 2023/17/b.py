from utils import *


def next_directions(ds):
    if not ds:
        return "S", "E"
    d = ds[-1]

    if len(ds) < 10:
        return turn_left(d), turn_right(d), d
    if len(set(ds)) == 1:
        return turn_left(d), turn_right(d)
    return turn_left(d), turn_right(d), d


def solve(input):
    city = split(input, "\n", "").map(lambda line: line.map(int))
    inbounds_ = inbounds(city)
    h, w = hw(city)
    paths = PriorityQueue()
    paths.put((0, 0, 0, []))
    # keys are (x, y, ds[-10:]), values are loss
    best = {}
    while True:
        loss, x, y, ds = paths.get()
        if x + 1 == w and y + 1 == h and len(set(ds[-4:])) == 1:
            return loss
        k = (x, y, tuple(ds[-10:]))
        if k in best:
            if loss < best[k]:
                best[k] = loss
            else:
                continue
        else:
            best[k] = loss
        for d in next_directions(ds[-10:]):
            if not ds or d != ds[-1]:
                nx, ny = x, y
                loss_ = loss
                for _ in range(4):
                    nx, ny = take_step(nx, ny, d)
                    if inbounds_(nx, ny):
                        loss_ += city[ny][nx]
                if inbounds_(nx, ny):
                    paths.put((loss_, nx, ny, ds + [d] * 4))
            else:
                nx, ny = take_step(x, y, d)

                if inbounds_(nx, ny):
                    paths.put((loss + city[ny][nx], nx, ny, ds + [d]))


with print_duration():
    print("solution:", solve(read("input.txt")))
