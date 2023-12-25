from utils import *


@dataclass
class Map:
    map: List[str]

    @property
    def height(self):
        return self.map.size()

    @property
    def width(self):
        return len(self.map[0])

    def tiles(self):
        return fit(range(self.width)).product(range(self.height)).map(t(lambda x, y: Tile(self, x, y)))

    def get(self, x, y):
        return self.map[y][x]

    @property
    def s(self):
        y, row = self.map.enumerate().only(t(lambda i, row: "S" in row))
        x = row.index("S")
        return Tile(self, x, y)


@dataclass
class Tile:
    map: Map
    x: int
    y: int

    def __repr__(self):
        return f"Tile({self.contents}, {self.x}, {self.y})"

    @property
    def inbounds(self):
        return 0 <= self.x < self.map.width and 0 <= self.y < self.map.height

    @property
    def contents(self):
        return self.map.get(self.x, self.y)

    @property
    def connections(self):
        match self.contents:
            case "|":
                return fit([Tile(self.map, self.x, self.y - 1), Tile(self.map, self.x, self.y + 1)]).filter(lambda tile: tile.inbounds)
            case "-":
                return fit([Tile(self.map, self.x - 1, self.y), Tile(self.map, self.x + 1, self.y)]).filter(lambda tile: tile.inbounds)
            case "L":
                return fit([Tile(self.map, self.x, self.y - 1), Tile(self.map, self.x + 1, self.y)]).filter(lambda tile: tile.inbounds)
            case "J":
                return fit([Tile(self.map, self.x, self.y - 1), Tile(self.map, self.x - 1, self.y)]).filter(lambda tile: tile.inbounds)
            # TODO: don't hardcode S
            case "7" | "S":
                return fit([Tile(self.map, self.x, self.y + 1), Tile(self.map, self.x - 1, self.y)]).filter(lambda tile: tile.inbounds)
            case "F":
                return fit([Tile(self.map, self.x, self.y + 1), Tile(self.map, self.x + 1, self.y)]).filter(lambda tile: tile.inbounds)
            case ".":
                return fit([])


def expand(c):
    match c:
        case "|":
            return ".|.\n.|.\n.|."
        case "-":
            return "...\n---\n..."
        case "L":
            return ".|.\n.L-\n..."
        case "J":
            return ".|.\n-J.\n..."
        case "7":
            return "...\n-7.\n.|."
        # TODO: don't hardcode S
        case "S":
            return "...\n-S.\n.|."
        case "F":
            return "...\n.F-\n.|."
        case ".":
            return "...\n...\n..."


def hstack(blocks):
    return fit(blocks).map(lambda block: block.split("\n")).unzip().map("".join).apply("\n".join)


def expand_raw(raw):
    in_lines = raw.split("\n")
    out_lines = []
    for line in in_lines:
        out_lines.append(fit(line).map(expand).apply(hstack))
    return "\n".join(out_lines)


def is_locus(tile):
    return tile.x % 3 == 1 and tile.y % 3 == 1


def inside(border):
    def test(tile):
        # tile is guaranteed to be a locus. go up by one and then count intersections going left
        if (tile.x, tile.y) in border:
            return False
        tile2 = Tile(tile.map, tile.x, tile.y - 1)
        intersections = 0
        for i in range(tile2.x):
            if (i, tile2.y) in border:
                intersections += 1
        return intersections % 2
    return test


def find_border(map):
    s = map.s
    prev_l = s
    l, _ = map.s.connections
    border = fit([l])
    while True:
        l, prev_l = l.connections.only(lambda tile: tile != prev_l), l
        border.append(l)
        if l == s:
            break
    return border


def solve(input):
    map = Map(split(expand_raw(input), "\n"))
    border = find_border(map).map(lambda tile: (tile.x, tile.y)).set()
    inside_tiles = map.tiles().filter(is_locus).filter(inside(border)).list()
    return inside_tiles.size()


with print_duration():
    print("solution:", solve(read("input.txt")))
