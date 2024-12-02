from utils import *


def parse_line(line):
    match line:
        case [a, _, "lose", amount, *_, b]:
            return (a, b[:-1]), -int(amount)
        case [a, _, "gain", amount, *_, b]:
            return (a, b[:-1]), int(amount)


def total_happiness(rules):
    def total(order):
        return (
            Tuple(order + (order[0],))
            .sliding(2)
            .map(t(lambda a, b: rules.get((a, b), 0) + rules.get((b, a), 0)))
            .reduce(add)
        )

    return total


def solve(input):
    rules = split(input, "\n", None).map(parse_line).dict()
    people = rules.keys().flatten().set()
    return people.permutations().map(total_happiness(rules)).max()


with print_duration():
    print("solution:", solve(read("input.txt")))
