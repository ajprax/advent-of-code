from utils import *


def passable(grid):
    def test(x, y):
        return grid[y][x] != "#"
    return test


def not_in(path):
    def test(x, y):
        return (x, y) not in path
    return test


def next_step(grid, path):
    x, y = path[-1]
    if grid[y][x] == ">":
        possibilities = List([(x + 1, y)])
    elif grid[y][x] == "v":
        possibilities = List([(x, y + 1)])
    elif grid[y][x] == "^":
        possibilities = List([(x, y - 1)])
    elif grid[y][x] == "<":
        possibilities = List([(x - 1, y)])
    else:
        possibilities = neighbors(x, y)
    yield from (
        possibilities
        .filter(t(inbounds(grid)))
        .filter(t(passable(grid)))
        .filter(t(not_in(path)))
    )


def solve(input):
    grid = split(input, "\n", "")
    start = grid[0].index("."), 0
    end = grid[-1].index("."), len(grid) - 1
    paths = List()
    search = [List([start])]
    while search:
        path = search.pop()
        if path[-1] == end:
            paths.append(path)
        else:
            for xy in next_step(grid, path):
                search.append(path.appended(xy))

    return paths.map(len).max() - 1


with print_duration():
    print("solution:", solve(read("input.txt")))
