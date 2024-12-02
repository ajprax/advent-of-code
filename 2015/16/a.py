from utils import *


known = dict(children=3, cats=7, samoyeds=2, pomeranians=3, akitas=0, vizslas=0, goldfish=5, trees=3, cars=2, perfumes=1)


def parse_line(line):
    return List(line.split(": ", 1)[1].split(", ")).map(lambda pair: split(pair, ": ")).dict().map_values(int)


def compatible(aunt):
    for key in set(known) & set(aunt):
        if known[key] != aunt[key]:
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
