# a group of 5 is impossible because the only even number is 2, so there would need to be 4 numbers that sum to 510 which there are not
# there is a group of 6, so 6 is the target size
# find all the groups of 6 that sum to 512
# prove that the remaining weights can be divided into two groups of 512

from utils import *


def others(weights, group):
    return weights.filter(lambda w: w not in group)


def evenly_divisible(weights, ngroups=2):
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
        .combinations(6)
        .filter(lambda group: sum(group) == 512)
        .filter(lambda group: evenly_divisible(others(weights, group)))
        .map(entanglement)
        .min()
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
