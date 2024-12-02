from utils import *


def divisors(n):
    out = List()
    for i in range(1, floor(sqrt(n)) + 1):
        if not n % i:
            out.append(i)
    return out.flat_map(lambda i: (i, n // i)).filter(lambda i: i * 50 >= n)


def npresents(house):
    return divisors(house).reduce(add, 0) * 11


def solve(input):
    return Iterator(count(1)).map_to_pairs(npresents).first(t(lambda i, presents: presents >= int(input)))[0]


with print_duration():
    print("solution:", solve(read("input.txt")))
