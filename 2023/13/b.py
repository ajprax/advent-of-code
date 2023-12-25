from utils import *


def int_from_chars(chars):
    out = 0
    for i, c in enumerate(chars):
        out += (c == "#") << i
    return out


def columns_from_rows(rows):
    return [[row[i] for row in rows] for i in range(len(rows[0]))]


def find_mirror(rows, smudges=1):
    for i in range(1, len(rows)):
        before, after = list(reversed(rows[:i])), rows[i:]
        total = 0
        for j in range(min(i, len(rows) - i)):
            total += (before[j] ^ after[j]).bit_count()
            if total > smudges:
                break
        if total == smudges:
            return i
    return 0


def solve_pattern(pattern):
    rows = split(pattern, "\n")
    cols = rows.transpose()
    rows = rows.map(int_from_chars)
    cols = cols.map(int_from_chars)
    row = find_mirror(rows)
    col = find_mirror(cols)
    return col + 100 * row


def solve(input):
    return split(input, "\n\n").map(solve_pattern).reduce(add)


with print_duration():
    print("solution:", solve(read("input.txt")))
