from utils import *


def derive(seq):
    seqs = fit([seq])
    while seqs[-1].any():
        seqs.append(seqs[-1].sliding(2).map(t(rsub)))
    return seqs.map(lambda seq: seq[-1]).reduce(add)


def solve(input):
    return (
        split(input, "\n", " ")
        .map(lambda line: line.map(int))
        .map(derive)
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
