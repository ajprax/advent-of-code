from utils import *


alphabet = "abcdefghijklmnopqrstuvwxyz"
confusing = {alphabet.index("i"), alphabet.index("o"), alphabet.index("l")}


def parse(input):
    return split(input, "\n", "").flatten().map(lambda c: alphabet.index(c))


def increment(password):
    if password[-1] == len(alphabet) - 1:
        return increment(password[:-1]) + [0]
    return password[:-1] + [password[-1] + 1]


def is_valid(password):
    if not password.sliding(3).any(t(lambda a, b, c: a + 1 == b and b + 1 == c)):
        return False
    if password.any(lambda c: c in confusing):
        return False
    if password.sliding(2).filter(t(eq)).map(tuple).set().size() < 2:
        return False
    return True


def solve(input):
    password = parse(input)
    while not is_valid(password):
        password = increment(password)
    return password.map(alphabet.__getitem__).apply("".join)


with print_duration():
    print("solution:", solve(read("input.txt")))

