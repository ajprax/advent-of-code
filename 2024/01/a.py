from utils import *


def solve(input):
    return (
        split(input, "\n", "   ")
        .unzip()
        .map(lambda a: a.map(int).sorted())
        .apply_and_fit(t(lambda l, r: zip(l, r)))
        .map(t(difference))
        .apply(sum)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
