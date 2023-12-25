from utils import *


def solve(input):
    times, records = split(input, "\n").map(lambda line: List(line[10:].split()).map(int))

    counts = List()
    for time, record in times.zip(records):
        count = 0
        for hold in range(time + 1):
            distance = hold * (time - hold)
            if distance > record:
                count += 1
        counts.append(count)
    return counts.reduce(mul)


with print_duration():
    print("solution:", solve(read("input.txt")))
