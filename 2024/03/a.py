from utils import *


mul_re = re.compile("mul\((\d{1,3}),(\d{1,3})\)")


def solve(input):
    total = 0
    for match in mul_re.finditer(input):
        a, b = match.groups()
        total += int(a) * int(b)
    return total


with print_duration():
    print("solution:", solve(read("input.txt")))