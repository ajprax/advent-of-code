from utils import *


def parse_line(line):
    return line[0], line[2], int(line[4])


def build_graph(lines):
    graph = defaultdict(list)
    distances = Dict()
    for a, b, d in lines:
        graph[a].append(b)
        graph[b].append(a)
        distances[(a, b)] = d
        distances[(b, a)] = d
    return Dict(graph), distances


def find_paths(a, b, graph):
    def gen():
        search = [(Tuple((a,)), {a})]
        while search:
            path, visited = search.pop()
            if path[-1] == b:
                if len(path) == len(graph):
                    yield path
                continue
            for n in graph[a]:
                if n not in visited:
                    search.append((path + (n,), visited | {n}))
    return List(gen())


def length_of_path(path, distances):
    return path.sliding(2).map(distances.get).reduce(add)


def solve(input):
    graph, distances = build_graph(split(input, "\n", None).map(parse_line))
    return (
        graph
        .keys()
        .combinations(2)
        .flat_map(t(lambda a, b: find_paths(a, b, graph)))
        .map(lambda path: length_of_path(path, distances))
        .max()
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
