from utils import *


def is_empty(line):
    return "#" not in line


def between(a, b):
    if a < b:
        def test(c):
            return a < c < b
    else:
        def test(c):
            return b < c < a
    return test


def manhattan_distance(empty_rows, empty_cols):
    def inner(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return (
            999999 * (empty_cols.filter(between(x1, x2)).size() + empty_rows.filter(between(y1, y2)).size())
            + abs(x2 - x1)
            + abs(y2 - y1)
        )
    return inner


def solve(input):
    grid = split(input, "\n", "")
    empty_rows = grid.enumerate().filter(t(lambda y, row: is_empty(row))).map(itemgetter(0))
    empty_cols = grid.transpose().enumerate().filter(t(lambda x, col: is_empty(col))).map(itemgetter(0))

    return (
        grid
        .map(lambda row: row.enumerate())
        .enumerate()
        .flat_map(t(lambda y, row: row.map(t(lambda x, s: (x, y, s)))))
        .filter(t(lambda x, y, s: s == "#"))
        .map(itemgetter(0, 1))
        .combinations(2)
        .map(t(manhattan_distance(empty_rows, empty_cols)))
        .reduce(add)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
