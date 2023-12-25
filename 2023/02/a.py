from utils import *


@dataclass
class Pull:
    red: int = 0
    blue: int = 0
    green: int = 0

    @classmethod
    def parse(cls, s):
        return cls(**(split(s, ", ", " ").map(t(lambda n, c: (c, int(n)))).dict()))


@dataclass
class Game:
    id: int
    pulls: List[Pull]

    @classmethod
    def parse(cls, s):
        game, pulls = s.split(": ")
        id = int(game[5:])
        pulls = fit(pulls.split("; ")).map(Pull.parse)
        return cls(id, pulls)

    def max(self, color):
        return self.pulls.map(lambda pull: getattr(pull, color)).max()

    @property
    def required(self):
        return self.max("red"), self.max("green"), self.max("blue")

    @property
    def possible(self, red=12, green=13, blue=14):
        r, g, b = self.required
        return r <= red and g <= green and b <= blue


def solve(input):
    return (
        split(input, "\n")
        .map(Game.parse)
        .filter(lambda game: game.possible)
        .map(lambda game: game.id)
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
