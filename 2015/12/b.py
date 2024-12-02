import json

from utils import *


def tree_sum(json):
    match json:
        case str():
            return 0
        case None:
            return 0
        case int() | float():
            return json
        case list():
            return sum(tree_sum(item) for item in json)
        case dict():
            if "red" not in json.values():
                return sum(tree_sum(value) for value in json.values())
            return 0


def solve(input):
    input = json.loads(input)
    return tree_sum(input)


with print_duration():
    print("solution:", solve(read("input.txt")))
