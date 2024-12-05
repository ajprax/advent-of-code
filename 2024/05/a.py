from utils import *


def build_graph(rules):
    ordering = defaultdict(List)
    for a, b in rules:
        ordering[a].append(b)
    return ordering


def is_in_order(ordering):
    def test(update):
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if update[i] in ordering[update[j]]:
                    return False
        return True
    return test


def solve(input):
    ordering, updates = split(input, "\n\n")
    ordering = build_graph(split(ordering, "\n", "|"))
    updates = split(updates, "\n", ",")

    return (
        updates
        .filter(is_in_order(ordering))
        .map(lambda update: update[len(update) // 2])
        .map(int)
        .apply(sum)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
