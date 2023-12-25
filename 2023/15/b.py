from utils import *


@dataclass
class Insert:
    box: int
    label: str
    n: int


@dataclass
class Remove:
    box: int
    label: str


def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def parse(instruction):
    if "=" in instruction:
        label, n = instruction.split("=")
        box = hash(label)
        return Insert(box, label, int(n))
    if "-" in instruction:
        label = instruction[:-1]
        box = hash(label)
        return Remove(box, label)


def remove(ls, i):
    return ls[:i] + ls[:i+1:]


def process(instructions):
    boxes = [[] for _ in range(256)]
    for instruction in instructions:
        match instruction:
            case Insert(box, label, n):
                for i in range(len(boxes[box])):
                    if boxes[box][i][0] == label:
                        boxes[box][i] = (label, n)
                        break
                else:
                    boxes[box].append((label, n))

            case Remove(box, label):
                boxes[box] = [(l, n) for (l, n) in boxes[box] if l != label]
    return boxes


def focusing_power(boxes):
    total = 0
    for boxi, box in enumerate(boxes, 1):
        for lensi, (label, lens) in enumerate(box, 1):
            total += boxi * lensi * lens
    return total


def solve(input):
    instructions = split(input, ",").map(parse)
    boxes = process(instructions)
    return focusing_power(boxes)


with print_duration():
    print("solution:", solve(read("input.txt")))
