from utils import *


def rules(i):
    if i == 0:
        return List([1])
    if len(str(i)) % 2 == 0:
        i = str(i)
        l, r = i[:len(i)//2], i[len(i)//2:]
        return List([int(l), int(r)])
    return List([i * 2024])


def step(stone, count):
    return rules(stone).map(lambda next_stone: (next_stone, count))


def collect(counts, stone_and_count):
    stone, count = stone_and_count
    if stone in counts:
        counts[stone] += count
    else:
        counts[stone] = count
    return counts


def solve(input):
    stones = split(input, " ").map(int).count().list()
    for i in range(75):
        stones = stones.flat_map(t(step)).fold(Dict(), collect).list()

    return stones.map(itemgetter(1)).apply(sum)


with print_duration():
    print("solution:", solve(read("input.txt")))
