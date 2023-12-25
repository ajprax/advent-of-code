from utils import *


def name(i):
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    d, m = divmod(i, 26)
    if d:
        return name(d - 1) + abc[m]
    else:
        return abc[m]


@dataclass
class Brick:
    name: str
    x: range
    y: range
    z: range

    @classmethod
    def parse(cls, i, s):
        def make_range(l, r):
            l, r = sorted((int(l), int(r)))
            return range(l, r + 1)

        l, r = s.split("~")
        return cls(name(i), *List(l.split(",")).zip(r.split(",")).map(t(make_range)))

    def bottom(self):
        return self.z.start

    def top(self):
        return self.z.stop

    def intersects_xy(self, other):
        return ranges_intersect(self.x, other.x) and ranges_intersect(self.y, other.y)

    def fall_onto(self, pile):
        def shift(r, new_start):
            return range(new_start, r.stop - r.start + new_start)

        # find the highest brick that would obstruct this one from falling
        for brick in pile.sorted(Brick.top, reverse=True):
            if self.intersects_xy(brick):
                self.z = shift(self.z, brick.top())
                break
        else:
            self.z = shift(self.z, 1)
        pile.append(self)
        return pile

    def supports(self, other):
        return self.intersects_xy(other) and self.z.stop == other.z.start


def graph(pile):
    # values support keys
    supports = defaultdict(set)
    # keys support values
    supported_by = defaultdict(set)
    for a, b in pile.combinations(2):
        if a.supports(b):
            supports[b.name].add(a.name)
            supported_by[a.name].add(b.name)
    return supports, supported_by


def count_chain_reaction(supports, supported_by, brick):
    chain = {brick}
    search = [*supported_by[brick]]
    while search:
        other = search.pop()
        if other not in chain:
            if supports[other] <= chain:
                chain.add(other)
                search.extend(supported_by[other])
    # the brick itself is included in the chain to make comparisons easier, but should not be included in the output
    return len(chain) - 1


def parse(input):
    return fit(input.split("\n")).enumerate().map(t(Brick.parse))


def solve(input):
    pile = parse(input).sorted(Brick.bottom).fold(List(), lambda pile, brick: brick.fall_onto(pile))
    supports, supported_by = graph(pile)
    return pile.map(lambda brick: count_chain_reaction(supports, supported_by, brick.name)).reduce(add)


sample_solution = solve(read("sample.txt"))
assert sample_solution == 7, sample_solution

with print_duration():
    print("solution:", solve(read("input.txt")))
