from utils import *


def concat(a, b):
    return int(str(a) + str(b))


def apply(operators, inputs):
    result = inputs[0]
    for operator, input in zip(operators, inputs[1:]):
        result = operator(result, input)
    return result

def result_if_possible(result, inputs):
    if (
        Iterator((add, mul, concat))
        .product(repeat=len(inputs) - 1)
        .any(lambda operators: apply(operators, inputs) == result)
    ):
        return result
    return 0


def solve(input):
    return (
        split(input, "\n")
        .map(lambda line: split(line, ": "))
        .map(t(lambda result, inputs: (int(result), split(inputs, " ").map(int))))
        .map(t(result_if_possible))
        .apply(sum)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
