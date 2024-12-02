from utils import *


def is_nice(s):
    if List(s).filter(lambda c: c in "aeiou").size() < 3:
        return False
    if List(s).sliding(2).all(t(ne)):
        return False
    if List(["ab", "cd", "pq", "xy"]).any(lambda bad: bad in s):
        return False
    return True


def solve(input):
    return split(input, "\n").filter(is_nice).size()


with print_duration():
    print("solution:", solve(read("input.txt")))
