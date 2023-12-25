from utils import *


def parse_graph(lines):
    return (
        split(lines, "\n")
        .map(lambda line: (line[:3], (line[7:10], line[12:15])))
        .dict()
    )


def detect_loop_length(graph, instructions):
    def inner(pos):
        visited = set()
        steps = 0
        positions = []
        for i in fit(range(len(instructions))).iter().repeat():
            if (pos, i) in visited:
                break
            steps += 1
            visited.add((pos, i))
            positions.append(pos)
            pos = graph[pos][instructions[i] == "R"]
        return steps - positions.index(pos)
    return inner


def solve(input):
    instructions, graph = input.split("\n\n")
    instructions = fit(instructions).list()
    graph = parse_graph(graph)
    loop_lengths = graph.keys().filter(lambda pos: pos[-1] == "A").map(detect_loop_length(graph, instructions)).list()
    return lcm(*loop_lengths)


with print_duration():
    print("solution:", solve(read("input.txt")))
