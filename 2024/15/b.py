from utils import *


def widen(map):
    def _widen(c):
        if c == ".":
            return ".."
        if c == "O":
            return "[]"
        if c == "@":
            return "@."
        if c == "#":
            return "##"
    return map.map(lambda row: row.flat_map(_widen))


def find_robot(map):
    h, w = hw(map)
    for y in range(h):
        try:
            x = map[y].index("@")
            return x, y
        except ValueError:
            pass


def solve(input):
    map, instructions = split(input, "\n\n")
    map = widen(split(map, "\n", ""))
    instructions = split(instructions, "\n", "").flatten()
    rx, ry = find_robot(map)

    def box(x, y):
        if map[y][x] == "[":
            return x, y
        elif map[y][x] == "]":
            return x - 1, y

    # x and y must be the left index of the box
    # -> [] indicates the box cannot be moved
    # -> [(x, y), ...] indicates the boxes pushed by this box in order, including itself
    def pushes(x, y, d):
        match d:
            case "<":
                match map[y][x - 1]:
                    case ".":
                        return [(x, y)]
                    case "#":
                        return []
                    case "]":
                        transitive = pushes(x - 2, y, d)
                        if transitive:
                            return [(x, y), *transitive]
                        return []
            case ">":
                match map[y][x + 2]:
                    case ".":
                        return [(x, y)]
                    case "#":
                        return []
                    case "[":
                        transitive = pushes(x + 2, y, d)
                        if transitive:
                            return [(x, y), *transitive]
                        return []
            case "^":
                match (map[y - 1][x], map[y - 1][x + 1]):
                    case ("#", _):
                        return []
                    case (_, "#"):
                        return []
                    case (".", "."):
                        return [(x, y)]
                    case ("[", "]"):
                        transitive = pushes(x, y - 1, d)
                        if transitive:
                            return [(x, y), *transitive]
                        return []
                    case ("]", "."):
                        transitive = pushes(x - 1, y - 1, d)
                        if transitive:
                            return [(x, y), *transitive]
                        return None
                    case ".", "[":
                        transitive = pushes(x + 1, y - 1, d)
                        if transitive:
                            return [(x, y), *transitive]
                        return None
                    case "]", "[":
                        left = pushes(x - 1, y - 1, d)
                        right = pushes(x + 1, y - 1, d)
                        if left and right:
                            return [(x, y), *left, *right]
                        return []
            case "v":
                match (map[y + 1][x], map[y + 1][x + 1]):
                    case ("#", _):
                        return []
                    case (_, "#"):
                        return []
                    case (".", "."):
                        return [(x, y)]
                    case ("[", "]"):
                        transitive = pushes(x, y + 1, d)
                        if transitive:
                            return [(x, y), *transitive]
                        return None
                    case ("]", "."):
                        transitive = pushes(x - 1, y + 1, d)
                        if transitive:
                            return [(x, y), *transitive]
                        return None
                    case ".", "[":
                        transitive = pushes(x + 1, y + 1, d)
                        if transitive:
                            return [(x, y), *transitive]
                        return None
                    case "]", "[":
                        left = pushes(x - 1, y + 1, d)
                        right = pushes(x + 1, y + 1, d)
                        if left and right:
                            return [(x, y), *left, *right]
                        return []

    for d in instructions:
        match d:
            case "<":
                match map[ry][rx - 1]:
                    case "#":
                        continue
                    case "]":
                        boxes = pushes(rx - 2, ry, d)
                        if not boxes:
                            continue
                        for bx, by in List(boxes).reversed().distinct():
                            map[by][bx - 1] = "["
                            map[by][bx] = "]"
                map[ry][rx - 1] = "@"
                map[ry][rx] = "."
                rx -= 1
            case ">":
                match map[ry][rx + 1]:
                    case "#":
                        continue
                    case "[":
                        boxes = pushes(rx + 1, ry, d)
                        if not boxes:
                            continue
                        for bx, by in List(boxes).reversed().distinct():
                            map[by][bx + 1] = "["
                            map[by][bx + 2] = "]"
                map[ry][rx + 1] = "@"
                map[ry][rx] = "."
                rx += 1
            case "^":
                match map[ry - 1][rx]:
                    case "#":
                        continue
                    case "[" | "]":
                        boxes = pushes(*box(rx, ry - 1), d)
                        if not boxes:
                            continue
                        for bx, by in List(boxes).reversed().distinct():
                            map[by - 1][bx] = "["
                            map[by - 1][bx + 1] = "]"
                            map[by][bx] = "."
                            map[by][bx + 1] = "."
                map[ry - 1][rx] = "@"
                map[ry][rx] = "."
                ry -= 1
            case "v":
                match map[ry + 1][rx]:
                    case "#":
                        continue
                    case "[" | "]":
                        boxes = pushes(*box(rx, ry + 1), d)
                        if not boxes:
                            continue
                        for bx, by in List(boxes).reversed().distinct():
                            map[by + 1][bx] = "["
                            map[by + 1][bx + 1] = "]"
                            map[by][bx] = "."
                            map[by][bx + 1] = "."
                map[ry + 1][rx] = "@"
                map[ry][rx] = "."
                ry += 1

    return (
        indices(map)
        .filter(t(lambda x, y: map[y][x] == "["))
        .map(t(lambda x, y: x + 100 * y))
        .apply(sum)
    )


with print_duration():
    print("solution:", solve(read("input.txt")))
