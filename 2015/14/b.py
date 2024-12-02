from utils import *


@dataclass
class Deer:
    speed: int
    fly: int
    rest: int
    flying: int = 0
    resting: int = 0
    distance: int = 0
    points: int = 0

    def step(self):
        if self.flying < self.fly:
            self.flying += 1
            self.distance += self.speed
        elif self.resting < self.rest:
            self.resting += 1
        if self.resting == self.rest:
            self.flying = 0
            self.resting = 0
        return self.distance

    def give_point(self):
        self.points += 1


def parse_line(line):
    speed = line[3]
    fly = line[6]
    rest = line[13]
    return Deer(int(speed), int(fly), int(rest))


def solve(input):
    deer = split(input, "\n", None).map(parse_line)
    for i in range(2503):
        lead = deer.map(lambda d: d.step()).max()
        deer.filter(lambda d: d.distance == lead).for_each(lambda d: d.give_point())
    return deer.map(lambda d: d.points).max()


with print_duration():
    print("solution:", solve(read("input.txt")))
