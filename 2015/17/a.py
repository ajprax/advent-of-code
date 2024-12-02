from utils import *


def solve(input):
    @cache
    def count_combinations(i, l):
        total = 0
        for i in range(i, len(containers)):
            if containers[i] == l:
                total += 1
            elif containers[i] < l:
                total += count_combinations(i + 1, l - containers[i])
        return total

    containers = split(input, "\n").map(int).sorted(reverse=True)
    return count_combinations(0, 150)


with print_duration():
    print("solution:", solve(read("input.txt")))
