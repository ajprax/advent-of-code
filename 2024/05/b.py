from utils import *


def build_graph(rules):
    ordering = defaultdict(List)
    for a, b in rules:
        ordering[a].append(b)
    return ordering


def is_out_of_order(ordering):
    def test(update):
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if update[i] in ordering[update[j]]:
                    return True
    return test


def reorder(ordering):
    def _reorder(update):
        for i in range(1, len(update)):
            for j in range(i):
                if update[j] in ordering[update[i]]:
                    update.insert(j, update.pop(i))
        return update
    return _reorder


def solve(input):
    ordering, updates = split(input, "\n\n")
    ordering = build_graph(split(ordering, "\n", "|"))
    updates = split(updates, "\n", ",")

    return (
        updates
        .filter(is_out_of_order(ordering))
        .map(reorder(ordering))
        .map(lambda update: update[len(update) // 2])
        .map(int)
        .apply(sum)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
