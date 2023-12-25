from utils import *


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


def spin(matrix):
    return tilt(tilt(tilt(tilt(matrix, "N"), "W"), "S"), "E")


def spin_until_stable(matrix):
    cycles = 0
    previous = fit([matrix])
    current = spin(matrix.copy())
    while not previous.any(lambda p: np.all(p == current)):
        cycles += 1
        previous.append(current)
        current = spin(current.copy())
    # find the start of the loop and it's length, and then play that forward to get to 1B
    start = previous.enumerate().first(t(lambda i, p: np.all(p == current)))[0]
    length = previous.size() - start
    return previous[start + ((1000000000 - start) % length)]


def tilt(matrix, direction):
    # for each O, starting in the direction of the tilt, see how far it can move in that direction before hitting
    # something (the edge, a #, another O). Move it there and go to the next O.
    matrix = rotate(matrix, direction)
    for y, x in zip(*np.where(matrix == "O")):
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
    return calculate_load(spin_until_stable(matrix))


with print_duration():
    print("solution:", solve(read("input.txt")))
