from utils import *


def solve(input):
    @cache
    def combinations(i, l, so_far=()):
        total = []
        for i in range(i, len(containers)):
            if containers[i] == l:
                total.append(so_far + (l,))
            elif containers[i] < l:
                total.extend(combinations(i + 1, l - containers[i], so_far + (containers[i],)))
        return total

    containers = split(input, "\n").map(int).sorted(reverse=True)
    combos = List(combinations(0, 150))
    min_count = combos.map(len).min()
    return combos.filter(lambda combo: len(combo) == min_count).size()


with print_duration():
    print("solution:", solve(read("input.txt")))
