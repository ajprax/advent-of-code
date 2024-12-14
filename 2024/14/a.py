from utils import *


h, w = 103, 101


@dataclass
class Robot:
    p: (int, int)
    v: (int, int)

    def move(self):
        px, py = self.p
        vx, vy = self.v
        self.p = (px + vx) % w, (py + vy) % h

    @property
    def quadrant(self):
        x, y = self.p
        left = x < w / 2 - 1
        right = x > w / 2
        top = y < h / 2 - 1
        bottom = y > h / 2
        if left and top:
            return "TL"
        if left and bottom:
            return "BL"
        if right and top:
            return "TR"
        if right and bottom:
            return "BR"


def solve(input):
    robots = (
        split(input, "\n", " ", "=")
        .map(t(lambda p, v: Robot(
            split(p[1], ",").map(int),
            split(v[1], ",").map(int)
        )))
    )

    for _ in range(100):
        for robot in robots:
            robot.move()

    counts = robots.count(lambda robot: robot.quadrant)
    counts.pop(None, None)
    return counts.values().reduce(mul)


with print_duration():
    print("solution:", solve(read("input.txt")))
