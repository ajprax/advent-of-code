from sklearn.cluster import SpectralClustering

from utils import *


def parse_line(line):
    l, r = line.split(": ")
    r = r.split()
    return l, r


def parse_graph(input):
    ids = count()
    name_to_id = {}
    graph = defaultdict(set)
    for l, r in split(input, "\n").map(parse_line):
        if l not in name_to_id:
            name_to_id[l] = next(ids)
        l = name_to_id[l]
        for c in r:
            if c not in name_to_id:
                name_to_id[c] = next(ids)
            c = name_to_id[c]
            graph[l].add(c)
            graph[c].add(l)
    return Dict(graph)


def adjacency_matrix(graph):
    n = len(graph)
    m = np.zeros((n, n))
    for a, bs in graph.items():
        for b in bs:
            m[a, b] = 1
    return m


def cluster(graph, n=2):
    m = adjacency_matrix(graph)
    labels = SpectralClustering(n_clusters=n, affinity='precomputed', assign_labels='discretize').fit_predict(m)
    return (
        Iterator(labels)
        .enumerate()
        .group_by(itemgetter(1))
        .values()
        .map(lambda values: values.map(itemgetter(0)))
        .list()
    )


def connections(graph, clusters):
    a, b = clusters
    return a.flat_map(graph.get).filter(b.contains).size()


def solve(input):
    graph = parse_graph(input)
    clusters = cluster(graph)
    assert connections(graph, clusters) == 3
    return clusters.map(len).reduce(mul)


with print_duration():
    print("solution:", solve(read("sample.txt")), "expected:", 54)

with print_duration():
    print("solution:", solve(read("input.txt")))
