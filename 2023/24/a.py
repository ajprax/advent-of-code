from utils import *


minx = miny = 200000000000000
maxx = maxy = 400000000000000


def parse_line(line):
    p, v = line.split(" @ ")
    x, y, z = p.split(", ")
    dx, dy, dz = v.split(", ")
    return np.array((int(x), int(y), int(z))), np.array((int(dx), int(dy), int(dz)))


def derive_line(x, y, dx, dy):
    # y = ax + b
    a = dy / dx
    b = y - a * x
    return a, b


def intersection(l1, l2):
    a1, b1 = l1
    a2, b2 = l2

    # parallel lines
    if a1 == a2:
        return None

    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1
    return x, y


def collides_within(h1, h2):
    p1, v1 = h1
    p2, v2 = h2

    x1, y1, _ = p1
    x2, y2, _ = p2
    dx1, dy1, _ = v1
    dx2, dy2, _ = v2

    l1 = derive_line(x1, y1, dx1, dy1)
    l2 = derive_line(x2, y2, dx2, dy2)

    i = intersection(l1, l2)
    if i is None:
        return False
    ix, iy = i
    # in the region of interest
    if not (minx <= ix <= maxx) or not (miny <= iy <= maxy):
        return False
    # check if ix, iy is in the correct direction for both lines
    if (
        (dx1 >= 0 and ix < x1)
        or (dx1 < 0 and ix > x1)
        or (dy1 >= 0 and iy < y1)
        or (dy1 < 0 and iy > y1)
        or (dx2 >= 0 and ix < x2)
        or (dx2 < 0 and ix > x2)
        or (dy2 >= 0 and iy < y2)
        or (dy2 < 0 and iy > y2)
    ):
        return False
    return True


def solve(input):
    return (
        split(input, "\n")
        .map(parse_line)
        .combinations(2)
        .filter(t(collides_within))
        .size()
    )


def z3collides_within(a, b):
    from z3.z3 import Real, Solver, sat
    (ax, ay, _), (adx, ady, _) = a
    (bx, by, _), (bdx, bdy, _) = b
    solver = Solver()
    x, y = Real("x"), Real("y")
    at, bt = Real("at"), Real("bt")
    solver.add(at >= 0)
    solver.add(bt >= 0)
    solver.add(minx <= x)
    solver.add(x <= maxx)
    solver.add(miny <= y)
    solver.add(y <= maxy)
    solver.add(ax + adx * at == x)
    solver.add(ay + ady * at == y)
    solver.add(bx + bdx * bt == x)
    solver.add(by + bdy * bt == y)
    return solver.check() == sat


def z3solve(input):
    return (
        split(input, "\n")
        .map(parse_line)
        .combinations(2)
        .filter(t(z3collides_within))
        .size()
    )


with print_duration():
    print("solution:", solve(read("input.txt")))


with print_duration():
    print("z3 solution:", z3solve(read("input.txt")))