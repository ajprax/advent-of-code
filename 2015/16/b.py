from utils import *


exact = dict(children=3, samoyeds=2, akitas=0, vizslas=0, cars=2, perfumes=1)
greater = dict(cats=7, trees=3)
lesser = dict(pomeranians=3, goldfish=5)


def parse_line(line):
    return List(line.split(": ", 1)[1].split(", ")).map(lambda pair: split(pair, ": ")).dict().map_values(int)


def compatible(aunt):
    for key in set(exact) & set(aunt):
        if exact[key] != aunt[key]:
            return False
    for key in set(greater) & set(aunt):
        if greater[key] >= aunt[key]:
            return False
    for key in set(lesser) & set(aunt):
        if lesser[key] <= aunt[key]:
            return False
    return True


def solve(input):
    return (
        split(input, "\n")
        .map(parse_line)
        .enumerate(1)
        .only(t(lambda i, aunt: compatible(aunt)))
        [0]
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
