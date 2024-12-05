from utils import *


import re


mul_re = re.compile("mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")


def solve(input):
    total = 0
    on = True
    for match in mul_re.finditer(input):
        if match.group() == "do()":
            on = True
        elif match.group() == "don't()":
            on = False
        else:
            a, b = match.groups()
            if on:
                total += int(a) * int(b)
    return total


with print_duration():
    print("solution:", solve(read("input.txt")))
