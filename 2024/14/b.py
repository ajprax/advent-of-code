import builtins

import cv2

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


def show(robots):
    m = [[" " for _ in range(w)] for _ in range(h)]
    for robot in robots:
        x, y = robot.p
        m[y][x] = "0"
    print("\n".join("".join(row) for row in m))


def make_image(robots):
    m = np.zeros((h + 1, w + 1, 3), np.uint8)
    for robot in robots:
        x, y = robot.p
        m[y, x] = 255
    return m


def solve(input):
    robots = (
        split(input, "\n", " ", "=")
        .map(t(lambda p, v: Robot(
            split(p[1], ",").map(int),
            split(v[1], ",").map(int)
        )))
    )

    for i in range(10000):
        # 2 and 101 determined by manually inspecting and noticing repeating pattern
        if (i - 2) % 101 == 0:
            show(robots)
            print(i)
        for robot in robots:
            robot.move()


with print_duration():
    print("solution:", solve(read("input.txt")))
