from utils import *


def name(i):
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    d, m = divmod(i, 26)
    if d:
        return name(d - 1) + abc[m]
    else:
        return abc[m]


def shift(r, new_start):
    return range(new_start, r.stop - r.start + new_start)


def make_range(l, r):
    l = int(l)
    r = int(r)
    l, r = sorted((l, r))
    return range(l, r + 1)


@dataclass
class Brick:
    name: str
    x: range
    y: range
    z: range

    @classmethod
    def parse(cls, i, s):
        l, r = s.split("~")
        lx, ly, lz = l.split(",")
        rx, ry, rz = r.split(",")

        return cls(name(i), make_range(lx, rx), make_range(ly, ry), make_range(lz, rz))

    def bottom(self):
        return self.z.start

    def top(self):
        return self.z.stop

    def intersects_xy(self, other):
        return ranges_intersect(self.x, other.x) and ranges_intersect(self.y, other.y)

    def fall_onto(self, bricks):
        # find the highest brick that would obstruct this one from falling
        for brick in bricks.sorted(Brick.top, reverse=True):
            if self.intersects_xy(brick):
                self.z = shift(self.z, brick.top())
                break
        else:
            self.z = shift(self.z, 1)
        bricks.append(self)
        return bricks

    def supports(self, other):
        return self.intersects_xy(other) and self.z.stop == other.z.start


def parse(input):
    return fit(input.split("\n")).enumerate().map(t(Brick.parse))


def graph(pile):
    # keys support values
    supports = defaultdict(set)
    for a, b in pile.combinations(2):
        if a.supports(b):
            supports[b.name].add(a.name)
    return supports


def solve(input):
    bricks = parse(input).sorted(Brick.bottom)
    pile = bricks.fold(List(), lambda pile, brick: brick.fall_onto(pile))
    supports = graph(pile)
    sole_supporters = fit(supports).values().filter(lambda supporters: len(supporters) == 1).flatten().set()
    return len(pile) - len(sole_supporters)


with print_duration():
    print("sample:", solve(read("sample.txt")), "expected:", 5)

with print_duration():
    print("input:", solve(read("input.txt")))
