from utils import *


def count_matches(winning, playing):
    return len(set(winning) & set(playing))


def solve(input):
    original_cards = (
        split(input, "\n")
        .map(lambda line: line[10:])
        .map(lambda line: split(line, " | ", None))
    )

    count = 0
    cards = original_cards.enumerate()
    while cards:
        i, card = cards.pop()
        count += 1
        for j in range(count_matches(*card)):
            k = i + j + 1
            cards.append((k, original_cards[k]))
    return count


with print_duration():
    print("solution:", solve(read("input.txt")))

