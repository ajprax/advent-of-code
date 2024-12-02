from utils import *


def parse_line(line):
    speed = line[3]
    fly = line[6]
    rest = line[13]
    return int(speed), int(fly), int(rest)


def calculate(duration):
    def calc(speed, fly, rest):
        remaining = duration
        distance = 0
        while remaining > 0:
            if remaining < fly:
                distance += remaining * speed
                remaining -= remaining
            else:
                distance += fly * speed
                remaining -= fly + rest
        return distance
    return calc


def solve(input):
    return split(input, "\n", None).map(parse_line).map(t(calculate(2503))).max()


with print_duration():
    print("solution:", solve(read("input.txt")))
