# similar reasoning as part 1, but the smallest group is size 4

from utils import *


def others(weights, group):
    return weights.filter(lambda w: w not in group)


def evenly_divisible(weights, ngroups=3):
    if ngroups == 1:
        return True
    total = sum(weights)
    target, remainder = divmod(total, ngroups)
    if remainder:
        return False
    return (
        weights
        .powerset()
        .any(lambda group: sum(group) == target and evenly_divisible(others(weights, group), ngroups - 1))
    )


def entanglement(group):
    e = 1
    for w in group:
        e *= w
    return e


def solve(input):
    weights = split(input, "\n").map(int).sorted(reverse=True).tuple()

    return (
        weights
        .combinations(4)
        .filter(lambda group: sum(group) == 384)
        .filter(lambda group: evenly_divisible(others(weights, group)))
        .map(entanglement)
        .min()
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
