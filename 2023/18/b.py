from utils import *


def parse_line(line):
    line = line.split()[-1][2:-1]
    direction = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }[line[-1]]
    distance = int(line[:-1], 16)
    return direction, distance, None


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


def count_overlap(a):
    def count(b):
        (ax1, ay1), (ax2, ay2) = a
        (bx1, by1), (bx2, by2) = b
        if ax1 == ax2:
            # vertical line
            if bx1 != bx2 or ax1 != bx1:
                return 0
            ay1, ay2 = sorted((ay1, ay2))
            by1, by2 = sorted((by1, by2))
            if ay2 < by1 or ay1 > by2:
                return 0
            top = max(ay1, by1)
            bottom = min(ay2, by2)
            return bottom - top
        elif ay1 == ay2:
            # horizontal line
            if by1 != by2 or ay1 != by1:
                return 0
            ax1, ax2 = sorted((ax1, ax2))
            bx1, bx2 = sorted((bx1, bx2))
            if ax2 < bx1 or ax1 > bx2:
                return 0
            left = max(ax1, bx1)
            right = min(ax2, bx2)
            return right - left
    return count


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
    instructions = split(input, "\n").map(parse_line)
    vertices = get_vertices(instructions)
    segments = vertices.appended(vertices[0]).sliding(2)
    vertical_segments = segments.filter(t(lambda p1, p2: p1[1] != p2[1]))
    horizontal_segments = segments.filter(t(lambda p1, p2: p1[0] != p2[0]))

    xs, ys = vertices.unzip()
    xs = xs.sorted().distinct()
    ys = ys.sorted().distinct()

    inside = 0
    for (x1, x2), (y1, y2) in xs.sliding(2).product(ys.sliding(2)):
        if interior(vertical_segments, x1+1, y1):
            area = (x2-x1)*(y2-y1)
            left = (x1, y1), (x1, y2)
            left_overlap = vertical_segments.map(count_overlap(left)).apply(sum)
            top = (x1, y1), (x2, y1)
            top_overlap = horizontal_segments.map(count_overlap(top)).apply(sum)
            corner = bool(left_overlap and top_overlap)
            inside += area - left_overlap - top_overlap + corner
    border = int(segments.map(t(euclidean_distance)).reduce(add))
    # bottom right corners are not handled properly by the edge overlap checks
    bottom_right_corners = (
        instructions
        .map(itemgetter(0))
        .appended(instructions[0][0])
        .sliding(2)
        .filter(t(lambda a, b: a == "R" and b == "U"))
        .size()
    )
    return inside + border - bottom_right_corners


with print_duration():
    print("solution:", solve(read("input.txt")))
