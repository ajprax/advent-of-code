from utils import *


def is_nice(s):
    if not (
        Tuple(s)
        .sliding(2)
        .enumerate()
        .group_by(itemgetter(1))
        .values()
        .any(lambda group: (
            group
            .map(itemgetter(0))
            .combinations(2)
            .any(t(lambda a, b: difference(a, b) > 1))
        ))
    ):
        return False
    if not (
        List(s)
        .sliding(3)
        .any(t(lambda a, b, c: a == c))
    ):
        return False
    return True


def solve(input):
    return split(input, "\n").filter(is_nice).size()


with print_duration():
    print("solution:", solve(read("input.txt")))
