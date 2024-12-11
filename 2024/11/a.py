from utils import *


def rules(i):
    if i == 0:
        return [1]
    if len(str(i)) % 2 == 0:
        i = str(i)
        l, r = i[:len(i)//2], i[len(i)//2:]
        return [int(l), int(r)]
    return [i * 2024]


def solve(input):
    stones = split(input, " ").map(int)
    for i in range(25):
        stones = stones.flat_map(rules)

    return len(stones)


with print_duration():
    print("solution:", solve(read("input.txt")))
