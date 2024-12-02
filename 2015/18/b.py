from utils import *


def step(m):
    n = m.copy()
    h, w = m.shape
    for y in range(h):
        for x in range(w):
            sx = max(x - 1, 0)
            ex = min(x + 2, w)
            sy = max(y - 1, 0)
            ey = min(y + 2, h)
            live_neighbors = np.count_nonzero(m[sy:ey, sx:ex]) - m[y, x]
            if m[y, x]:
                n[y, x] = int(2 <= live_neighbors <= 3)
            else:
                n[y, x] = int(live_neighbors == 3)
    for y in (0, h-1):
        for x in (0, w-1):
            n[y, x] = 1
    return n


def solve(input):
    m = np.array(split(input, "\n", "").map(lambda line: line.map(lambda c: c == "#")), np.uint8)
    for _ in range(100):
        m = step(m)
    return np.count_nonzero(m)


with print_duration():
    print("solution:", solve(read("input.txt")))
