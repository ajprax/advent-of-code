from utils import *


def step(n):
    return (n * 252533) % 33554393


def solve():
    target = 3075, 2981

    value = 20151125
    x = y = d = 1
    while (x, y) != target:
        if y == 1:
            d += 1
            x = 1
            y = d
        else:
            y -= 1
            x += 1
        value = step(value)
    return value


with print_duration():
    print("solution:", solve())
