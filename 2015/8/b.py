from utils import *


DICT = str.maketrans({
    "\\": "\\\\",
    "\"": "\\\"",
})


def escape(s):
    return f"\"{s.translate(DICT)}\""


def count_line(line):
    return len(escape(line)), len(line)


def solve(input):
    return split(input, "\n").map(count_line).map(t(sub)).reduce(add)


with print_duration():
    print("solution:", solve(read("input.txt")))
