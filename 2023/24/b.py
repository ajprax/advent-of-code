from z3.z3 import Int, Solver, sat

from utils import *


def parse_line(line):
    p, v = line.split(" @ ")
    x, y, z = p.split(", ")
    dx, dy, dz = v.split(", ")
    return (int(x), int(y), int(z)), (int(dx), int(dy), int(dz))


def solve(input):
    stones = split(input, "\n").map(parse_line)[:3]

    solver = Solver()
    sx, sy, sz = Int("sx"), Int("sy"), Int("sz")
    sdx, sdy, sdz = Int("sdx"), Int("sdy"), Int("sdz")
    for i, ((x, y, z), (dx, dy, dz)) in stones.enumerate():
        dt = Int(f"t{i}")
        solver.add(dt >= 0)
        solver.add((x + dx * dt) == (sx + sdx * dt))
        solver.add((y + dy * dt) == (sy + sdy * dt))
        solver.add((z + dz * dt) == (sz + sdz * dt))
    assert solver.check() == sat
    return solver.model().eval(sx + sy + sz)


with print_duration():
    print("solution:", solve(read("input.txt")))
