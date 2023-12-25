from utils import *


def parse(line):
    springs, groups = line.split()
    return "?".join([springs]*5), fit([groups.split(",")]*5).flatten().map(int)


def solve_line(line):
    springs, groups = parse(line)

    # if the current position is a . move to the next
    # if it's a # it must be the start of the current group
    #   check if the rest of the group can fit with (not "." in springs[i:i+group] and springs[i+group+1] != "#")
    # if it's a ? proceed as if it's the start of the current group and do the same check, but also move to the next position as if it was a .

    @cache
    def count(si, gi):
        if si >= len(springs):
            return int(gi == len(groups))

        def as_working():
            return count(si + 1, gi)

        def as_broken():
            if (
                gi < len(groups)
                and si + groups[gi] <= len(springs)
                and "." not in springs[si: si + groups[gi]]
                and (si + groups[gi] >= len(springs) or "#" != springs[si + groups[gi]])
            ):
                # the group fits. move si forward by the group size plus one for padding
                return count(si + groups[gi] + 1, gi + 1)
            return 0

        match springs[si]:
            case ".":
                return as_working()
            case "#":
                return as_broken()
            case "?":
                return as_working() + as_broken()

    return count(0, 0)


def solve(input):
    return (
        split(input, "\n")
        .map(solve_line)
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))