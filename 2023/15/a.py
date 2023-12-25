from utils import *


def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def solve(input):
    return fit(split(input, ",")).map(hash).reduce(add)


with print_duration():
    print("solution:", solve(read("input.txt")))
