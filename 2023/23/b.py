from utils import *


class Path:
    def __init__(self, last, visited=None):
        self.last = last
        self.visited = (visited or set()) | {last}

    def __contains__(self, item):
        return item in self.visited

    def __len__(self):
        return len(self.visited) - 1

    def add(self, xy):
        return Path(xy, self.visited)


class VertexPath:
    def __init__(self, last, visited=None, len=0):
        self.last = last
        self.visited = (visited or set()) | {last}
        self.len = len

    def __contains__(self, item):
        return item in self.visited

    def __len__(self):
        return self.len

    def add(self, xy, d):
        return VertexPath(xy, self.visited, self.len + d)


def not_in(path):
    @cache
    def test(x, y):
        return (x, y) not in path
    return test


def solve(input):
    grid = split(input, "\n", "")
    @cache
    def passable(x, y):
        return grid[y][x] != "#"

    @cache
    def inbounds(x, y):
        return 0 <= y < h and 0 <= x < w

    @cache
    def is_vertex(x, y):
        if not inbounds(x, y) or not passable(x, y):
            return False
        return (
                Tuple([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])
                .filter(t(inbounds))
                .filter(t(passable))
                .size() > 2
        )

    @cache
    def neighbors_(x, y):
        return neighbors(x, y).filter(t(inbounds)).filter(t(passable))

    def next_step(path):
        x, y = path.last
        return neighbors_(x, y).filter(t(not_in(path)))

    def next_vertex(path):
        x, y = path.last
        return (
            List(graph[(x, y)])
            .filter(t(lambda xy, d: not xy in path))
        )

    h, w = hw(grid)
    start = (grid[0].index("."), 0)
    end = (grid[-1].index("."), len(grid) - 1)
    vertices = Range(w).product(Range(h)).filter(t(is_vertex)).set()
    vertices.add(start)
    vertices.add(end)
    graph = defaultdict(list)  # key is vertex, values are [(vertex, distance)]

    def search_for_neighboring_vertices(start):
        paths = neighbors_(*start).map(lambda xy: Path(start).add(xy))
        for path in paths:
            while path.last not in vertices:
                path = path.add(next_step(path).only())
            graph[start].append((path.last, len(path)))

    vertices.for_each(search_for_neighboring_vertices)

    best = 0
    search = [VertexPath(start)]
    while search:
        path = search.pop()
        if path.last == end:
            if len(path) > best:
                best = len(path)
        else:
            for xy, d in next_vertex(path):
                search.append(path.add(xy, d))
    return best


with print_duration():
    print("solution:", solve(read("input.txt")))
