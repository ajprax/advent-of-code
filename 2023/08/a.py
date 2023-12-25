from utils import *


def parse_graph(lines):
    return (
        split(lines, "\n")
        .map(lambda line: (line[:3], (line[7:10], line[12:15])))
        .dict()
    )


def solve(input):
    instructions, graph = input.split("\n\n")
    instructions = fit(instructions).repeat()
    graph = parse_graph(graph)

    pos = "AAA"
    steps = 0
    for instruction in instructions:
        steps += 1
        pos = graph[pos][instruction == "R"]
        if pos == "ZZZ":
            return steps


with print_duration():
    print("solution:", solve(read("input.txt")))
