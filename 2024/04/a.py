from utils import *


def solve(input):
    m = split(input, "\n", "")
    h = len(m)
    w = len(m[0])

    def right(x, y):
        if w > x + 3:
            return tuple(m[y][x + d] for d in range(4))

    def down(x, y):
        if h > y + 3:
            return tuple(m[y + d][x] for d in range(4))

    def up_right(x, y):
        if w > x + 3 and y >= 3:
            return tuple(m[y - d][x + d] for d in range(4))

    def down_right(x, y):
        if w > x + 3 and h > y + 3:
            return tuple(m[y + d][x + d] for d in range(4))

    return (
        Range(w)
        .product(Range(h))
        .flat_map(t(lambda x, y: (
            right(x, y),
            down(x, y),
            up_right(x, y),
            down_right(x, y),
        )))
        .filter(lambda word: word in (("X", "M", "A", "S"), ("S", "A", "M", "X")))
        .size()
    )


with print_duration():
    print("solution:", solve(read("input.txt")))