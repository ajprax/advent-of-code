from utils import *


def process(input):
    def gen():
        input = input.iter()
        while input.has_next():
            i = input.next()
            count = input.take_while(lambda n: n == i).size() + 1
            yield count
            yield i
    return List(gen())


def solve(input):
    input = split(input, "\n", "").flatten().map(int)
    for _ in range(40):
        input = process(input)
    return input.size()


with print_duration():
    print("solution:", solve(read("input.txt")))
