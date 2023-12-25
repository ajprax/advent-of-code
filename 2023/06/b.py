from utils import *


def solve(input):
    def wins(hold):
        return hold * (time - hold) > record

    def lowest():
        _min = 1
        _max = time
        while True:
            mid = _min + ((_max - _min) // 2)
            if _min == _max:
                break
            if wins(mid):
                _max = mid
            elif _min == mid:
                # _min only equals mid if _min + 1 equals _max
                _min = _max
            else:
                _min = mid
        return mid

    def highest():
        _min = 1
        _max = time
        while True:
            mid = (_min + _max) // 2
            if mid == _min:
                break
            if wins(mid):
                _min = mid
            else:
                _max = mid
        return mid

    time, record = split(input, "\n").map(lambda line: int(line[10:].replace(" ", "")))
    l = lowest()
    h = highest()
    return h - l + 1


with print_duration():
    print("solution:", solve(read("input.txt")))
