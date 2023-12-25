from utils import *


@dataclass
class Location:
    x: int
    y: int
    d: str

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.d


@dataclass
class Beam:
    location: Location

    def split(self, da, db):
        return (
            self.copy(location=self.location.copy(d=da)),
            self.copy(location=self.location.copy(d=db)),
        )

    def step(self, layout, energized, visited):
        x, y, d = self.location
        self.location = Location(*take_step(x, y, d), d)
        if visited.add(tuple(self.location)):
            x, y, d = self.location
            if inbounds(layout)(x, y):
                energized[y][x] = 1
                match (layout[y][x], d):
                    case ("|", "N" | "S"):
                        return [self]
                    case ("|", "E" | "W"):
                        return self.split("N", "S")
                    case ("-", "N" | "S"):
                        return self.split("E", "W")
                    case ("-", "E" | "W"):
                        return [self]
                    case ("\\", "N"):
                        self.location.d = "W"
                        return [self]
                    case ("\\", "S"):
                        self.location.d = "E"
                        return [self]
                    case ("\\", "E"):
                        self.location.d = "S"
                        return [self]
                    case ("\\", "W"):
                        self.location.d = "N"
                        return [self]
                    case ("/", "N"):
                        self.location.d = "E"
                        return [self]
                    case ("/", "S"):
                        self.location.d = "W"
                        return [self]
                    case ("/", "E"):
                        self.location.d = "N"
                        return [self]
                    case ("/", "W"):
                        self.location.d = "S"
                        return [self]
                    case (".", _):
                        return [self]
        return []


def count(energized):
    return sum(sum(line) for line in energized)


def solve(input):
    layout = split(input, "\n")
    h, w = hw(layout)
    energized = [[0 for _ in range(w)] for _ in range(h)]

    visited = Set()
    beams = [Beam([-1, 0, "E"])]
    while beams:
        beam = beams.pop()
        beams.extend(beam.step(layout, energized, visited))
    return count(energized)


with print_duration():
    print("solution:", solve(read("input.txt")))
