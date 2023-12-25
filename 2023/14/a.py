from utils import *

raw = read("input.txt")


def rotate(matrix, direction):
    match direction:
        case "N":
            return matrix
        case "S":
            return np.rot90(matrix, 2)
        case "E":
            return np.rot90(matrix, 1)
        case "W":
            return np.rot90(matrix, 3)


def unrotate(matrix, direction):
    match direction:
        case "N":
            return matrix
        case "S":
            return np.rot90(matrix, 2)
        case "E":
            return np.rot90(matrix, 3)
        case "W":
            return np.rot90(matrix, 1)


def tilt(matrix, direction):
    # for each O, starting in the direction of the tilt, see how far it can move in that direction before hitting
    # something (the edge, a #, another O). Move it there and go to the next O
    matrix = rotate(matrix, direction)
    h, w = matrix.shape
    for y in range(h):
        for x in range(w):
            if matrix[y, x] == "O":
                for shift in range(1, y + 1):
                    if matrix[y - shift, x] == ".":
                        matrix[y - shift, x] = "O"
                        matrix[y - shift + 1, x] = "."
                    else:
                        break
    return unrotate(matrix, direction)


def calculate_load(matrix):
    h, _ = matrix.shape
    total = 0
    for i, row in enumerate(matrix):
        total += fit(row).count()["O"] * (h - i)
    return total


def solve(input):
    matrix = np.array(split(input, "\n", ""))
    matrix = tilt(matrix, "N")
    return calculate_load(matrix)


with print_duration():
    print("solution:", solve(read("input.txt")))
