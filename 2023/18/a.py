from utils import *


def parse_line(line):
    direction, distance, color = line.split()
    distance = int(distance)
    color = color[1:-1]
    return direction, distance, color


def intersects(x, y):
    def test(line):
        (x1, y1), (x2, y2) = line
        return (
            (y1 <= y < y2 if y1 < y2 else y2 <= y < y1)
            and x > x1
        )
    return test


def interior(vertical_segments, x, y):
    return vertical_segments.filter(intersects(x, y)).size() % 2


def get_vertices(instructions):
    vertices = List()
    x, y = 0, 0
    for direction, distance, _ in instructions:
        match direction:
            case "R":
                x += distance
            case "L":
                x -= distance
            case "U":
                y -= distance
            case "D":
                y += distance
        vertices.append((x, y))
    minx = vertices.iter().map(itemgetter(0)).min()
    miny = vertices.iter().map(itemgetter(1)).min()
    return vertices.map(t(lambda x, y: (x - minx, y - miny)))


def solve(input):
    vertices = get_vertices(split(input, "\n").map(parse_line))
    maxx = vertices.iter().map(itemgetter(0)).max()
    maxy = vertices.iter().map(itemgetter(1)).max()
    segments = vertices.appended(vertices[0]).sliding(2)
    m = [["." for _ in range(maxx + 1)] for _ in range(maxy + 1)]
    for (x1, y1), (x2, y2) in segments:
        if x1 == x2:
            if y1 > y2:
                for y in range(y2, y1 + 1):
                    m[y][x1] = "#"
            else:
                for y in range(y1, y2 + 1):
                    m[y][x1] = "#"
        if y1 == y2:
            if x1 > x2:
                for x in range(x2, x1 + 1):
                    m[y1][x] = "#"
            else:
                for x in range(x1, x2 + 1):
                    m[y1][x] = "#"

    vertical_segments = segments.filter(t(lambda p1, p2: p1[1] != p2[1]))
    inside = Set()
    for x in range(maxx + 1):
        for y in range(maxy + 1):
            if interior(vertical_segments, x, y):
                inside.add((x, y))

    for x, y in inside.list().sorted():
        m[y][x] = "#"

    return fit(m).flatten().filter(lambda s: s == "#").size()


with print_duration():
    print("solution:", solve(read("input.txt")))
