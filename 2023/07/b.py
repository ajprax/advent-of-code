from utils import *


def convert(hand):
    return (
        hand
        .replace("A", "e")
        .replace("K", "d")
        .replace("Q", "c")
        .replace("J", "1")  # jokers are lowest in this variant
        .replace("T", "a")
    )


@dataclass
class HandWager:
    hand: str
    wager: int

    def __post_init__(self):
        self.wager = int(self.wager)

    @property
    def type(self):
        counts = fit(self.hand).count()
        jokers = counts.pop("J", 0)
        counts = counts.values().list().sorted()
        if counts:
            # adding all the jokers to the largest group is always best
            counts[-1] += jokers
        else:
            # a hand that's all jokers is 5 of a kind
            counts = [5]

        if counts == [5]:
            return 6
        elif counts == [1, 4]:
            return 5
        elif counts == [2, 3]:
            return 4
        elif counts == [1, 1, 3]:
            return 3
        elif counts == [1, 2, 2]:
            return 2
        elif counts == [1, 1, 1, 2]:
            return 1
        elif counts == [1, 1, 1, 1, 1]:
            return 0

    def key(self):
        return self.type, convert(self.hand)


def solve(input):
    return (
        split(input, "\n", None)
        .map(t(HandWager))
        .sorted(HandWager.key)
        .enumerate(1)
        .map(t(lambda rank, hw: rank * hw.wager))
        .reduce(add, 0)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
