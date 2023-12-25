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


def solve(input):
    map = Map(split(input, "\n"))
    prev_l = prev_r = map.s
    l, r = map.s.connections
    steps = 0
    while l != r:
        steps += 1
        l, prev_l = l.connections.only(lambda tile: tile != prev_l), l
        r, prev_r = r.connections.only(lambda tile: tile != prev_r), r
    return steps + 1


with print_duration():
    print("solution:", solve(read("input.txt")))
